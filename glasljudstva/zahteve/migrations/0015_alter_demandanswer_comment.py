# Generated by Django 4.0.1 on 2022-01-13 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zahteve", "0014_party_finished_quiz"),
    ]

    operations = [
        migrations.AlterField(
            model_name="demandanswer",
            name="comment",
            field=models.CharField(blank=True, default="", max_length=1024),
        ),
    ]
