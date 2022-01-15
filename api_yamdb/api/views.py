from django.core.mail import send_mail
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins, permissions

from loguru import logger
from rest_framework.viewsets import GenericViewSet

from .secrets import generate_activation_key
from .serializers import UserSignUpSerializer, UserAuthSerializer, UserSerializer, UserMeSerializer
from .models import User


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

    def retrieve(self, request, *args, **kwargs):
        # do your customization here
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def UsersMe(request):
    user = User.objects.get(username=request.user)
    if request.method == 'GET':
        serializer = UserMeSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
