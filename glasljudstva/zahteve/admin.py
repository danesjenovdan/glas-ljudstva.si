from django.contrib import admin

from django.contrib.auth.models import User

from zahteve.models import WorkGroup, Demand, EmailVerification, Newsletter, Party, DemandAnswer, VoterQuestion, Election

# Register your models here.
admin.site.register(WorkGroup)
admin.site.register(Demand)
admin.site.register(EmailVerification)
admin.site.register(Newsletter)
admin.site.register(Party)
admin.site.register(DemandAnswer)
admin.site.register(VoterQuestion)


# normalen inline ne dela, ker bi User moral imet foreign key na Party
# class UserInline(admin.StackedInline):
#     model = User
#     max_num = 1

# class PartyAdmin(admin.ModelAdmin):
#     inlines = [UserInline]

# admin.site.register(Party, PartyAdmin)


class PartyInline(admin.StackedInline):
    model = Party
    extra = 1


class DemandInline(admin.StackedInline):
    model = Demand
    extra = 1


class ElectionAdmin(admin.ModelAdmin):
    inlines = [
        PartyInline,
        DemandInline,
    ]

admin.site.register(Election, ElectionAdmin)
