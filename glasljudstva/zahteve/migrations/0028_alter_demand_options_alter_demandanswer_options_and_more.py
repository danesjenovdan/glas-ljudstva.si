# Generated by Django 4.1.2 on 2022-11-06 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zahteve', '0027_remove_demand_municipality_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='demand',
            options={'verbose_name': 'Vprašanje za kandidate', 'verbose_name_plural': 'Vprašanja za kandidate'},
        ),
        migrations.AlterModelOptions(
            name='demandanswer',
            options={'verbose_name': 'Odgovor kandidata_ke', 'verbose_name_plural': 'Odgovori kandidatov'},
        ),
        migrations.AlterModelOptions(
            name='election',
            options={'verbose_name': 'Volitve', 'verbose_name_plural': 'Volitve'},
        ),
        migrations.AlterModelOptions(
            name='municipality',
            options={'verbose_name': 'Občina', 'verbose_name_plural': 'Občine'},
        ),
        migrations.AlterModelOptions(
            name='party',
            options={'verbose_name': 'Kandidat_ka (ali stranka)', 'verbose_name_plural': 'Kandidati_ke (ali stranke)'},
        ),
        migrations.AlterModelOptions(
            name='voterquestion',
            options={'verbose_name': 'Vprašanje volilca_ke', 'verbose_name_plural': 'Vprašanja volilcev'},
        ),
        migrations.AlterModelOptions(
            name='workgroup',
            options={'verbose_name': 'Kategorija vprašanj za kandidate', 'verbose_name_plural': 'Kategorije vprašanj za kandidate'},
        ),
        migrations.AlterField(
            model_name='demand',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Dodaten opis'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zahteve.election', verbose_name='Volitve'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='priority_demand',
            field=models.BooleanField(default=False, verbose_name='Gre za prioritetno zahtevo? (samo za parlamentarne volitve)'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='title',
            field=models.TextField(verbose_name='Vprašanje'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='workgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='zahteve.workgroup', verbose_name='Kategorija'),
        ),
        migrations.AlterField(
            model_name='demandanswer',
            name='agree_with_demand',
            field=models.BooleanField(blank=True, null=True, verbose_name='Odgovor'),
        ),
        migrations.AlterField(
            model_name='demandanswer',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='Komentar'),
        ),
        migrations.AlterField(
            model_name='demandanswer',
            name='demand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zahteve.demand', verbose_name='Vprašanje'),
        ),
        migrations.AlterField(
            model_name='demandanswer',
            name='party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zahteve.party', verbose_name='Kandidat_ka (ali stranka)'),
        ),
        migrations.AlterField(
            model_name='election',
            name='name',
            field=models.TextField(verbose_name='Ime volitev'),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='demands',
            field=models.ManyToManyField(to='zahteve.demand', verbose_name='Vprašanja'),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-naslov'),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Grb'),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='name',
            field=models.TextField(verbose_name='Ime občine'),
        ),
        migrations.AlterField(
            model_name='party',
            name='already_has_pp',
            field=models.BooleanField(default=False, verbose_name='Je že izvajal_a PP v prejšnjem mandatu?'),
        ),
        migrations.AlterField(
            model_name='party',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zahteve.election', verbose_name='Volitve'),
        ),
        migrations.AlterField(
            model_name='party',
            name='finished_quiz',
            field=models.BooleanField(default=False, verbose_name='Je oddal_a vprašalnik? (se izpolni avtomatsko)'),
        ),
        migrations.AlterField(
            model_name='party',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Slika'),
        ),
        migrations.AlterField(
            model_name='party',
            name='is_winner',
            field=models.BooleanField(default=False, verbose_name='Je zmagal_a na volitvah?'),
        ),
        migrations.AlterField(
            model_name='party',
            name='municipality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='zahteve.municipality', verbose_name='Občina'),
        ),
        migrations.AlterField(
            model_name='party',
            name='party_name',
            field=models.TextField(blank=True, verbose_name='Ime kandidata_ke (ali stranke)'),
        ),
        migrations.AlterField(
            model_name='party',
            name='proposer',
            field=models.TextField(blank=True, verbose_name='Predlagatelj kandidata_ke'),
        ),
        migrations.AlterField(
            model_name='party',
            name='sex',
            field=models.CharField(blank=True, max_length=1, verbose_name='spol (m/f)'),
        ),
        migrations.AlterField(
            model_name='party',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Uporabnik'),
        ),
    ]
