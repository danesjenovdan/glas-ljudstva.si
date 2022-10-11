from django.urls import include, path
from zahteve.views import (
    landing,
    delovna_skupina,
    demand,
    demands_party,
    faq,
    verify_email,
    Registracija,
    RestorePasswordView,
    after_registration,
    party,
    PartyDemand,
    party_instructions,
    party_finish,
    party_save,
    party_summary,
    open_party_summary,
    Volitvomat
)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', landing),
    
    path('<int:delovna_skupina_id>/', delovna_skupina),
    path('zahteve/<int:demand_id>/', demand),
    path('zahteve/stranka/<int:party_id>/', demands_party),
    path('zahteve/', landing),
    path('pogosta-vprasanja/', faq),
    
    path('', include('django.contrib.auth.urls')),
    path('comments/', include('django_comments.urls')),
    path('registracija/', Registracija.as_view()),
    path('potrdi-naslov/<str:token>/', verify_email),
    path('ponastavi-geslo/<str:parameter>/', RestorePasswordView.as_view()),
    path('ponastavi-geslo/', RestorePasswordView.as_view()),
    path('hvala/', after_registration),

    path('<slug:election_slug>/', landing),
    path('<slug:election_slug>/zahteve/', landing),
    
    # URLS for candidates, twice. this is just cosmetics
    # first for parties
    path('<slug:election_slug>/stranke/', party),
    path('<slug:election_slug>/stranke/<int:category_id>/', PartyDemand.as_view()),
    path('<slug:election_slug>/stranke/navodila/', party_instructions),
    path('<slug:election_slug>/stranke/oddaja/', party_finish),
    path('<slug:election_slug>/stranke/oddaj/', party_save),
    path('<slug:election_slug>/stranke/povzetek/', party_summary),
    path('<slug:election_slug>/stranke/povzetek/<int:party_id>/', open_party_summary),
    # then for individual candidates
    path('<slug:election_slug>/kandidati_ke/', party),
    path('<slug:election_slug>/kandidati_ke/<int:category_id>/', PartyDemand.as_view()),
    path('<slug:election_slug>/kandidati_ke/navodila/', party_instructions),
    path('<slug:election_slug>/kandidati_ke/oddaja/', party_finish),
    path('<slug:election_slug>/kandidati_ke/oddaj/', party_save),
    path('<slug:election_slug>/kandidati_ke/povzetek/', party_summary),

    path('<int:election_id>/api/volitvomat/', Volitvomat.as_view()),
    path('api/volitvomat/', Volitvomat.as_view()),
]
