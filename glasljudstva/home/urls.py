from django.urls import path
from django.views.defaults import page_not_found

from .views import content_page, landing, news, news_item


def test_page_not_found(request):
    return page_not_found(request, None)


urlpatterns = [
    path("test-404/", test_page_not_found),
    path("novice/<int:id>/<slug:slug>/", news_item),
    path("novice/<int:id>/", news_item),
    path("novice/", news),
    path("<slug:slug>/", content_page),
    path("", landing),
]
