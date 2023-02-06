# Generated by Django 4.1.3 on 2023-02-06 11:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zahteve', '0034_alter_monitoringreport_state'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workgroup',
            options={'verbose_name': 'Področje dela', 'verbose_name_plural': 'Področja dela'},
        ),
        migrations.AddField(
            model_name='workgroup',
            name='order',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Vrstni red za sortiranje na seznamu'),
        ),
    ]
