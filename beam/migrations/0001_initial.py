# Generated by Django 3.2.6 on 2021-09-14 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='loadCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='pointLoad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('magnitude', models.DecimalField(decimal_places=2, max_digits=8)),
                ('location', models.CharField(max_length=10)),
                ('load_case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='beam.loadcase')),
            ],
        ),
    ]