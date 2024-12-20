# Generated by Django 4.1.3 on 2024-02-15 12:01

import martor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_alter_sidebarlink_icon_alter_sidebarlink_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContentPage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Naslov")),
                (
                    "content",
                    martor.models.MartorField(
                        blank=True, null=True, verbose_name="Vsebina"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        help_text="Ime strani v povezavi (npr. glas-ljudstva.si/kljuc-za-povezavo, pusti prazno za samodejno generiranje ključa)",
                        max_length=200,
                        verbose_name="Ključ za povezavo",
                    ),
                ),
                (
                    "published",
                    models.BooleanField(default=False, verbose_name="Objavljeno"),
                ),
            ],
            options={
                "verbose_name": "Vsebinska stran",
                "verbose_name_plural": "Vsebinske strani",
            },
        ),
    ]
