from django.urls import include, path

from .views import landing, news, news_item

urlpatterns = [
    path("novice/<int:id>/<slug:slug>", news_item),
    path("novice/<int:id>/", news_item),
    path("novice/", news),
    path("", landing),
]
