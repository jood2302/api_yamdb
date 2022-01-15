from django.urls import include, path
from rest_framework import routers

from . import views
from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', views.signupUser, name='signup'),
    path('v1/auth/token/', views.getAuthToken, name='auth'),
    path('v1/users/me/', views.UsersMe, name='users_me'),

    path("v1/", include(router.urls)),
]
