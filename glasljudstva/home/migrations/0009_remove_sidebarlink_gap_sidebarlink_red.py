# Generated by Django 4.1.3 on 2024-02-26 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0008_alter_campaignitem_options_campaignitem_ordering"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sidebarlink",
            name="gap",
        ),
        migrations.AddField(
            model_name="sidebarlink",
            name="red",
            field=models.BooleanField(default=False, verbose_name="Rdeče"),
        ),
    ]
