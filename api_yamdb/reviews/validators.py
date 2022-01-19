from django.core.exceptions import ValidationError
from django.utils import timezone


def correct_year(data):
    now = timezone.now().year
    if now < data:
        raise ValidationError("Некорректная дата")
    return data
