"""
WSGI config for risk_lms project.
"""

import os

import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "risk_lms.settings")

# Ensure Django is initialized before checking migrations.
django.setup()

try:
    from .migrate_on_start import migrate_if_needed

    migrate_if_needed()
except Exception as exc:
    # Avoid failing the whole app startup if migrations can't be checked/applied.
    print(f"Error running migrate_on_start: {exc}")

application = get_wsgi_application()
