from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name[:15]


class Genres(models.Model):
    FUSION = "FU"
    CLASSIC = "CL"
    POP = "PO"
    STORY = "ST"
    GENRE_CHOISES = [
        (FUSION, "FUSION"),
        (CLASSIC, "CLASSIC"),
        (POP, "POP"),
        (STORY, "STORY"),
    ]
    name = models.CharField(
        max_length=2,
        choices=GENRE_CHOISES,
        default=FUSION)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name[:15]


class Titles(models.Model):
    name = models.TextField()
    year = models.IntegerField(db_index=True)
    description = models.TextField()
    category = models.ForeignKey(
        Categories,
        null=True,
        on_delete=models.SET_NULL,
        related_name="title",
    )
    genre = models.ManyToManyField(
        Genres,
        related_name="title"
    )

    def __str__(self):
        return self.name[:15]
