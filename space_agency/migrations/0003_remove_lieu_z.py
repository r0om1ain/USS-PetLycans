from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space_agency', '0002_lieu_and_mission_destination_fk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lieu',
            name='z',
        ),
    ]
