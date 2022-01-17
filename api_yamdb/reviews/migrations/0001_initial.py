# Generated by Django 2.2.16 on 2022-01-15 11:56

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import reviews.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("auth", "0011_update_proxy_permissions")]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("username", models.CharField(max_length=150, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("first_name", models.CharField(blank=True, max_length=150)),
                ("last_name", models.CharField(blank=True, max_length=150)),
                ("bio", models.TextField(blank=True, verbose_name="Биография")),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("user", "user"),
                            ("moderator", "moderator"),
                            ("admin", "admin"),
                        ],
                        default="user",
                        max_length=10,
                    ),
                ),
                (
                    "confirmation_code",
                    models.TextField(
                        blank=True, null=True, verbose_name="Код подтверждения"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[("objects", django.contrib.auth.models.UserManager())],
        ),
        migrations.CreateModel(
            name="Categories",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("slug", models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Genres",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("slug", models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Titles",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                (
                    "year",
                    models.IntegerField(
                        db_index=True, validators=[reviews.models.correctyear]
                    ),
                ),
                ("description", models.TextField()),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="title",
                        to="reviews.Categories",
                    ),
                ),
                (
                    "genre",
                    models.ManyToManyField(related_name="title", to="reviews.Genres"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.TextField(max_length=5000, verbose_name="Текст отзыва"),
                ),
                (
                    "score",
                    models.SmallIntegerField(
                        choices=[
                            (1, "1. Очень плохо. Не понравилось совсем."),
                            (2, "2. Плохо. Не понравилось почти всё."),
                            (3, "3. Не очень. Не понравилось многое."),
                            (4, "4. Так себе. Мало что понравилось."),
                            (5, "5. Ни то, ни сё. Почти ничего не понравилось."),
                            (6, "6. Неплохо. Кое-что понравилось."),
                            (7, "7. Хорошо. Многое понравилось."),
                            (8, "8. Очень хорошо. Почти всё понравилось."),
                            (9, "9. Великолепно. Очень понравилось."),
                            (10, "10. Высший балл. В восторге."),
                        ],
                        verbose_name="Оценка произведения пользователем",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания отзыва"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор отзыва",
                    ),
                ),
                (
                    "title",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="reviews.Titles",
                        verbose_name="Рецензируемое произведение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Отзыв. model Review",
                "verbose_name_plural": "Отзывы. model Review",
                "ordering": ("title",),
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.TextField(max_length=2000, verbose_name="Текст комментария"),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата создания комментария",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор комментария",
                    ),
                ),
                (
                    "review",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="reviews.Review",
                        verbose_name="Комментируемый отзыв",
                    ),
                ),
            ],
            options={
                "verbose_name": "Комментарий. model Comment",
                "verbose_name_plural": "Комментарии. model Comment",
                "ordering": ("review", "author"),
            },
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                fields=("title", "author"), name="title_one_review"
            ),
        ),
    ]
