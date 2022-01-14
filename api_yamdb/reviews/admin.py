from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from .models import Categories, Genres, Titles


class CategoriesResources(resources.ModelResource):
    class Meta:
        model = Categories


class CategoriesAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'slug')
    resources_class = CategoriesResources


class GenresResources(resources.ModelResource):
    class Meta:
        model = Genres


class GenresAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'slug')
    resources_class = GenresResources


class TitlesResources(resources.ModelResource):
    class Meta:
        model = Titles


class TitlesAdmin(ImportExportActionModelAdmin):
    resources_class = TitlesResources


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, CategoriesAdmin)
admin.site.register(Titles, TitlesAdmin)
