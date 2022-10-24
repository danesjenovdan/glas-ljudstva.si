from django.contrib import admin

from django.contrib.auth.models import User

from zahteve.models import WorkGroup, Demand, EmailVerification, Newsletter, Party, DemandAnswer, VoterQuestion, Election, Municipality

# Register your models here.
admin.site.register(WorkGroup)
admin.site.register(EmailVerification)
admin.site.register(Newsletter)
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


class PartyAdmin(admin.ModelAdmin):
    list_display = ('party_name', 'election', 'finished_quiz')
    list_filter = ('election', )


class DemandAdmin(admin.ModelAdmin):
    list_display = ('title', 'election')
    list_filter = ('election', )


class DemandAnswerAdmin(admin.ModelAdmin):
    list_display = ('get_demand_title', 'get_election', 'party')
    list_filter = ('demand__election', )

    def get_election(self, obj):
        return obj.demand.election
    get_election.admin_order_field  = 'demand'  # Allows column order sorting
    get_election.short_description = 'Election'  # Renames column head

    def get_demand_title(self, obj):
        return str(obj.demand.title)[:60] + '...' if len(str(obj.demand.title)) > 60 else str(obj.demand.title)
    get_demand_title.admin_order_field  = 'demand'
    get_demand_title.short_description = 'Demand'


class ElectionAdmin(admin.ModelAdmin):
    inlines = [
        PartyInline,
        DemandInline,
    ]


class MunicipalityAdmin(admin.ModelAdmin):
    inlines = [
        PartyInline,
        DemandInline,
    ]


admin.site.register(Election, ElectionAdmin)
admin.site.register(Demand, DemandAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(DemandAnswer, DemandAnswerAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
