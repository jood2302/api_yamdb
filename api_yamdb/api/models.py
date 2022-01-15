from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_CHOISES = [
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True, unique=False)
    last_name = models.CharField(max_length=150, blank=True, unique=False)

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=USER_CHOISES,
        default="user")

    confirmation_code = models.TextField(
        'Код подтверждения',
        null=True, blank=True,
    )
    exclude = ('confirmation_code',)

    def save(self, *args, **kwargs):
        # set the value of the read_only_field using the regular field
        if self.role == 'admin':
            self.is_staff = True

        # call the save() method of the parent
        super(User, self).save(*args, **kwargs)


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
