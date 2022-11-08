from django.db import models
from django.contrib.auth.models import User
from django.utils.http import urlencode
from django.utils.encoding import filepath_to_uri

from django_comments.moderation import CommentModerator, moderator

from zahteve.behaviors.models import Timestampable, Versionable

from zahteve.utils import id_generator


class Election(models.Model):
    name = models.TextField(verbose_name = "Ime volitev")
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Volitve'
        verbose_name_plural = 'Volitve'


class WorkGroup(Timestampable, Versionable):
    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    og_title = models.TextField(null=False, blank=False)
    og_description = models.TextField(null=False, blank=False)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    # municipality = models.ForeignKey(Municipality, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    @property
    def demands(self):
        return Demand.objects.filter(workgroup=self).order_by("?")

    class Meta:
        verbose_name = 'Kategorija vprašanj za kandidate'
        verbose_name_plural = 'Kategorije vprašanj za kandidate'


class Demand(Timestampable, Versionable):
    title = models.TextField(null=False, blank=False, verbose_name = "Vprašanje")
    description = models.TextField(null=True, blank=True, verbose_name = "Dodaten opis")
    workgroup = models.ForeignKey(
        "WorkGroup", null=True, blank=True, on_delete=models.SET_NULL, verbose_name = "Kategorija"
    )
    priority_demand = models.BooleanField(default=False, verbose_name = "Gre za prioritetno zahtevo? (samo za parlamentarne volitve)")
    election = models.ForeignKey(Election, on_delete=models.CASCADE, verbose_name = "Volitve")

    def __str__(self):
        return self.title

    @property
    def partys_which_agree(self):
        return Party.objects.filter(
            id__in=DemandAnswer.objects.filter(
                demand=self, agree_with_demand=True, party__finished_quiz=True
            ).values_list("party__id", flat=True)
        )

    @property
    def partys_which_agree_in_ids(self):
        return DemandAnswer.objects.filter(
            demand=self, agree_with_demand=True, party__finished_quiz=True
        ).values_list("party__id", flat=True)

    @property
    def partys_which_dont_agree(self):
        return Party.objects.filter(
            id__in=DemandAnswer.objects.filter(
                demand=self, agree_with_demand=False, party__finished_quiz=True
            ).values_list("party__id", flat=True)
        )

    @property
    def answers_which_dont_agree(self):
        return DemandAnswer.objects.filter(
            demand=self, agree_with_demand=False, party__finished_quiz=True
        )

    class Meta:
        verbose_name = 'Vprašanje za kandidate'
        verbose_name_plural = 'Vprašanja za kandidate'


class DemandModerator(CommentModerator):
    email_notification = False


class EmailVerification(Timestampable):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="email_verification"
    )
    verification_key = models.CharField(max_length=100)
    newsletter_permission = models.BooleanField(default=False)


class ResetPassword(Timestampable):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reset_passwords"
    )
    key = models.CharField(max_length=100)


class Newsletter(Timestampable):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    permission = models.BooleanField(default=False, blank=True)


class Municipality(models.Model):
    name = models.TextField(verbose_name = "Ime občine")
    email = models.EmailField(null=True, blank=True, verbose_name = "E-naslov")
    slug = models.SlugField(blank=True)
    image = models.ImageField(null=True, blank=True, verbose_name = "Grb")
    demands = models.ManyToManyField(Demand, verbose_name = "Vprašanja")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Občina'
        verbose_name_plural = 'Občine'


class Party(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name = "Uporabnik"
    )
    party_name = models.TextField(blank=True, verbose_name = "Ime kandidata_ke (ali stranke)")
    proposer = models.TextField(blank=True, verbose_name = "Predlagatelj kandidata_ke")
    sex = models.CharField(blank=True, max_length=1, verbose_name = "spol (m/f)")
    email = models.EmailField(null=True, blank=True)
    is_winner = models.BooleanField(default=False, verbose_name = "Je zmagal_a na volitvah?")
    finished_quiz = models.BooleanField(default=False, verbose_name = "Je oddal_a vprašalnik? (se izpolni avtomatsko)")
    image = models.ImageField(null=True, blank=True, verbose_name = "Slika")
    url = models.URLField(blank=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, verbose_name = "Volitve")
    municipality = models.ForeignKey(Municipality, null=True, on_delete=models.SET_NULL, verbose_name = "Občina")
    already_has_pp = models.BooleanField(default=False, verbose_name = "Je že izvajal_a PP v prejšnjem mandatu?")
    mautic_id = models.IntegerField(blank=True, null=True)

    @property
    def image_url(self):
        return f"https://djnd.s3.fr-par.scw.cloud/glas-ljudstva/img/{filepath_to_uri(self.party_name)}.jpg"

    def __str__(self):
        return self.party_name


    class Meta:
        verbose_name = 'Kandidat_ka (ali stranka)'
        verbose_name_plural = 'Kandidati_ke (ali stranke)'


class DemandAnswer(models.Model):
    agree_with_demand = models.BooleanField(null=True, blank=True, verbose_name = "Odgovor")
    comment = models.CharField(blank=True, default="", max_length=1024, verbose_name = "Komentar")
    party = models.ForeignKey("Party", on_delete=models.CASCADE, verbose_name = "Kandidat_ka (ali stranka)")
    demand = models.ForeignKey("Demand", on_delete=models.CASCADE, verbose_name = "Vprašanje")

    def __str__(self):
        return self.demand.title + ", " + self.party.party_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["party", "demand"], name="unique_party_demand"
            ),
        ]
        verbose_name = 'Odgovor kandidata_ke'
        verbose_name_plural = 'Odgovori kandidatov'


class VoterQuestion(models.Model):
    name = models.CharField(blank=True, max_length=50)
    hometown = models.CharField(max_length=50)
    receiver = models.CharField(max_length=120)
    question = models.CharField(max_length=500)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Vprašanje volilca_ke'
        verbose_name_plural = 'Vprašanja volilcev'

moderator.register(Demand, DemandModerator)
