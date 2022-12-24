from django.shortcuts import render
from .models import Foto, Category
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
    context = {
        'categories': categories,
        'foto_id': foto_id,
    }
    return render(request, 'foto/foto.html', context)



def add_voice(request):
    if request.method == 'GET':
        return render(request, 'todo/create.html', {'form': ToDoForm()})
    else:
        try:
            form = ToDoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('current_todo')
        except ValueError:
            return render(request, 'todo/create.html', {'form': ToDoForm(), 'error': 'Слишком длинный заголовок!'})