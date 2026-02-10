import json
import os
import re

from django.core.management.base import BaseCommand, CommandError

from zahteve.models import Demand, Election, WorkGroup


class Command(BaseCommand):
    help = "Import list titles for 2026 demands"

    def _read_demand_list_titles_json(self):
        self.stdout.write(f"Reading demands list titles...")

        # read file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "import_2026_demand_list_titles.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    def _get_demands(self, election):
        return list(Demand.objects.filter(workgroup__election=election).order_by("id"))

    def handle(self, *args, **options):
        election = Election.objects.get(slug="drzavnozborske-volitve-2026")

        list_titles = self._read_demand_list_titles_json()
        print(len(list_titles))

        demands = self._get_demands(election)
        print(len(demands))

        for demand, list_title in zip(demands, list_titles):
            lt = list_title.strip().rstrip(".").strip()
            dt = demand.title.strip().rstrip(".").strip()

            if demand.list_title:
                print("skipped already has list title")
                print("----")
                continue

            if lt == dt:
                demand.list_title = list_title.strip()
                demand.save()
                print("same as title, saved list title")
                print("----")
                continue

            if lt != dt:
                print(lt)
                print(demand.title)
                print(demand.description)
                # print("----")
                # # wait for input("Press Enter to continue...")
                # input("Press Enter to set list title and continue...")
                demand.list_title = list_title.strip()
                demand.save()

        self.stdout.write("DONE")
