from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название чата')
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.title

    def connect_user(self, user):
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        elif user in self.users.all():
            is_user_removed = True
        return is_user_removed


    @property
    def room_name(self):
        return f'Чат - {self.title}'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class ChatManager(models.Manager):
    def by_room(self, room):
        messages_in_room = ChatMessage.objects.filter(room=room).order_by('-timestamp')
        return messages_in_room

class ChatMessage(models.Model):
    text = models.TextField(max_length=1000, verbose_name='Сообщение')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор сообщения')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, verbose_name='Чат', related_name='room')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время сообщения')

    objects = ChatManager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'