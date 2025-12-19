"""
Add course completion time limits and enhance content management
"""
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='completion_time_limit',
            field=models.IntegerField(
                default=0,
                help_text='Time limit for course completion in days (0 = no limit)'
            ),
        ),
        migrations.AddField(
            model_name='course',
            name='completion_time_enabled',
            field=models.BooleanField(
                default=False,
                help_text='Enable time limit for course completion'
            ),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='deadline',
            field=models.DateTimeField(
                null=True,
                blank=True,
                help_text='Deadline for course completion'
            ),
        ),
    ]