from django.core.mail import send_mail
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from .mixins import CreateListDestroy
from reviews.models import Category, Comment, Genre, Review, Title, User
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly, IsUserOrAdminOrModerOrReadOnly
from .secrets import generate_activation_key
from .serializers import (
    CategoriesSerializer,
    CommentSerializer,
    GenresSerializer,
    ReviewSerializer,
    TitlesReadSerializer,
    TitlesWriteSerializer,
    UserAuthSerializer,
    UserMeSerializer,
    UserSerializer,
    UserSignUpSerializer,
)


class CategoriesViewSet(CreateListDestroy):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenresViewSet(CreateListDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return TitlesWriteSerializer
        return TitlesReadSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = ReviewSerializer
    permission_classes = (IsUserOrAdminOrModerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review_id = self.kwargs.get("pk")
        author = get_object_or_404(Review.objects, pk=review_id).author
        serializer.save(author=author, title_id=title.id)


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = CommentSerializer
    permission_classes = (IsUserOrAdminOrModerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review_id=review.id)

    def perform_update(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        comment_id = self.kwargs.get("pk")
        author = get_object_or_404(Comment.objects, pk=comment_id).author
        serializer.save(author=author, review_id=review.id)


@api_view(["POST"])
def signupUser(request):
    serializer = UserSignUpSerializer(data=request.data, many=False)
    if serializer.is_valid():
        confirmation_code = generate_activation_key(request.data["username"])
        serializer.save(confirmation_code=confirmation_code)

        email = request.data["email"]
        send_mail(
            "API_YAMDB: Confirmation code",
            f"confirmation_code: {confirmation_code}",
            "from@example.com",
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def getAuthToken(request):
    serializer = UserAuthSerializer(data=request.data, many=False)
    if serializer.is_valid():
        token = serializer.data["token"]
        return Response({"token": token}, status=status.HTTP_200_OK)

    username_err = serializer.errors.get("username")
    if username_err is not None:
        for e in username_err:
            if e.code == "invalid":
                return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAdminUser,)
    lookup_field = "username"


@api_view(["GET", "PATCH"])
@permission_classes([permissions.IsAuthenticated])
def UsersMe(request):
    user = User.objects.get(username=request.user)
    if request.method == "GET":
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = UserMeSerializer(user, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
