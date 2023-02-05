# Generated by Django 4.1.5 on 2023-02-05 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название категории')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500, verbose_name='Текст комментария')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')),
                ('approved', models.BooleanField(default=False, verbose_name='Одобрено модератором')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100, verbose_name='Имя пользователя')),
                ('email', models.EmailField(max_length=100, verbose_name='Электронная почта')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Описание')),
                ('add_data', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('affected', models.BooleanField(default=False, verbose_name='Одобрено')),
                ('images', models.ImageField(upload_to='media', verbose_name='Фотография')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('dismissed', models.BooleanField(default=False, verbose_name='Отклонено')),
                ('category', models.ForeignKey(default='Без категории', on_delete=django.db.models.deletion.DO_NOTHING, to='foto.category', verbose_name='Категория')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('voices', models.ManyToManyField(blank=True, related_name='foto_voices', to=settings.AUTH_USER_MODEL, verbose_name='Голоса')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фотографии',
            },
        ),
        migrations.CreateModel(
            name='CommentsSecondLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500, verbose_name='Текст комментария второго уровня')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')),
                ('approved', models.BooleanField(default=False, verbose_name='Одобрено модератором')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondComment', to='foto.comments', verbose_name='Первый комментарий')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария второго уровня')),
            ],
            options={
                'verbose_name': 'Комментарий второго уровня',
                'verbose_name_plural': 'Комментарии второго уровня',
            },
        ),
        migrations.AddField(
            model_name='comments',
            name='foto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='foto.foto', verbose_name='Фото комментария'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария'),
        ),
    ]
