"""
WSGI config for risk_lms project.
"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'risk_lms.settings')

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'risk_lms.settings')

# Run migrations if needed before starting the WSGI app
try:
	from .migrate_on_start import migrate_if_needed
	migrate_if_needed()
except Exception as e:
	print(f'Error running migrate_on_start: {e}')

application = get_wsgi_application()
