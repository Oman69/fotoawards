from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Foto(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=1000, verbose_name='Описание', blank=True, null=True)
    add_data = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, verbose_name='Категория', default='Без категории')
    affected = models.BooleanField(default=False, verbose_name='Одобрено модератором')
    images = models.ImageField(upload_to='media', verbose_name='Фотография')
    voices = models.ManyToManyField(User, related_name='foto_voices', verbose_name='Голоса', blank=True)


    def __str__(self):
        return self.title

    def total_voices(self):
        return self.voices.count()


    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'



class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(max_length=1000, verbose_name='Описание', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'




class Comments(models.Model):
    text = models.TextField(max_length=500, verbose_name='Текст комментария')
    foto = models.ForeignKey(Foto, on_delete=models.CASCADE, related_name='comments', verbose_name='Фото комментария')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')
    approved = models.BooleanField(default=False, verbose_name='Одобрено модератором')


    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Subscribe(models.Model):
    user = models.CharField(max_length=100, verbose_name='Имя пользователя')
    email = models.EmailField(max_length=100, verbose_name='Электронная почта')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'