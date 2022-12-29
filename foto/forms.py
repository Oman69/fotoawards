from django.forms import ModelForm
from .models import Foto, Comments

class FotoForm(ModelForm):
    class Meta:
        model = Foto
        fields = ['title', 'description', 'images', 'category']


class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['text']