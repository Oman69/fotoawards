from django.contrib import admin

from foto.models import Foto, Category, Comments, Subscribe, CommentsSecondLevel

# Register your models here.
class FotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'add_data', 'user', 'affected', 'dismissed', 'deleted')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_editable = ('affected', 'deleted', 'dismissed')
    list_filter = ('affected','deleted')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'foto', 'user')
    list_display_links = ('id', 'text', 'foto', 'user')


class CommentsSecondLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'comment', 'user')
    list_display_links = ('id', 'text', 'comment', 'user')


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email')
    list_display_links = ('id', 'user', 'email')


admin.site.register(Foto, FotoAdmin)
admin.site.register(Category)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(CommentsSecondLevel, CommentsSecondLevelAdmin)
