from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Categories, Genres, Titles, User


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Categories
        fields = ('id', 'name', 'slug',)


class CategoriesAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource


admin.site.register(User)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres)
admin.site.register(Titles)
