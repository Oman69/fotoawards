from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect

from .forms import FotoForm
from .models import Foto, Category, Comments
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def home(request):
    fotos = Foto.objects.all()
    categories = Category.objects.all()
    context = {'Fotos': fotos, 'categories': categories}
    return render(request, 'foto/home.html', context)



def category(request, category_id):
    filter_foto = Foto.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    category_id = Category.objects.get(pk=category_id)
    context = {
        'filter_foto': filter_foto,
        'categories': categories,
        'category_id': category_id,
    }
    return render(request, 'foto/category.html', context)


def foto(request, foto_id):
    foto_id = Foto.objects.get(pk=foto_id)
    categories = Category.objects.all()
    comments = Comments.objects.filter(id=foto_id.pk)
    stuff = get_object_or_404(Foto, id=foto_id.pk)
    total_voices = stuff.total_voices()
    liked = False
    if stuff.voices.filter(id=request.user.id):
        liked = True
    context = {
        'categories': categories,
        'foto_id': foto_id,
        'total_voices': total_voices,
        'liked': liked,
        'comments': comments,
    }
    return render(request, 'foto/foto.html', context)



def like(request, foto_id):
    foto_id = get_object_or_404(Foto, id=request.POST.get('foto_id'))
    liked = False
    if foto_id.voices.filter(id=request.user.id).exists():
        foto_id.voices.remove(request.user)
        liked = False
    else:
        foto_id.voices.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('foto', args=[str(foto_id.pk)]))


def user(request):
    filter_foto = Foto.objects.filter(user=request.user)
    categories = Category.objects.all()
    context = {'Fotos': filter_foto, 'categories': categories}
    return render(request, 'foto/user.html', context)



#Добавить фотографию
def add_foto(request):
    if request.method == 'GET':
        return render(request, 'foto/add_foto.html', {'form': FotoForm()})
    else:
        try:
            form = FotoForm(request.POST, request.FILES)
            newfoto = form.save(commit=False)
            newfoto.user = request.user
            newfoto.save()
            return redirect('user')
        except ValueError:
            return render(request, 'foto/add_foto.html', {'form': FotoForm(), 'error': 'Ошибка при загрузке'})