from django_filters import rest_framework as filter
from django_filters.filters import CharFilter, NumberFilter

from reviews.models import Titles


class TitleFilter(filter.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = NumberFilter(field_name='year', lookup_expr='exact')
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')

    class Meta:
        model = Titles
        fields = ('name', 'year', 'category', 'genre')
        