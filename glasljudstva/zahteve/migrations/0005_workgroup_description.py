# Generated by Django 3.2.9 on 2021-11-12 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zahteve', '0004_merge_20211112_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='workgroup',
            name='description',
            field=models.TextField(default='primer'),
            preserve_default=False,
        ),
    ]