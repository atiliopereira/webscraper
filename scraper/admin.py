from collections.abc import Sequence

from django.contrib import admin
from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.urls import path

from scraper.forms import scraperForm
from scraper.models import Link, Page
from scraper.services import create_page


class LinkInline(admin.TabularInline):
    model = Link
    extra = 0
    readonly_fields = (
        "name",
        "url",
    )
    show_change_link = False

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    change_list_template = "admin/scraper/page/change_list.html"
    change_form_template = "admin/scraper/page/change_form.html"
    readonly_fields = (
        "name",
        "url",
        "total_links",
        "created_by",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "url",
                    "total_links",
                )
            },
        ),
    )
    actions = None

    def total_links(self, obj):
        return obj.link_set.count()

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path(
                "scrape/",
                self.admin_site.admin_view(self.scrape),
                name="scraper_page_scrape",
            ),
        ]
        return my_urls + urls

    def scrape(self, request):
        if request.method == "POST":
            form = scraperForm(request.POST)
            if form.is_valid():
                url = form.cleaned_data["url"]
                message, status = create_page(url, request.user)
                level = "success" if status == 200 else "error"
                self.message_user(request=request, message=message, level=level)
            else:
                self.message_user(request, "Invalid URL")
        return redirect("admin:scraper_page_changelist")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["form"] = scraperForm()
        return super().changelist_view(request, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}

        page = self.get_object(request, object_id)

        links = page.link_set.all()
        paginator = Paginator(links, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        extra_context["links"] = page_obj
        extra_context["is_paginated"] = page_obj.has_other_pages()
        extra_context["page_obj"] = page_obj

        return super().change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def get_list_display(self, request):
        default_list_display = [
            "id",
            "name",
            "url",
            "total_links",
        ]
        if request.user.is_superuser:
            default_list_display.append("created_by")
        return default_list_display


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "page",
    )
