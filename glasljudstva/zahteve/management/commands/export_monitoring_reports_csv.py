import csv

from django.core.management.base import BaseCommand

from zahteve.models import YES_NO_PARTIALLY_OPTIONS, MonitoringReport


class Command(BaseCommand):
    help = "Export monitoring reports to CSV"

    def handle(self, *args, **kwargs):
        self.stdout.write("Exporting monitoring reports to CSV...")

        row_headers = [
            "id",
            "created_at",
            "updated_at",
            "demand.title",
            "responsible_state_bodies",
            "present_in_coalition_treaty",
            "cooperative",
            "state",
            "summary",
            "notes",
            "published",
        ]
        rows = []

        monitoring_reports = MonitoringReport.objects.all()
        for report in monitoring_reports:

            demand_title = str(report.demand) if report.demand else None
            demand_state = str(report.state) if report.state else None
            responsible_state_bodies = (
                "\n".join([str(body) for body in report.responsible_state_bodies.all()])
                if report.responsible_state_bodies.exists()
                else None
            )

            yes_no_partially_dict = dict(YES_NO_PARTIALLY_OPTIONS)
            present_in_coalition_treaty = (
                yes_no_partially_dict.get(report.present_in_coalition_treaty, None)
                if report.present_in_coalition_treaty
                else None
            )
            cooperative = (
                yes_no_partially_dict.get(report.cooperative, None)
                if report.cooperative
                else None
            )

            rows.append(
                [
                    report.id,
                    report.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    report.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    demand_title,
                    responsible_state_bodies,
                    present_in_coalition_treaty,
                    cooperative,
                    demand_state,
                    report.summary,
                    report.notes,
                    "Da" if report.published else "Ne",
                ]
            )

        with open("monitoring_reports.csv", "w", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row_headers)
            writer.writerows(rows)
        self.stdout.write("CSV file 'monitoring_reports.csv' created successfully.")

        self.stdout.write("Monitoring reports exported successfully.")
