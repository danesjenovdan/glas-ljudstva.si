from django.urls import include, path
from zahteve.views import (
    landing,
    delovna_skupina,
    demand,
    demands_party,
    verify_email,
    Registracija,
    RestorePasswordView,
    after_registration,
    party,
    PartyDemand,
    party_instructions,
    party_finish,
    party_save,
    party_summary
)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', landing),
    path('<int:delovna_skupina_id>/', delovna_skupina),
    path('zahteve/<int:demand_id>/', demand),
    path('zahteve/stranka/<int:party_id>/', demands_party),
    path('zahteve/', landing),
    path('', include('django.contrib.auth.urls')),
    path('comments/', include('django_comments.urls')),
    path('registracija/', Registracija.as_view()),
    path('potrdi-naslov/<str:token>/', verify_email),
    path('ponastavi-geslo/<str:parameter>/', RestorePasswordView.as_view()),
    path('ponastavi-geslo/', RestorePasswordView.as_view()),
    path('hvala/', after_registration),
    path('stranke/', party),
    path('stranke/<int:category_id>/', PartyDemand.as_view()),
    path('stranke/navodila/', party_instructions),
    path('stranke/oddaja/', party_finish),
    path('stranke/oddaj/', party_save),
    path('stranke/povzetek/', party_summary)
]
