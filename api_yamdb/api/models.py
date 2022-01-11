from django.contrib.auth import get_user_model
from django.db import models
import datetime as dt
from django.core.exceptions import ValidationError

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return u'%s'%(self.name)

    def __str__(self):
        return self.name[:15]


class Genres(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name[:15]

def correctyear(data):
    year = dt.date.today().year
    if year < data:
        raise ValidationError("Некорректная дата")
    return data
class Titles(models.Model):
    name = models.TextField()
    year = models.IntegerField(db_index=True, validators=[correctyear])
    description = models.TextField()
    category = models.ForeignKey(
        Categories,
        null=True,
        on_delete=models.SET_NULL,
        related_name="title",
    )
    genre = models.ManyToManyField(
        Genres,
        related_name="title", null=True
    )

    def __str__(self):
        return self.name[:15]
    
    
