# Generated by Django 3.2.11 on 2022-01-11 14:30

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_genres_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='genre',
            field=models.ManyToManyField(null=True, related_name='title', to='api.Genres'),
        ),
        migrations.AlterField(
            model_name='titles',
            name='year',
            field=models.IntegerField(db_index=True, validators=[api.models.correctyear]),
        ),
    ]
