from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from martor.fields import MartorFormField

from zahteve.models import WorkGroup, Demand, EmailVerification, Newsletter, Party, DemandAnswer, VoterQuestion, Election, Municipality, MonitoringReport, StateBody, DemandState

# Register your models here.
admin.site.register(WorkGroup)
admin.site.register(EmailVerification)
admin.site.register(Newsletter)
admin.site.register(VoterQuestion)
admin.site.register(StateBody)
admin.site.register(DemandState)


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
    search_fields = ['title']


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
    filter_horizontal = ('demands',)

    inlines = [
        PartyInline,
    ]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "demands":
            try:
                election = Election.objects.get(slug='lokalne-volitve-2022')
                kwargs["queryset"] = Demand.objects.filter(election=election)
            except:
                kwargs["queryset"] = Demand.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)



class MonitoringReportForm(forms.ModelForm):
    summary = MartorFormField(required=False, label="Kratek povzetek ugotovitev o  uresničevanju zaveze (max 5000 znakov)")
    notes = MartorFormField(required=False, label="Opombe (max 1000 znakov)")

    class Meta:
        model = MonitoringReport
        fields = ('__all__')


class MonitoringReportAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['demand']
    list_filter = ('demand__workgroup', 'state',)
    search_fields = ['demand__title']
    list_display = ('get_title', 'state', 'published',)

    form = MonitoringReportForm

    @admin.display(description='Ime zaveze')
    def get_title(self, obj):
        return obj.demand.title


admin.site.register(Election, ElectionAdmin)
admin.site.register(Demand, DemandAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(DemandAnswer, DemandAnswerAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(MonitoringReport, MonitoringReportAdmin)
