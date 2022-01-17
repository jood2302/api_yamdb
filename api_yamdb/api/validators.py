from rest_framework import serializers

from reviews.models import User


def username_exist(username):
    if not User.objects.filter(username=username).exists():
        raise serializers.ValidationError(
            "A user with that username don't exists."
        )
