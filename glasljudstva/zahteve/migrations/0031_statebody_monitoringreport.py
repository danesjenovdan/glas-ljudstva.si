# Generated by Django 4.1.3 on 2023-01-08 22:39

import django.db.models.deletion
import martor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zahteve", "0030_party_mautic_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="StateBody",
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
                ("name", models.TextField(verbose_name="Državni organ")),
            ],
            options={
                "verbose_name": "Državni organ",
                "verbose_name_plural": "Državni organi",
            },
        ),
        migrations.CreateModel(
            name="MonitoringReport",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "present_in_coalition_treaty",
                    models.TextField(
                        blank=True,
                        choices=[("yes", "Da"), ("no", "Ne"), ("partially", "Delno")],
                        verbose_name="Je predvolilna zaveza vključena v koalicijsko pogodbo?",
                    ),
                ),
                (
                    "cooperative",
                    models.BooleanField(
                        default=False,
                        verbose_name="Državni organ(i) sodeluje(jo) z Glasom ljudstva pri spremljanju uresničevanja zaveze",
                    ),
                ),
                (
                    "state",
                    models.TextField(
                        blank=True,
                        choices=[
                            ("fulfilled", "IZPOLNJENA (zaveza je v celoti uresničena)"),
                            (
                                "partially_fulfilled",
                                "DELNO IZPOLNJENA (nekateri elementi zaveze so uresničeni)",
                            ),
                            ("in_progress", "V IZVAJANJU (delo še poteka)"),
                            (
                                "stuck",
                                "ZASTALA (poskusi uresničevanja so bili neuspešni)",
                            ),
                            (
                                "untouched",
                                "NEDOTAKNJENA (sploh ni prizadevanj ali poskusov, da bi zavezo uresničili)",
                            ),
                            (
                                "broken",
                                "PRELOMLJENA (državni organi delujejo v nasprotju z zavezo)",
                            ),
                        ],
                        verbose_name="Napredek pri uresničevanju zaveze:",
                    ),
                ),
                (
                    "summary",
                    martor.models.MartorField(
                        blank=True,
                        max_length=1100,
                        verbose_name="Kratek povzetek ugotovitev o  uresničevanju zaveze (max 1100 znakov)",
                    ),
                ),
                (
                    "notes",
                    martor.models.MartorField(
                        blank=True,
                        max_length=300,
                        verbose_name="Opombe (max 300 znakov)",
                    ),
                ),
                (
                    "demand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="zahteve.demand",
                        verbose_name="Predvolilna zaveza",
                    ),
                ),
                (
                    "responsible_state_bodies",
                    models.ManyToManyField(
                        to="zahteve.statebody",
                        verbose_name="Državni organ(i), pristojni za uresničevanje zaveze",
                    ),
                ),
            ],
            options={
                "verbose_name": "Monitoring zaveze",
                "verbose_name_plural": "Monitoring zavez",
            },
        ),
    ]
