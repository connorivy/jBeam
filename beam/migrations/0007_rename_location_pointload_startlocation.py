# Generated by Django 3.2.6 on 2021-12-07 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beam', '0006_rename_magnitude_pointload_startmagnitude'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pointload',
            old_name='location',
            new_name='startLocation',
        ),
    ]