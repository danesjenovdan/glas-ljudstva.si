from django.urls import include, path
from zahteve.views import landing, delovna_skupina, demand

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', landing),
    path('<int:delovna_skupina_id>/', delovna_skupina),
    path('zahteve/<int:demand_id>/', demand),
]
