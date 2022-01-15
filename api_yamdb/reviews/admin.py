from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from .models import Categories, Genres, Titles, Review, Comment


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


class CommentResources(resources.ModelResource):
    class Meta:
        model = Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'text', 'pub_date')
    resources_class = CommentResources


class ReviewResources(resources.ModelResource):
    class Meta:
        model = Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date')
    resources_class = ReviewResources


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, CategoriesAdmin)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)

