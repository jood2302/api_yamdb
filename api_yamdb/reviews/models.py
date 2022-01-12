from django.db import models
from django.utils import timezone
from pytils.translit import slugify
from users.models import User


class Category(models.Model):
    """Категории 'произведений'. Разделы на портале.

    Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
    Список категорий (Category) может быть расширен администратором
    (например, можно добавить категорию «Изобразительное искусство»
    или «Ювелирка»).
    """
    name = models.CharField(
        max_length=200,
        unique=True
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория. model Category'
        verbose_name_plural = 'Категории. model Category'

    def __str__(self):
        return self.name[:20]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:20]
        super().save(*args, **kwargs)


class Genre(models.Model):
    """Жанр произведения культуры.

    Произведению может быть присвоен жанр (Genre) из списка предустановленных
    (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать
    только администратор.
    """
    name = models.CharField(
        max_length=200,
        unique=True
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр. model Genre'
        verbose_name_plural = 'Жанры. model Genre'

    def __str__(self):
        return self.name[:20]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:20]
        super().save(*args, **kwargs)


class Title(models.Model):
    """Основной эл-т БД. Произведение культуры. Конкретный объект.

    Поля 'name', 'year', 'category', 'description' и 'rating'.
    name - Авторское или исторически сложившееся название. Обязательное.
    year - Год издания/публикации произведения. Обязательное.
    category - ссылка на категорию. Обязательное. При удалении категории,
    принимает дефоптное значение.
    Значение по умолчанию - 'Null'.
    description - Краткое представление произведения.
    Администрирование и наполнение доступны администратору системы.
    """
    name = models.CharField(
        max_length=300,
        verbose_name='Название произведения.'
    )
    description = models.CharField(
        max_length=300,
        verbose_name='Краткое представление произведения.'
    )

    year = models.PositiveSmallIntegerField(
        verbose_name='Год издания/публикации произведения.',
        db_index=True
    )
    description = models.CharField(
        max_length=300, blank=True, null=True,
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Раздел портала.'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
    )

    class Meta:
        ordering = ('category', 'name')
        verbose_name = 'Произведение. model Title'
        verbose_name_plural = 'Произведения. model Title'

    def __str__(self):
        return f'{self.name[:20]}, {str(self.year)}, {self.category}'


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