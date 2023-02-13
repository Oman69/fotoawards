from django.contrib import admin
from chat.models import ChatMessage, ChatRoom


admin.site.register(ChatRoom)
admin.site.register(ChatMessage)