# Generated by Django 4.1.3 on 2024-01-15 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zahteve', '0040_monitoringreport_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoringreport',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Objavi?'),
        ),
    ]
