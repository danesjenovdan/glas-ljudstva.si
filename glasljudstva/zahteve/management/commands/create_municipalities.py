from django.core.management.base import BaseCommand, CommandError
from zahteve.models import Municipality

MUNICIPALITIES = [
    "Ajdovščina",
    "Beltinci",
    "Bled",
    "Bohinj",
    "Borovnica",
    "Bovec",
    "Brda",
    "Brezovica",
    "Brežice",
    "Tišina",
    "Celje",
    "Cerklje na Gorenjskem",
    "Cerknica",
    "Cerkno",
    "Črenšovci",
    "Črna na Koroškem",
    "Črnomelj",
    "Destrnik",
    "Divača",
    "Dobrepolje",
    "Dobrova – Polhov Gradec",
    "Dol pri Ljubljani",
    "Domžale",
    "Dornava",
    "Dravograd",
    "Duplek",
    "Gorenja vas – Poljane",
    "Gorišnica",
    "Gornja Radgona",
    "Gornji Grad",
    "Gornji Petrovci",
    "Grosuplje",
    "Šalovci",
    "Hrastnik",
    "Hrpelje – Kozina",
    "Idrija",
    "Ig",
    "Ilirska Bistrica",
    "Ivančna Gorica",
    "Izola",
    "Jesenice",
    "Juršinci",
    "Kamnik",
    "Kanal",
    "Kidričevo",
    "Kobarid",
    "Kobilje",
    "Kočevje",
    "Komen",
    "Koper",
    "Kozje",
    "Kranj",
    "Kranjska Gora",
    "Krško",
    "Kungota",
    "Kuzma",
    "Laško",
    "Lenart",
    "Lendava",
    "Litija",
    "Ljubljana",
    "Ljubno",
    "Ljutomer",
    "Logatec",
    "Loška dolina",
    "Loški Potok",
    "Luče",
    "Lukovica",
    "Majšperk",
    "Maribor",
    "Medvode",
    "Mengeš",
    "Metlika",
    "Mežica",
    "Miren – Kostanjevica",
    "Mislinja",
    "Moravče",
    "Moravske Toplice",
    "Mozirje",
    "Murska Sobota",
    "Muta",
    "Naklo",
    "Nazarje",
    "Nova Gorica",
    "Novo mesto",
    "Odranci",
    "Ormož",
    "Osilnica",
    "Pesnica",
    "Piran",
    "Pivka",
    "Podčetrtek",
    "Podvelka",
    "Postojna",
    "Preddvor",
    "Ptuj",
    "Puconci",
    "Rače – Fram",
    "Radeče",
    "Radenci",
    "Radlje ob Dravi",
    "Radovljica",
    "Ravne na Koroškem",
    "Ribnica",
    "Rogašovci",
    "Rogaška Slatina",
    "Rogatec",
    "Ruše",
    "Semič",
    "Sevnica",
    "Sežana",
    "Slovenj Gradec",
    "Slovenska Bistrica",
    "Slovenske Konjice",
    "Starše",
    "Sveti Jurij ob Ščavnici",
    "Šenčur",
    "Šentilj",
    "Šentjernej",
    "Šentjur",
    "Škocjan",
    "Škofja Loka",
    "Škofljica",
    "Šmarje pri Jelšah",
    "Šmartno ob Paki",
    "Šoštanj",
    "Štore",
    "Tolmin",
    "Trbovlje",
    "Trebnje",
    "Tržič",
    "Turnišče",
    "Velenje",
    "Velike Lašče",
    "Videm",
    "Vipava",
    "Vitanje",
    "Vodice",
    "Vojnik",
    "Vrhnika",
    "Vuzenica",
    "Zagorje ob Savi",
    "Zavrč",
    "Zreče",
    "Železniki",
    "Žiri",
    "Benedikt",
    "Bistrica ob Sotli",
    "Bloke",
    "Braslovče",
    "Cankova",
    "Cerkvenjak",
    "Dobje",
    "Dobrna",
    "Dobrovnik",
    "Dolenjske Toplice",
    "Grad",
    "Hajdina",
    "Hoče – Slivnica",
    "Hodoš",
    "Horjul",
    "Jezersko",
    "Komenda",
    "Kostel",
    "Križevci",
    "Lovrenc na Pohorju",
    "Markovci",
    "Miklavž na Dravskem polju",
    "Mirna Peč",
    "Oplotnica",
    "Podlehnik",
    "Polzela",
    "Prebold",
    "Prevalje",
    "Razkrižje",
    "Ribnica na Pohorju",
    "Selnica ob Dravi",
    "Sodražica",
    "Solčava",
    "Sveta Ana",
    "Sveti Andraž v Slovenskih goricah",
    "Šempeter – Vrtojba",
    "Tabor",
    "Trnovska vas",
    "Trzin",
    "Velika Polana",
    "Veržej",
    "Vransko",
    "Žalec",
    "Žetale",
    "Žirovnica",
    "Žužemberk",
    "Šmartno pri Litiji",
    "Apače",
    "Cirkulane",
    "Kostanjevica na Krki",
    "Makole",
    "Mokronog – Trebelno",
    "Poljčane",
    "Renče – Vogrsko",
    "Središče ob Dravi",
    "Straža",
    "Sveta Trojica v Slovenskih goricah",
    "Sveti Tomaž",
    "Šmarješke Toplice",
    "Gorje",
    "Log – Dragomer",
    "Rečica ob Savinji",
    "Sveti Jurij v Slovenskih goricah",
    "Šentrupert",
    "Mirna",
    "Ankaran",
]

class Command(BaseCommand):
    help = 'Create municipality objects'

    def handle(self, *args, **options):
        self.stdout.write(f'Creating {len(MUNICIPALITIES)} municipalities...')
        for municipality in MUNICIPALITIES:
            Municipality.objects.create(name=municipality)
        self.stdout.write('DONE')