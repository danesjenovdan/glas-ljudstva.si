from django.db import models
from django.contrib.auth.models import User
from django.utils.http import urlencode
from django.utils.encoding import filepath_to_uri

from django_comments.moderation import CommentModerator, moderator

from zahteve.behaviors.models import Timestampable, Versionable

from zahteve.utils import id_generator


class WorkGroup(Timestampable, Versionable):
    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    og_title = models.TextField(null=False, blank=False)
    og_description = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.name

    @property
    def demands(self):
        return Demand.objects.filter(workgroup=self).order_by("?")


class Demand(Timestampable, Versionable):
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    workgroup = models.ForeignKey(
        "WorkGroup", null=True, blank=True, on_delete=models.SET_NULL
    )
    priority_demand = models.BooleanField(default=False)

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


class Party(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    party_name = models.TextField(blank=True)
    finished_quiz = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)
    url = models.URLField(blank=True)

    @property
    def image_url(self):
        return f"https://djnd.s3.fr-par.scw.cloud/glas-ljudstva/img/{filepath_to_uri(self.party_name)}.jpg"

    def __str__(self):
        return self.party_name


class DemandAnswer(models.Model):
    agree_with_demand = models.BooleanField(null=True, blank=True)
    comment = models.CharField(blank=True, default="", max_length=1024)
    party = models.ForeignKey("Party", on_delete=models.CASCADE)
    demand = models.ForeignKey("Demand", on_delete=models.CASCADE)

    def __str__(self):
        return self.demand.title + ", " + self.party.party_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["party", "demand"], name="unique_party_demand"
            ),
        ]


class VoterQuestion(models.Model):
    name = models.CharField(blank=True, max_length=50)
    hometown = models.CharField(max_length=50)
    receiver = models.CharField(max_length=120)
    question = models.CharField(max_length=500)

    def __str__(self):
        return self.question


moderator.register(Demand, DemandModerator)
