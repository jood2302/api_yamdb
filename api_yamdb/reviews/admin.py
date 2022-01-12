from django.contrib import admin
from reviews.models import Category, Comment, Genre, Review, Title


class CategorysInstanceInline(admin.TabularInline):
    model = Category


class GenreInstanceInline(admin.TabularInline):
    model = Genre


class TitlesInstanceInline(admin.TabularInline):
    model = Title


class TitleGenreInline(admin.TabularInline):
    model = Title.genre.through


class ReviewsInstanceInline(admin.TabularInline):
    model = Review
    fields = ('id', 'title', 'text', 'author', 'score')


class CommentsInstanceInline(admin.TabularInline):
    model = Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = list_display
    prepopulated_fields = {'slug': ('name',)}
    inlines = (TitlesInstanceInline,)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category',)
    inlines = [
        TitleGenreInline,
    ]
    exclude = ('genres',)


class ReviewsInstanceInline(admin.TabularInline):
    model = Review
    fields = ('id', 'title', 'text', 'author', 'score')


class CommentsInstanceInline(admin.TabularInline):
    model = Comment
    inlines = (ReviewsInstanceInline,)
    list_display = ('id', 'name', 'year', 'category')
    list_display_links = list_display


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date')
    list_display_links = ['id', 'title', 'text', 'author', 'score', 'pub_date']
    list_filter = ['title', 'text', 'author', 'score', 'pub_date']
    search_fields = ['id', 'title', 'text', 'author', 'score', 'pub_date']
    inlines = (CommentsInstanceInline,)

    class Meta:
        model = Review


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'text', 'pub_date')
    list_display_links = list_display