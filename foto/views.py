from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Foto, Category
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
    stuff = get_object_or_404(Foto, id=foto_id.pk)
    total_voices = stuff.total_voices()
    context = {
        'categories': categories,
        'foto_id': foto_id,
        'total_voices': total_voices
    }
    return render(request, 'foto/foto.html', context)



def like(request, foto_id):
    foto_id = get_object_or_404(Foto, id=request.POST.get('foto_id'))
    liked = True
    foto_id.voices.add(request.user)
    return HttpResponseRedirect(reverse('foto', args=[str(foto_id.pk)]))



def login_user(request):
    if request.method == 'GET':
        return render(request, 'foto/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'foto/login.html', {'form': AuthenticationForm(), 'error': 'Пользователь с такими данными не найден'})
        else:
            login(request, user)
            return redirect('home')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')