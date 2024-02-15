from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import CampaignItem, ContentPage, NewsItem


def landing(request):
    news = NewsItem.objects.filter(published=True).order_by("-publish_time")[:3]
    campaigns = CampaignItem.objects.filter(published=True, promoted=True)

    return render(
        request,
        "home/landing.html",
        {
            "news": news,
            "campaigns": campaigns,
        },
    )


def news(request):
    news = NewsItem.objects.filter(published=True).order_by("-publish_time")

    paginator = Paginator(news, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(
        number=page_obj.number,
        on_each_side=1,
        on_ends=1,
    )

    return render(
        request,
        "home/news.html",
        {
            "page_title": "Novice",
            "page_obj": page_obj,
            "page_range": page_range,
        },
    )


def news_item(request, id, slug=""):
    news_item = get_object_or_404(NewsItem, id=id, published=True)

    return render(
        request,
        "home/news_item_page.html",
        {
            "page_title": news_item.title,
            "news_item": news_item,
        },
    )


def campaigns(request):
    campaigns = CampaignItem.objects.filter(published=True)

    paginator = Paginator(campaigns, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(
        number=page_obj.number,
        on_each_side=1,
        on_ends=1,
    )

    return render(
        request,
        "home/campaigns.html",
        {
            "page_title": "Kampanje",
            "page_obj": page_obj,
            "page_range": page_range,
        },
    )


def campaign_item(request, id, slug=""):
    campaign_item = get_object_or_404(CampaignItem, id=id, published=True)

    return render(
        request,
        "home/campaign_item_page.html",
        {
            "page_title": campaign_item.title,
            "campaign_item": campaign_item,
        },
    )


def content_page(request, slug):
    content_page = get_object_or_404(ContentPage, slug=slug, published=True)

    return render(
        request,
        "home/content_page.html",
        {
            "page_title": content_page.title,
            "content_page": content_page,
        },
    )
