from django.db import models
from django.utils import timezone
from pytils.translit import slugify
from django.contrib.auth import get_user_model
from django.db import models
import datetime as dt
from django.core.exceptions import ValidationError


User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

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
        related_name="title")

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    """Отзывы пользователей. Контент пользователей.

    Поля 'title', 'text', 'author', 'score', 'pub_date'
    title - ссылка на произведение(model Title)
    text - текст отзыва
    author - ссылка на пользователя(model User)
    score - оценка пользователя(от 1 до 10 по заданию)
    pub_date - дата публикации(редактирования) отзыва
    Пользователь может оставить лишь один отзыв на произведение.
    Пользователь может менять текст и оценку или удалять полностью отзыв.
    Модератор может менять текст и оценку или удалять полностью объект.
    Администратор - как модератор.
    """
    SCORE_CHOICES = (
        (1, '1. Очень плохо. Не понравилось совсем.'),
        (2, '2. Плохо. Не понравилось почти всё.'),
        (3, '3. Не очень. Не понравилось многое.'),
        (4, '4. Так себе. Мало что понравилось.'),
        (5, '5. Ни то, ни сё. Почти ничего не понравилось.'),
        (6, '6. Неплохо. Кое-что понравилось.'),
        (7, '7. Хорошо. Многое понравилось.'),
        (8, '8. Очень хорошо. Почти всё понравилось.'),
        (9, '9. Великолепно. Очень понравилось.'),
        (10, '10. Высший балл. В восторге.'),
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Рецензируемое произведение'
    )
    text = models.TextField(
        max_length=5000,
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.SmallIntegerField(
        choices=SCORE_CHOICES,
        verbose_name='Оценка произведения пользователем'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания отзыва'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'author'], name='title_one_review'
            ),
        )
        ordering = ('title',)
        verbose_name = 'Отзыв. model Review'
        verbose_name_plural = 'Отзывы. model Review'

    def __str__(self):
        return (
            f'{self.author.username[:15]}, {self.text[:30]}, {self.score}'
        )

    def __iter__(self):
        for field_name in self._meta.get_fields():
            value = getattr(self, field_name, None)
            yield (field_name, value)


class Comment(models.Model):
    """Комментарии пользователей на отзывы. Контент пользователей.

    Поля 'review', 'text', 'author', 'pub_date'
    review - ссылка на отзыв(model Review).
    text - текст комментария.
    author - ссылка на автора коммента(model User)
    pub_date - дата создания
    Пользователь может менять текст или удалять полностью коммент.
    Модератор может менять текст или удалять полностью объект.
    Администратор - как модератор.
    """
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый отзыв'
    )
    text = models.TextField(
        max_length=2000,
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания комментария'
    )

    class Meta:
        ordering = ('review', 'author')
        verbose_name = 'Комментарий. model Comment'
        verbose_name_plural = 'Комментарии. model Comment'

    def __str__(self):
        return f'{self.author.username[:15]}, {self.text[:30]}'

    def __iter__(self):
        for field_name in self._meta.get_fields():
            value = getattr(self, field_name, None)
            yield (field_name, value)
