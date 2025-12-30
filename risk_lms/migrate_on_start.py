import os
from django.core.management import call_command
from django.db import OperationalError

def migrate_if_needed():
    try:
        from django.db.migrations.executor import MigrationExecutor
        from django.db import connections
        connection = connections['default']
        executor = MigrationExecutor(connection)
        targets = executor.loader.graph.leaf_nodes()
        plan = executor.migration_plan(targets)
        if plan:
            print('Applying pending migrations...')
            call_command('migrate', interactive=False)
        else:
            print('No pending migrations.')
    except OperationalError as e:
        print(f'Error checking migrations: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')
