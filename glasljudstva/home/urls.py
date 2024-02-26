from django.urls import path
from django.views.defaults import page_not_found

from .views import campaign_item, campaigns, content_page, landing, news, news_item


def test_page_not_found(request):
    return page_not_found(request, None)


urlpatterns = [
    path("test-404/", test_page_not_found),
    path("novice/<int:id>/<slug:slug>/", news_item),
    path("novice/<int:id>/", news_item),
    path("novice/", news),
    path("kampanje/<int:id>/<slug:slug>/", campaign_item),
    path("kampanje/", campaigns),
    path("objava/<slug:slug>/", content_page),
    path("", landing),
]
