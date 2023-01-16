from django.contrib import admin

from foto.models import Foto, Category, Comments, Subscribe

# Register your models here.
class FotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'add_data', 'user', 'affected', 'deleted')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_editable = ('affected', 'deleted')
    list_filter = ('affected','deleted')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'foto', 'user')
    list_display_links = ('id', 'text', 'foto', 'user')


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email')
    list_display_links = ('id', 'user', 'email')


admin.site.register(Foto, FotoAdmin)
admin.site.register(Category)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
