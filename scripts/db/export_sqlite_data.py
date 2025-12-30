"""
Export data from SQLite database to JSON for migration to MSSQL.
Handles UTF-8 encoding and special characters.
"""
import os
import sys
import json
import codecs

# Set environment variables BEFORE importing Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'risk_lms.settings')
os.environ['DB_ENGINE'] = 'sqlite'

# Force UTF-8 encoding on Windows
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

import django
django.setup()

from django.core import serializers
from django.apps import apps

def get_all_models():
    """Get all models from installed apps."""
    all_models = []
    excluded_apps = ['contenttypes', 'auth.permission']
    
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            model_label = f"{app_config.label}.{model._meta.model_name}"
            if model_label not in excluded_apps and app_config.label != 'contenttypes':
                all_models.append(model)
    
    return all_models

def export_data():
    """Export all data from SQLite to JSON file with proper encoding."""
    print("Exporting data from SQLite database...")
    
    try:
        all_data = []
        models = get_all_models()
        
        for model in models:
            model_name = f"{model._meta.app_label}.{model._meta.model_name}"
            try:
                queryset = model.objects.all()
                count = queryset.count()
                if count > 0:
                    data = serializers.serialize('python', queryset)
                    all_data.extend(data)
                    print(f"  + {model_name}: {count} records")
            except Exception as e:
                print(f"  ! {model_name}: Skipped - {e}")
        
        # Write to file with UTF-8 encoding
        output_file = 'data_backup.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nData exported successfully to {output_file}")
        print(f"  Total records: {len(all_data)}")
        return True
        
    except Exception as e:
        print(f"\nError exporting data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    export_data()
