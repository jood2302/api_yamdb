from rest_framework import status, viewsets, permissions, filters, mixins
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Avg
from reviews.models import Categories, Genres, Titles, Comment, Review, User
from .secrets import generate_activation_key
from .serializers import (CategoriesSerializer, GenresSerializer, TitlesSerializer,
                          ReviewSerializer, CommentSerializer, UserSignUpSerializer,
                          UserAuthSerializer, UserSerializer, UserMeSerializer)
from .permissions import IsAdminOrReadOnly, IsUserOrAdminOrModerOrReadOnly
from .filter import TitleFilter

class CreateListDestroy(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass


class CategoriesViewSet(CreateListDestroy):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

class GenresViewSet(CreateListDestroy):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
  
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
    permission_classes = (IsUserOrAdminOrModerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))

        serializer.save(
            author=self.request.user,
            title=title
        )

    def perform_update(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        review_id = self.kwargs.get('pk')
        author = Review.objects.get(pk=review_id).author
        serializer.save(
            author=author,
            title_id=title.id
        )


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = CommentSerializer
    permission_classes = (IsUserOrAdminOrModerOrReadOnly,)

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


@api_view(['POST'])
def signupUser(request):
    serializer = UserSignUpSerializer(data=request.data, many=False)
    if serializer.is_valid():
        confirmation_code = generate_activation_key(request.data['username'])
        serializer.save(confirmation_code=confirmation_code)

        email = request.data['email']
        send_mail(
            'API_YAMDB: Confirmation code',
            f'confirmation_code: {confirmation_code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def getAuthToken(request):
    serializer = UserAuthSerializer(data=request.data, many=False)
    if serializer.is_valid():
        token = serializer.data['token']
        return Response({'token': token}, status=status.HTTP_200_OK)

    username_err = serializer.errors.get('username')
    if username_err is not None:
        for e in username_err:
            if e.code == 'invalid':
                return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAdminUser,)
    lookup_field = 'username'


@api_view(['GET', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def UsersMe(request):
    user = User.objects.get(username=request.user)
    if request.method == 'GET':
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = UserMeSerializer(user, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
