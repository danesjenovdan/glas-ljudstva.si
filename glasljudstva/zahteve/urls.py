from django.urls import include, path
from zahteve.views import landing, delovna_skupina

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', landing),
    path('<int:delovna_skupina_id>/', delovna_skupina),
]
