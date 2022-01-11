from rest_framework import viewsets
from rest_framework import filters, mixins
from .models import Categories, Genres, Titles
from .serializers import CategoriesSerializer, GenresSerializer, TitlesSerializer
from .permissions import IsAdminOrReadOnly
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
