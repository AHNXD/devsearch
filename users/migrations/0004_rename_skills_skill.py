# Generated by Django 5.1.4 on 2024-12-21 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_location_skills'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Skills',
            new_name='Skill',
        ),
    ]
