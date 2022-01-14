from rest_framework import serializers
from django.db.models import Avg
from reviews.models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    
    def get_rating(self, title):
        return Review.objects.filter(title=title.id).aggregate(avg_rating=Avg('score'))

    class Meta:
        model = Titles
        fields = '__all__'
