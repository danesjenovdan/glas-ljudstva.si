# Generated by Django 4.0.1 on 2022-01-14 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zahteve', '0015_alter_demandanswer_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='party_name',
            field=models.TextField(blank=True),
        ),
    ]