from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_interactivecourseprogress_slide_timestamps_and_skip_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='interactivecourse',
            name='scale_mode',
            field=models.CharField(default='showAll', help_text='Captivate scale mode', max_length=20),
        ),
    ]
