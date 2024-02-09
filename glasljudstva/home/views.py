from django.shortcuts import render

from .models import NewsItem


def landing(request):
    news = NewsItem.objects.filter(published=True).order_by("-publish_time")[:3]

    return render(request, "home/landing.html", {"news": news})
