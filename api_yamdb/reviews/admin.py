from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from .models import Category, Comment, Genre, Review, Title, User


class CategoriesResources(resources.ModelResource):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class CategoriesAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "slug")
    resources_class = CategoriesResources


class GenresResources(resources.ModelResource):
    class Meta:
        model = Genre


class GenresAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "slug")
    resources_class = GenresResources


class TitlesResources(resources.ModelResource):
    class Meta:
        model = Title


class TitlesAdmin(ImportExportActionModelAdmin):
    resources_class = TitlesResources


class CommentResources(resources.ModelResource):
    class Meta:
        model = Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "review", "text", "pub_date")
    resources_class = CommentResources


class ReviewResources(resources.ModelResource):
    class Meta:
        model = Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "text", "author", "score", "pub_date")
    resources_class = ReviewResources


admin.site.register(User)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(Genre, CategoriesAdmin)
admin.site.register(Title, TitlesAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
