from django.db import models
from django.contrib.auth.models import User
from imagekit.models.fields import ImageSpecField
from imagekit.processors import Adjust,ResizeToFit, ResizeToFill

from foto.validators import validate_image


# Create your models here.



class Foto(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=1000, verbose_name='Описание', blank=True, null=True)
    add_data = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, verbose_name='Категория', null=True, default=4)
    affected = models.BooleanField(default=False, verbose_name='Одобрено')
    images = models.ImageField(upload_to='media', verbose_name='Фотография')
    image_medium = ImageSpecField([Adjust(contrast=1.1, sharpness=1.0),
            ResizeToFill(200, 200)], format='JPEG', options={'quality': 90})
    voices = models.ManyToManyField(User, related_name='foto_voices', verbose_name='Голоса', blank=True)
    deleted = models.BooleanField(default=False, verbose_name='На удалении')
    dismissed = models.BooleanField(default=False, verbose_name='Отклонено')


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


class CommentsSecondLevel(models.Model):
    text = models.TextField(max_length=500, verbose_name='Текст комментария второго уровня')
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='secondComment', verbose_name='Первый комментарий')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария второго уровня')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')
    approved = models.BooleanField(default=False, verbose_name='Одобрено модератором')


    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий второго уровня'
        verbose_name_plural = 'Комментарии второго уровня'




class Subscribe(models.Model):
    user = models.CharField(max_length=100, verbose_name='Имя пользователя')
    email = models.EmailField(max_length=100, verbose_name='Электронная почта')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'