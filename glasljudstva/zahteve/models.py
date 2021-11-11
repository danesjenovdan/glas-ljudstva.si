from django.db import models

from zahteve.behaviors.models import Timestampable, Versionable

# Create your models here.
class WorkGroup(Timestampable, Versionable):
    name = models.TextField(null=False, blank=False)


class Demand(Timestampable, Versionable):
    title = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    workgroup = models.ForeignKey('WorkGroup', null=True, blank=True, on_delete=models.SET_NULL)
