from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

appname = "api"
router_v1 = DefaultRouter()
router_v1.register(
    r"categories",
    views.CategoriesViewSet,
    basename="categories"
)
router_v1.register(
    r"genres",
    views.GenresViewSet,
    basename="genres"
)
router_v1.register(
    r"titles",
    views.TitlesViewSet,
    basename="titles"
)
router_v1.register(
    r"users",
    views.UserViewSet
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews",
    views.ReviewViewSet,
    basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    views.CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/auth/signup/", views.signup_user, name="signup"),
    path("v1/auth/token/", views.get_auth_token, name="auth"),
    path("v1/", include(router_v1.urls)),
]
