from django.forms import ModelForm
from .models import Foto

class FotoForm(ModelForm):
    class Meta:
        model = Foto
        fields = ['title', 'description', 'images']