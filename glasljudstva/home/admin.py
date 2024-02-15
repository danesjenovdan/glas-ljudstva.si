from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import (
    CampaignItem,
    ContentPage,
    LandingPageConfig,
    NewsItem,
    PrimaryNavBarLink,
    SecondaryNavBarLink,
    SideBarLink,
)


class PrimaryNavBarLinkInline(OrderableAdmin, admin.TabularInline):
    model = PrimaryNavBarLink
    ordering_field_hide_input = True


class SecondaryNavBarLinkInline(OrderableAdmin, admin.TabularInline):
    model = SecondaryNavBarLink
    ordering_field_hide_input = True


class SideBarLinkInline(OrderableAdmin, admin.TabularInline):
    model = SideBarLink
    ordering_field_hide_input = True


class LandingPageConfigAdmin(SingletonModelAdmin):
    inlines = [
        PrimaryNavBarLinkInline,
        SecondaryNavBarLinkInline,
        SideBarLinkInline,
    ]


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "publish_time", "published")
    search_fields = ("title", "intro", "content")


class CampaignItemAdmin(OrderableAdmin, admin.ModelAdmin):
    list_display = ("title", "promoted", "published", "ordering")
    list_editable = ("ordering",)
    search_fields = ("title", "intro", "content")
    ordering_field_hide_input = True


class ContentPageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "published")
    search_fields = ("title", "content")


admin.site.register(LandingPageConfig, LandingPageConfigAdmin)
admin.site.register(CampaignItem, CampaignItemAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(ContentPage, ContentPageAdmin)
