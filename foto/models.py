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
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, verbose_name='Категория')
    affected = models.BooleanField(default=False, verbose_name='Одобрено модератором')
    images = models.ImageField(upload_to='media', verbose_name='Фотография')
    voices = models.ManyToManyField(User, related_name='foto_voices', verbose_name='Голоса', blank=True, null=True)
    comments = models.ManyToManyField(User, related_name='foto_comments',  verbose_name='Комментарии', blank=True, null=True)


    def __str__(self):
        return self.title

    def total_voices(self):
        return self.voices.count()



class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(max_length=1000, verbose_name='Описание', blank=True)

    def __str__(self):
        return self.title



class Voices(models.Model):
    pass




class Comments(models.Model):
    pass