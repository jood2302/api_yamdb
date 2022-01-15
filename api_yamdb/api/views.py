from rest_framework import viewsets
from rest_framework import filters, mixins
from reviews.models import Categories, Genres, Titles, Comment, Review
from .serializers import (CategoriesSerializer, GenresSerializer, TitlesSerializer,
                          ReviewSerializer, CommentSerializer)
from .permissions import IsAdminOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_list_or_404, get_object_or_404


class CreateListDestroy(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass
class CategoriesViewSet(CreateListDestroy):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)

class GenresViewSet(CreateListDestroy):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category', 'genre')

    def get_category_genres(self, serializer):
        category_slug = serializer.initial_data.get('category')
        category = get_object_or_404(Categories, slug=category_slug)
        genre_slugs = serializer.initial_data.getlist('genre')
        if genre_slugs:
            genres = get_list_or_404(Genres, slug__in=genre_slugs)
            serializer.save(category=category, genre=genres)
        else:
            serializer.save(category=category)

    def perform_create(self, serializer):
        self.get_category_genres(serializer)

    def perform_update(self, serializer):
        self.get_category_genres(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        serializer.save(
            author=self.request.user,
            title=title
        )

    def perform_update(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review_id = self.kwargs.get('pk')
        author = Review.objects.get(pk=review_id).author
        serializer.save(
            author=author,
            title_id=title.id
        )


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,) #orReadOnly  если тесты будут падать

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review.id)

    def perform_update(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        comment_id = self.kwargs.get('pk')
        author = Comment.objects.get(pk=comment_id).author
        serializer.save(
            author=author,
            review_id=review.id
        )