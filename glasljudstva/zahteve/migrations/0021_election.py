# Generated by Django 4.0.3 on 2022-08-11 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zahteve", "0020_voterquestion"),
    ]

    operations = [
        migrations.CreateModel(
            name="Election",
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
                ("name", models.TextField()),
                ("slug", models.SlugField()),
            ],
        ),
    ]
