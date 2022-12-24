from django.contrib import admin

from foto.models import Foto, Category, Voices, Comments

# Register your models here.

admin.site.register(Foto)
admin.site.register(Category)
admin.site.register(Voices)
admin.site.register(Comments)