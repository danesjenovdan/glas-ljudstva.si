from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from zahteve.models import StateBody

STATE_BODIES = [
    "Ministrstvo za finance",
    "Ministrstvo za notranje zadeve",
    "Ministrstvo za zunanje in evropske zadeve",
    "Ministrstvo za obrambo",
    "Ministrstvo za pravosodje",
    "Ministrstvo za javno upravo",
    "Ministrstvo za zdravje",
    "Ministrstvo za solidarno prihodnost",
    "Ministrstvo za okolje, podnebje in energijo",
    "Ministrstvo za vzgojo in izobraževanje",
    "Ministrstvo za visoko šolstvo, znanost in inovacije",
    "Ministrstvo za gospodarstvo, turizem in šport",
    "Ministrstvo za kulturo",
    "Ministrstvo za kmetijstvo, gozdarstvo in prehrano",
    "Ministrstvo za delo, družino, socialne zadeve in enake možnosti",
    "Ministrstvo za infrastrukturo",
    "Ministrstvo za naravne vire in prostor",
    "Ministrstvo za kohezijo in regionalni razvoj",
    "Ministrstvo za digitalno preobrazbo",
    "Ministrstvo za okolje in prostor",
    "Ministrstvo za gospodarski razvoj in tehnologijo",
    "Ministrstvo za infrastrukturo",
    "Ministrstvo za izobraževanje, znanost in šport",
    "Generalni sekretariat vlade RS",
    "Sekretariat državnega zbora RS",
    "Urad vlade za komuniciranje",
    "Služba vlade RS za digitalno preobrazbo",
]


class Command(BaseCommand):
    help = "Create state body objects"

    def handle(self, *args, **options):
        self.stdout.write(f"Creating {len(STATE_BODIES)} state bodies ...")
        for stateBody in STATE_BODIES:
            sb, created = StateBody.objects.get_or_create(name=stateBody)
            sb.save()
        self.stdout.write("DONE")
