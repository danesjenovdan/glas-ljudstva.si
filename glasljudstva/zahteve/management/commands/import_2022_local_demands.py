import csv
from io import StringIO

from django.core.management.base import BaseCommand, CommandError
from zahteve.models import Demand, Election, Municipality

DEMANDS = """Občina bi morala uvesti participativni proračun v višini najmanj 1 % občinskega proračuna.,vse
Na občinskem spletnem mestu bi morali biti po vsaki seji občinskega sveta objavljeni poimenski rezultati glasovanj posameznih svetnic in svetnikov.,vse
Občina bi morala aktivno varovati kmetijska zemljišča in ne bo spreminjala njihove namembnosti.,vse
"Četudi občina financira lokalni medij, ne bi smela imeti vpliva na njegovo uredniško politiko.",vse
"Občina bi morala na svojem spletnem mestu transparentno, pregledno in ažurno objavljati rezultate vseh javnih razpisov in naročil, prejemnike javnih sredstev ter višino dodeljenih sredstev.",vse
"Občina bi morala skrbeti za obveščanje prebivalstva o problematiki v njej živečih ranljivih skupin (kot so na primer starejši, pripadniki LGBTQ+ skupnosti, avtistični otroci, tujci …) ter za sprejemanje in solidarnost do njih. To bi morala početi tudi s pomočjo ponekod že razvitih praks, kot so na primer sveti za vključevanje, delovne skupine itd.",vse
Občina bi morala zagotoviti zadostne kapacitete za nastanitev starejših občanov. ,vse
"Občina bi morala sistemsko podpirati delovanje organizacij civilne družbe in različne programe (prostovoljske, socialnovarstvene, medgeneracijske, mladinske itd.), na primer z zagotavljanjem brezplačnih prostorov ali kritjem stroškov prostovoljcev.",vse
"Občina bi morala sodelovati v programu Zero Waste, ki narekuje izdelavo in uporabo samo takšnih izdelkov, ki jih je mogoče dolgo uporabljati, predelati, reciklirati in ponovno uporabiti. ",vse
"Občina bi morala aktivno sodelovati pri vzpostavljanju oz. sistemskem podpiranju organizacij, ki pomagajo žrtvam nasilja. ",vse
"Občina bi morala aktivno spodbujati, podpirati in omogočati različne dejavnosti LGBTQ+ skupnosti.",vse
"Občina bi morala na svojem spletnem mestu javno objavljati redno posodobljen seznam vseh lobističnih stikov župana oz. županje, občinskih svetnic in svetnikov ter vseh drugih občinskih funkcionark in funkcionarjev.",vse
"Občina bi morala javno objavljati redno posodobljen seznam vseh subjektov, s katerimi veljajo omejitve poslovanja občine zaradi sorodstvenih, poslovnih in drugih vezi občinskih funkcionark in fukcionarjev. ",vse
"Občina bi morala zagotavljati ustrezne stanovanjske kapacitete za mlade, mlade družine ter ostale prebivalke in prebivalce.",vse
Občina bi morala ustrezno zaščititi žvižgače ter vzpostaviti ustrezne mehanizme za anonimno prijavo nepravilnosti pri njenem delovanju.,vse
"Občina bi morala spoštovati obstoječe avtonomne prostore, ki ob spoštovanju drugih izražajo alternativne družbene, kulturne ali ekonomske prakse, ter spodbujati vzpostavljanje novih tovrstnih prostorov.",vse
Občina bi morala nadzorovati število turistov v naravnih območjih in ne povečevati turističnih kapacitet na račun kakovosti bivanja občank in občanov ter varovanja narave.,vse
"Občina bi moral poskrbeti, da bodo imeli prebivalci in prebivalke na voljo učinkovit in vsem dostopen javni prevoz. ",vse
"Občina bi morala poskrbeti, da se javno razsvetljavo na območju občine v čim večji meri omeji in tako varčuje z energijo.","Ljubljana, Maribor, Kranj, Koper, Celje, Novo mesto, Velenje, Nova Gorica, Krško, Ptuj, Murska Sobota, Slovenj Gradec"
Občina bi morala aktivno pristopiti k vzpostavljanju projekta najemne stanovanjske zadruge.,"Ljubljana, Maribor, Kranj, Koper, Celje, Novo mesto, Velenje, Nova Gorica, Krško, Ptuj, Murska Sobota, Slovenj Gradec"
"Občina bi morala aktivno vzpostavljati dialog z romsko skupnostjo in zagotavljati pogoje za izboljšanje razmer njihovega bivanja, zaposlovanja, šolanja, zdravstvenega varstva, informiranja in drugih področij integracije. V pripravo in sprejemanje politik ter ukrepov na občinski ravni bi morala vključevati predstavnice in predstavnike romske skupnosti in si aktivno prizadevati za zaposlovanje Romov na delovnih mestih v občinskih ustanovah in podjetjih.","Beltinci, Cankova, Črenšovci, Črnomelj, Dobrovnik, Grosuplje, Kočevje, Krško, Kuzma, Lendava, Metlika, Murska Sobota, Novo mesto, Puconci, Rogašovci, Semič, Šentjernej, Tišina, Trebnje, Turnišče, Ljubljana, Maribor, Velenje"
Občina bi morala negovati 144-letno tradicijo organiziranega glasbenega šolstva na Ptuju ter najti ustrezno dolgoročno rešitev prostorske stiske ene od največjih glasbenih šol v Sloveniji – Glasbene šole Karol Pahor Ptuj.,Ptuj
"Občina bi se morala aktivno zavzemati za vzpostavitev večjega in stalnega razstavišča Pokrajinskega muzeja Ptuj-Ormož, da bodo lahko bogate arheološke zbirke po dobrem desetletju ponovno na ogled javnosti.",Ptuj
Občina bi morala opraviti  analizo uporabe geotermalnih voda kot trajnostnega vira energije.,Ptuj
Občina ne bi smela sekati odraslih zdravih dreves v urbanih središčih.,Ptuj
Občina bi morala vzpostaviti program za zdravljenje t. i. nekemične zasvojenosti – zasvojenosti z zasloni – za otroke in mladostnike.,Ptuj
Občina bi morala spodbujati trajnostno mobilnost v obliki vzpostavitve novih postaj in nabave novih kakovostnih koles v okviru sistema izposoje Pecikl.,Ptuj
Občina bi morala pred ponovnim sprejemom Odloka o občinskem prostorskem načrtu sprejeti strategijo razvoja in v njej določiti cilje dolgoročnega prostorskega razvoja.,Izola
"Občina bi morala povečati sredstva za izvajanje kulturnih programov, ki so trenutno finančno podhranjeni.",Izola
"Komunala Izola d. o. o. bi morala prenehati opravljati tržno dejavnost zbiranja, prevzema in predelave gradbenih odpadkov.",Izola
"Občina bi morala ukreniti vse, kar je v njeni pristojnosti, da prednostno poskrbi za zagotovitev stanovanj lokalnemu prebivalstvu.",Izola
"Občina bi morala zagotovili, da bodo imele krajevne skupnosti večjo moč odločanja pri investicijah in projektih na njihovem območju.",Cerkno
Občina bi morala podpirati in subvencionirati nakupe malih čistilnih naprav.,Cerkno
"Občina bi morala povečati sredstva, namenjena za modernizacijo in vzdrževanje cest, saj so ta trenutno prenizka.",Cerkno
Občina bi morala urediti in komunalno opremiti zazidljive parcele za stanovanjske stavbe ter jih prodati lokalnim interesentom po stroškovni in ne tržni ceni.,Cerkno
"Občina bi morala zgraditi stanovanjski blok, ki bo na voljo mladim družinam.",Cerkno
"Občina bi morala poskrbeti za zadostno število stanovanj in primernih služb, ki bi mlade odvrnile od izseljevanja.",Cerkno
"Občina mora poskrbeti za drugo lokacijo za novo zdravstveno postajo, saj je trenutno predvidena lokacija (bivša uprava tovarne ETA) neprimerna.",Cerkno
"Občina bi morala več sredstev nameniti okoliškim vasem, saj jih trenutno preveč nameni kraju Cerkno.",Cerkno
"Občina bi morala zaposliti osebo, ki bo zadolžena za pridobivanje sredstev iz EU.",Cerkno
"""


class Command(BaseCommand):
    help = "Create demands for 2022 local elections and link them with municipalities"

    def handle(self, *args, **options):
        election = Election.objects.get(slug="lokalne-volitve-2022")

        self.stdout.write(f"Creating and linking demands with municipalities...")
        f = StringIO(DEMANDS)
        reader = csv.reader(f)
        for row in reader:
            demand = row[0]
            obcine_string = row[1] or "vse"
            obcine = list(map(lambda x: x.strip(), obcine_string.split(",")))

            self.stdout.write(f'Creating demand "{demand[:80]}"...')
            obj = Demand.objects.create(
                title=demand,
                election=election,
            )
            if obcine == ["vse"]:
                municipalities = Municipality.objects.all()
                for m in municipalities:
                    self.stdout.write(f'Linking with "{m.name}"...')
                    m.demands.add(obj)
                    m.save()
            else:
                for obcina in obcine:
                    m = Municipality.objects.get(name=obcina)
                    self.stdout.write(f'Linking with "{m.name}"...')
                    m.demands.add(obj)
                    m.save()

            self.stdout.write("---")

        self.stdout.write("DONE")
