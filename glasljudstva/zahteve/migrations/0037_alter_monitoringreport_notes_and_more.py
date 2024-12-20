# Generated by Django 4.1.3 on 2023-02-06 12:33

import martor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("zahteve", "0036_alter_monitoringreport_notes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="monitoringreport",
            name="notes",
            field=martor.models.MartorField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="monitoringreport",
            name="summary",
            field=martor.models.MartorField(blank=True, max_length=5000, null=True),
        ),
    ]
