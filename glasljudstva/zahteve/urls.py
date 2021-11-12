from django.urls import include, path
from zahteve.views import landing, delovna_skupina, demand, verify_email, Registracija, RestorePasswordView


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', landing),
    path('<int:delovna_skupina_id>/', delovna_skupina),
    path('zahteve/<int:demand_id>/', demand),
    path('', include('django.contrib.auth.urls')),
    path('comments/', include('django_comments.urls')),
    path('registracija/', Registracija.as_view()),
    path('potrdi-naslov/<str:token>/', verify_email),
    path('ponastavi-geslo/<str:parameter>/', RestorePasswordView.as_view()),
    path('ponastavi-geslo/', RestorePasswordView.as_view()),

]
