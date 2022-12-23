from django.shortcuts import render
from .models import Foto, Category
# Create your views here.


def home(request):
    fotos = Foto.objects.all()
    categories = Category.objects.all()
    context = {'Fotos': fotos, 'categories': categories}
    return render(request, 'foto/home.html', context)



def category(request, category_id):
    blogs = Foto.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    category_id = Category.objects.get(pk=category_id)
    context = {
        'blogs': blogs,
        'categories': categories,
        'category_id': category_id,
    }
    return render(request, 'foto/cat.html', context)