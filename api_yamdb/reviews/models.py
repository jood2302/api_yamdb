import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Модель пользователей.
    username - логин пользователя
    email - электронная почта
    first_name - имя
    last_name - фамилия
    bio - биография
    role - роль
    confirmation_code - код подтверждения
    """
    ADMIN = "admin"
    MODER = "moderator"
    USER = "user"
    ME = "me"
    USER_CHOISES = [
        (USER, "admin"),
        (MODER, "moderator"),
        (ADMIN, "user")
    ]
    username = models.CharField("Логин", max_length=150, unique=True)
    email = models.EmailField("Почта", max_length=254, unique=True)
    first_name = models.CharField(
        "Имя",
        max_length=150,
        blank=True,
        unique=False
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150,
        blank=True,
        unique=False
    )

    bio = models.TextField("Биография", blank=True)
    role = models.CharField(
        "Роль",
        max_length=10,
        choices=USER_CHOISES,
        default=USER
    )

    confirmation_code = models.TextField(
        "Код подтверждения",
        null=True,
        blank=True
    )
    exclude = ("confirmation_code",)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ADMIN

        if self.role == self.ADMIN:
            self.is_staff = True
        else:
            self.is_staff = False

        super(User, self).save(*args, **kwargs)


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField("Slug", max_length=50, unique=True)

    def __str__(self):
        return self.name[:15]


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField("Slug", max_length=50, unique=True)

    def __str__(self):
        return self.name[:15]


def correctyear(data):
    year = dt.date.today().year
    if year < data:
        raise ValidationError("Некорректная дата")
    return data


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(db_index=True, validators=[correctyear])
    description = models.TextField()
    category = models.ForeignKey(
        Categories, null=True, on_delete=models.SET_NULL, related_name="title"
    )
    genre = models.ManyToManyField(Genres, related_name="title")

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Рецензируемое произведение",
    )
    text = models.TextField(max_length=5000, verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    score = models.SmallIntegerField(validators=[MinValueValidator(1),
                                     MaxValueValidator(10)], 
                                     verbose_name="Оценка произведения пользователем"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания отзыва"
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["title", "author"], name="title_one_review"
            ),
        )
        ordering = ("title",)
        verbose_name = "Отзыв. model Review"
        verbose_name_plural = "Отзывы. model Review"

    def __str__(self):
        return f"{self.author.username[:15]}, {self.text[:30]}, {self.score}"

    def __iter__(self):
        for field_name in self._meta.get_fields():
            value = getattr(self, field_name, None)
            yield (field_name, value)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Комментируемый отзыв",
    )
    text = models.TextField(max_length=2000, verbose_name="Текст комментария")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    pub_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания комментария"
    )

    class Meta:
        ordering = ("review", "author", "-pub_date",)
        verbose_name = "Комментарий. model Comment"
        verbose_name_plural = "Комментарии. model Comment"

    def __str__(self):
        return f"{self.author.username[:15]}, {self.text[:30]}"
