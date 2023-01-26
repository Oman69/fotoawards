from django.forms import ModelForm
from .models import Foto, Comments, Subscribe, CommentsSecondLevel


class FotoForm(ModelForm):
    class Meta:
        model = Foto
        fields = ['title', 'description', 'images', 'category']


class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['text']


class CommentsSecondLevelForm(ModelForm):
    class Meta:
        model = CommentsSecondLevel
        fields = ['text']


class SubscribeForm(ModelForm):
    class Meta:
        model = Subscribe
        fields = ['user', 'email']