# Generated by Django 3.2.9 on 2021-11-12 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zahteve', '0009_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='permission',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]