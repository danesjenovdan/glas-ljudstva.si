from django.db import models
from django.contrib.auth.models import User

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


class Demand(Timestampable, Versionable):
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    workgroup = models.ForeignKey('WorkGroup', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class DemandModerator(CommentModerator):
    email_notification = False


class EmailVerification(Timestampable):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='email_verification'
    )
    verification_key = models.CharField(max_length=100)
    newsletter_permission = models.BooleanField(default=False)


class ResetPassword(Timestampable):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reset_passwords'
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
    finished_quiz = models.BooleanField(default=False)

    def  __str__(self):
        return self.user.first_name


class DemandAnswer(models.Model):
    agree_with_demand = models.BooleanField(null=True, blank=True)
    comment = models.CharField(blank=True, default='', max_length=1024)
    party = models.ForeignKey('Party', on_delete=models.CASCADE)
    demand = models.ForeignKey('Demand', on_delete=models.CASCADE)

    def __str__(self):
        return self.demand.title + ", " + self.party.user.first_name

    class Meta:    
        constraints = [
            models.UniqueConstraint(fields= ['party', 'demand'], name='unique_party_demand'),
        ]


moderator.register(Demand, DemandModerator)
