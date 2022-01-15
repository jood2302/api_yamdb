from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

appname = 'api'
router_v1 = DefaultRouter()
router_v1.register(r'categories', views.CategoriesViewSet, basename='categories')
router_v1.register(r'genres', views.GenresViewSet, basename='genres')
router_v1.register(r'titles', views.TitlesViewSet, basename='titles')
router_v1.register(r"users", views.UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', views.signupUser, name='signup'),
    path('v1/auth/token/', views.getAuthToken, name='auth'),
    path('v1/users/me/', views.UsersMe, name='users_me'),

    path('v1/', include(router_v1.urls)),
]
