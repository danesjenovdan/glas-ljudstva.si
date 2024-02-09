from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import LandingPageConfig, NewsItem, SideBarLink


class SideBarLinkInline(OrderableAdmin, admin.TabularInline):
    model = SideBarLink
    ordering_field_hide_input = True


class LandingPageConfigAdmin(SingletonModelAdmin):
    inlines = [SideBarLinkInline]


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "publish_time", "published")
    search_fields = ("title", "body")


admin.site.register(LandingPageConfig, LandingPageConfigAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
