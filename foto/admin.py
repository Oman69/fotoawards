from django.contrib import admin

from foto.models import Foto, Category

# Register your models here.
class FotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'add_data', 'user', 'affected')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_editable = ('affected',)
    list_filter = ('affected',)



admin.site.register(Foto, FotoAdmin)
admin.site.register(Category)
