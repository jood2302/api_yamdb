from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.db.models import Avg
from rest_framework.exceptions import ParseError

from reviews.models import Categories, Genres, Review, Titles, Comment, User
from rest_framework_simplejwt.tokens import RefreshToken

from .validators import username_exist


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        title = get_object_or_404(Titles, pk=title_id)
        user = self.context['request'].user
        if (
            self.context['request'].method == 'POST'
            and Review.objects.filter(author=user, title=title).exists()
        ):
            raise ParseError(
                'Возможен только один отзыв на произведение!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        exclude = ('review',)
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']


class UserMeSerializer(UserSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)


class UserSignUpSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists!")
        return value

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("A user with that username already exists.")
        return value


class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[username_exist])
    token = serializers.SerializerMethodField(read_only=True)

    # todo( не работает через def validate_username)
    # A user with that username already exists.

    class Meta:
        model = User
        fields = ['username', 'confirmation_code', 'token']

    # def validate_username(self, value):
    #     if not User.objects.filter(username=value).exists():
    #         raise serializers.ValidationError({'username': 'A user with that username don\'t exists.'})
    def get_token(self, data):
        user = User.objects.get(username=data['username'])
        token = RefreshToken.for_user(user)
        return str(token.access_token)

    def validate(self, data):
        # if not User.objects.filter(username=username).exists():
        #     raise serializers.ValidationError('A user with that username don\'t exists.')

        code = User.objects.get(username=data['username']).confirmation_code
        code_from_user = data.get('confirmation_code')
        if code_from_user is None:
            raise serializers.ValidationError({'confirmation_code': "This field is required."})

        if code != code_from_user:
            raise serializers.ValidationError({'confirmation_code': "Invalid value."})
        return data
