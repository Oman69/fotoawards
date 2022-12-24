from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
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
    images = models.ImageField(upload_to='media')
    voices = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)


    def __str__(self):
        return self.title



class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(max_length=1000, verbose_name='Описание', blank=True)

    def __str__(self):
        return self.title



class Voices(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='voices',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.user




class Comments(models.Model):
    count = models.IntegerField(default=0)
    text = models.TextField(max_length=150, null=True)

    def __str__(self):
        return self.text