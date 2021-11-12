from django.db import models

from django_comments.moderation import CommentModerator, moderator

from zahteve.behaviors.models import Timestampable, Versionable

# Create your models here.
class WorkGroup(Timestampable, Versionable):
    name = models.TextField(null=False, blank=False)


class Demand(Timestampable, Versionable):
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    workgroup = models.ForeignKey('WorkGroup', null=True, blank=True, on_delete=models.SET_NULL)


class DemandModerator(CommentModerator):
    email_notification = False

moderator.register(Demand, DemandModerator)
