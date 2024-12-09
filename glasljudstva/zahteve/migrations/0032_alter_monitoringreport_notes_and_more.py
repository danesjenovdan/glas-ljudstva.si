# Generated by Django 4.1.3 on 2023-01-08 23:01

import martor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("zahteve", "0031_statebody_monitoringreport"),
    ]

    operations = [
        migrations.AlterField(
            model_name="monitoringreport",
            name="notes",
            field=martor.models.MartorField(
                blank=True,
                max_length=300,
                null=True,
                verbose_name="Opombe (max 300 znakov)",
            ),
        ),
        migrations.AlterField(
            model_name="monitoringreport",
            name="summary",
            field=martor.models.MartorField(
                blank=True,
                max_length=1100,
                null=True,
                verbose_name="Kratek povzetek ugotovitev o  uresničevanju zaveze (max 1100 znakov)",
            ),
        ),
    ]
