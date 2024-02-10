from django.core.paginator import Paginator
from django.shortcuts import render

from .models import NewsItem


def landing(request):
    news = NewsItem.objects.filter(published=True).order_by("-publish_time")[:3]

    return render(request, "home/landing.html", {"news": news})


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
            "page_obj": page_obj,
            "page_range": page_range,
        },
    )


def news_item(request, id, slug=""):
    news_item = NewsItem.objects.get(id=id)

    return render(request, "home/news_item.html", {"news_item": news_item})
