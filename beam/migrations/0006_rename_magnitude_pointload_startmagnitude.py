# Generated by Django 3.2.6 on 2021-12-07 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beam', '0005_distributedload'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pointload',
            old_name='magnitude',
            new_name='startMagnitude',
        ),
    ]
