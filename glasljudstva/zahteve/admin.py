from django.contrib import admin

from zahteve.models import WorkGroup, Demand, EmailVerification, Newsletter

# Register your models here.
admin.site.register(WorkGroup)
admin.site.register(Demand)
admin.site.register(EmailVerification)
admin.site.register(Newsletter)
