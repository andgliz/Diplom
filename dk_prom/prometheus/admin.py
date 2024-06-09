from django.contrib import admin
from prometheus.models import *


class PrometheusAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image", "data", "time", "category", "space")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class SpacesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "time", "event", "user", "seats_reserved")
    list_display_links = ("id", "event")
    search_fields = ("event",)


class RecordAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "number", "group")
    list_display_links = ("id", "name")
    search_fields = ("name",)


class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "image1", "image2", "image3", "image4", "image5")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "post", "image")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Events, PrometheusAdmin)
admin.site.register(Spaces, SpacesAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(FirstLessons, RecordAdmin)
admin.site.register(Groups, GroupAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Booking, BookingAdmin)
