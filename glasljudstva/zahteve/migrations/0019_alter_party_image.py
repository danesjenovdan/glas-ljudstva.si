# Generated by Django 4.0.1 on 2022-02-11 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zahteve", "0018_party_image_party_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="party",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
