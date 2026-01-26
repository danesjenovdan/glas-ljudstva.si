import os
import re

from django.core.management.base import BaseCommand, CommandError

from zahteve.models import Demand, Election, WorkGroup


class Command(BaseCommand):
    help = "Create demands for 2026 parliamentary elections"

    def _read_demands_markdown(self):
        self.stdout.write(f"Reading demands...")

        # read file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "import_2026_demands.md")
        with open(file_path, "r", encoding="utf-8") as f:
            content_lines = f.readlines()

        # parse workgroups and demands text
        workgroups = []
        for line in content_lines:
            if line.startswith("**") and not line[2].isdigit():
                wg_name = line.strip().replace("**", "").strip()
                workgroups.append({"name": wg_name, "demands": []})
                continue

            if line.startswith("**") and line[2].isdigit():
                demand_name = line.strip().replace("**", "").strip()
                demand_name = demand_name.replace("\\", "")
                demand_name = re.sub(r"^\d+\.\s*", "", demand_name).strip()
                workgroups[-1]["demands"].append(
                    {"name": demand_name, "description": ""}
                )
                continue

            if workgroups and workgroups[-1]["demands"]:
                workgroups[-1]["demands"][-1]["description"] += line

        for wg in workgroups:
            for demand in wg["demands"]:
                demand["description"] = demand["description"].strip()

        # split demand text first level list in to seperate demands
        new_workgroups = []
        for wg in workgroups:
            wg_name = wg["name"]
            new_demands = []
            for demand in wg["demands"]:
                demand_name = demand["name"]
                demand_description = demand["description"]

                description_lines = demand_description.splitlines()
                first_line = description_lines[0] if description_lines else ""
                if re.match(r"^\d+\.\s+", first_line):
                    multiple_demands = True
                else:
                    multiple_demands = False

                if multiple_demands:
                    list_char = "a"
                    for line in description_lines:
                        if re.match(r"^\d+\.\s+", line):
                            # New demand found
                            demand_text = re.sub(r"^\d+\.\s+", "", line).strip()
                            new_demands.append(
                                {
                                    "name": demand_name + " (" + list_char + ")",
                                    "description": demand_text + "\n",
                                }
                            )
                            list_char = chr(ord(list_char) + 1)
                        else:
                            if new_demands:
                                new_demands[-1]["description"] += line + "\n"
                else:
                    # if no demands yet just copy the demand
                    new_demands.append(
                        {"name": demand_name, "description": demand_description}
                    )

            new_workgroups.append({"name": wg_name, "demands": new_demands})
        workgroups = new_workgroups

        # add empty line before and after lists that start with an asterish
        new_workgroups = []
        for wg in workgroups:
            wg_name = wg["name"]
            new_demands = []
            for demand in wg["demands"]:
                demand_name = demand["name"]
                demand_description = demand["description"]

                description_lines = demand_description.splitlines()
                modified_description_lines = []
                for i, line in enumerate(description_lines):
                    if re.match(r"^\s*\*\s+", line):
                        if i > 0 and not re.match(
                            r"^\s*\*\s+", description_lines[i - 1]
                        ):
                            modified_description_lines.append("")
                        modified_description_lines.append(line)
                    else:
                        if i > 0 and re.match(r"^\s*\*\s+", description_lines[i - 1]):
                            modified_description_lines.append("")
                        modified_description_lines.append(line)

                new_description = "\n".join(modified_description_lines).strip()
                new_demands.append(
                    {"name": demand_name, "description": new_description}
                )

            new_workgroups.append({"name": wg_name, "demands": new_demands})
        workgroups = new_workgroups

        return workgroups

    def _save_demands(self, election, demands_dict):
        for wg_i, wg_dict in enumerate(demands_dict):
            wg_name = wg_dict["name"]
            wg_exists = WorkGroup.objects.filter(
                name=wg_name,
                election=election,
            ).exists()
            if wg_exists:
                self.stdout.write(f'Workgroup "{wg_name}" already exists')
                wg_obj = WorkGroup.objects.get(
                    name=wg_name,
                    election=election,
                )
            else:
                wg_obj = WorkGroup.objects.create(
                    name=wg_name,
                    description="",
                    og_title="",
                    og_description="",
                    election=election,
                    order=wg_i + 1,
                )
                self.stdout.write(f'Created workgroup "{wg_name}"')

            for demand_dict in wg_dict["demands"]:
                demand_name = demand_dict["name"]
                demand_description = demand_dict["description"]
                demand_exists = Demand.objects.filter(
                    title=demand_name,
                    election=election,
                ).exists()
                if demand_exists:
                    self.stdout.write(f'  Demand "{demand_name}" already exists')
                else:
                    Demand.objects.create(
                        title=demand_name,
                        description=demand_description,
                        workgroup=wg_obj,
                        election=election,
                    )
                    self.stdout.write(f'  Created demand "{demand_name}"')

    def handle(self, *args, **options):
        election = Election.objects.get(slug="drzavnozborske-volitve-2026")

        demands_dict = self._read_demands_markdown()
        self._save_demands(election, demands_dict)

        self.stdout.write("DONE")
