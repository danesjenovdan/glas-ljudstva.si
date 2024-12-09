# Generated by Django 4.1.3 on 2024-02-14 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_newsitem"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sidebarlink",
            name="icon",
            field=models.CharField(
                choices=[
                    ("box-title", "Naslov polja"),
                    ("eye", "Oko"),
                    ("handshake", "Roka"),
                ],
                default="handshake",
                max_length=100,
                verbose_name="Ikona",
            ),
        ),
        migrations.AlterField(
            model_name="sidebarlink",
            name="url",
            field=models.CharField(
                blank=True, max_length=512, null=True, verbose_name="Povezava"
            ),
        ),
    ]
