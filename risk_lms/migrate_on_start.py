import os
import time
from contextlib import contextmanager
from pathlib import Path

import django
from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.db import OperationalError, connections


@contextmanager
def _migration_lock(timeout_seconds: int = 120):
    """
    Best-effort cross-process lock to avoid concurrent migrations on multi-worker IIS.
    - MSSQL: uses sp_getapplock (recommended).
    - Other DBs: falls back to a filesystem lock.
    """
    engine = connections["default"].settings_dict.get("ENGINE", "")
    if engine in {"mssql", "sql_server.pyodbc"}:
        lock_name = "risk_lms:migrate_on_start"
        lock_timeout_ms = max(0, int(timeout_seconds * 1000))
        try:
            cursor = connections["default"].cursor()
            try:
                cursor.execute(
                    "DECLARE @res int; "
                    "EXEC @res = sp_getapplock "
                    "@Resource=%s, @LockMode='Exclusive', @LockOwner='Session', @LockTimeout=%s; "
                    "SELECT @res;",
                    [lock_name, lock_timeout_ms],
                )
                result = cursor.fetchone()
                # sp_getapplock returns:
                # 0 = lock granted, 1 = lock granted (after waiting),
                # negative values = failure.
                if not result or int(result[0]) < 0:
                    yield False
                    return
                yield True
                return
            finally:
                try:
                    cursor.execute(
                        "EXEC sp_releaseapplock @Resource=%s, @LockOwner='Session';",
                        [lock_name],
                    )
                except Exception:
                    pass
                try:
                    cursor.close()
                except Exception:
                    pass
        except Exception:
            # If advisory locks aren't available, fall back to a filesystem lock.
            pass

    base_dir = getattr(settings, "BASE_DIR", None)
    if base_dir:
        lock_path = str(Path(base_dir) / ".migrate_on_start.lock")
    else:
        lock_path = str(Path(__file__).resolve().parent.parent / ".migrate_on_start.lock")
    start = time.time()
    lock_file = None
    try:
        lock_file = open(lock_path, "a+")
        while True:
            try:
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                yield True
                return
            except Exception:
                if time.time() - start >= timeout_seconds:
                    yield False
                    return
                time.sleep(0.5)
    finally:
        if lock_file is not None:
            try:
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            except Exception:
                pass
            try:
                lock_file.close()
            except Exception:
                pass

def migrate_if_needed():
    if os.environ.get("RUN_MIGRATIONS_ON_START", "true").lower() not in {"1", "true", "yes"}:
        return

    # If called before get_wsgi_application(), ensure app registry is ready.
    if not apps.ready:
        django.setup()

    try:
        from django.db.migrations.executor import MigrationExecutor

        connection = connections["default"]
        executor = MigrationExecutor(connection)
        targets = executor.loader.graph.leaf_nodes()
        plan = executor.migration_plan(targets)
        if plan:
            with _migration_lock() as acquired:
                if not acquired:
                    print("Skipping migrations (could not acquire migration lock).")
                    return
                # Re-check plan after acquiring the lock to avoid redundant work.
                executor = MigrationExecutor(connection)
                targets = executor.loader.graph.leaf_nodes()
                plan = executor.migration_plan(targets)
                if not plan:
                    print("No pending migrations.")
                    return
                print("Applying pending migrations...")
                call_command("migrate", interactive=False, verbosity=1)
        else:
            print("No pending migrations.")
    except OperationalError as e:
        print(f"Error checking migrations: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
