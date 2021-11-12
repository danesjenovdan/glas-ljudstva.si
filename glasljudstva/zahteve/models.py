from django.db import models
from django.contrib.auth.models import User

from django_comments.moderation import CommentModerator, moderator

from zahteve.behaviors.models import Timestampable, Versionable

from zahteve.utils import id_generator

class WorkGroup(Timestampable, Versionable):
    name = models.TextField(null=False, blank=False)


class Demand(Timestampable, Versionable):
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    workgroup = models.ForeignKey('WorkGroup', null=True, blank=True, on_delete=models.SET_NULL)


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

moderator.register(Demand, DemandModerator)
