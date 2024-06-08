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


class RecordAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "number", "group")
    list_display_links = ("id", "name")
    search_fields = ("name",)


admin.site.register(Events, PrometheusAdmin)
admin.site.register(Spaces, SpacesAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(FirstLessons, RecordAdmin)
