from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from zahteve.models import DemandState

STATES = [
    {"name": "IZPOLNJENA", "description": "zaveza je v celoti uresničena", "order": 4},
    {
        "name": "DELNO IZPOLNJENA",
        "description": "nekateri elementi zaveze so uresničeni",
        "order": 3,
    },
    {"name": "V IZVAJANJU", "description": "delo še poteka", "order": 2},
    {
        "name": "ZASTALA",
        "description": "poskusi uresničevanja so bili neuspešni",
        "order": 5,
    },
    {
        "name": "NEDOTAKNJENA",
        "description": "sploh ni prizadevanj ali poskusov, da bi zavezo uresničili",
        "order": 1,
    },
    {
        "name": "PRELOMLJENA",
        "description": "državni organi delujejo v nasprotju z zavezo",
        "order": 6,
    },
]


class Command(BaseCommand):
    help = "Create state body objects"

    def handle(self, *args, **options):
        self.stdout.write(f"Creating {len(STATES)} monitoring report states ...")
        for state in STATES:
            s, created = DemandState.objects.get_or_create(name=state["name"])
            s.description = state["description"]
            s.order = state["order"]
            s.save()
        self.stdout.write("DONE")
