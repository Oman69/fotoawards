from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .forms import FotoForm, CommentsForm
from .models import Foto, Category, Comments
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
PRODUCTS_PER_PAGE = 4

def home(request, sort=1):

    sort_voices = request.GET.get('voices', '')
    sort_comments = request.GET.get('comments', '')
    sort_date = request.GET.get('date', '')

    categories = Category.objects.all()
    orders = ['voices', 'add_data']
    fotos = Foto.objects.order_by(orders[sort])
    page = request.GET.get('page', 1)
    product_paginator = Paginator(fotos, PRODUCTS_PER_PAGE)
    try:
        fotos = product_paginator.page(page)
    except EmptyPage:
        fotos = product_paginator.page(product_paginator.num_pages)
    except:
        fotos = product_paginator.page(PRODUCTS_PER_PAGE)
    context = {'Fotos': fotos, 'categories': categories, 'is_paginated': True, 'paginator': product_paginator, 'page_obj': fotos}
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
    if request.method == 'GET':
        foto_id = Foto.objects.get(pk=foto_id)
        categories = Category.objects.all()
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
            'form': CommentsForm(),
        }
        return render(request, 'foto/foto.html', context)
    else:
        try:
            form = CommentsForm(request.POST)
            newcomment = form.save(commit=False)
            newcomment.user = request.user
            newcomment.foto_id = foto_id
            newcomment.save()
            print('Created comment...')
            return redirect('user')
        except ValueError:
            return render(request, 'foto/foto.html', {'form': CommentsForm(), 'error': 'Ошибка'})



def delete_comment(request, pk):
    comment = get_object_or_404(Comments, pk=pk, user=request.user)
    if request.method == 'GET':
        comment.delete()
        print('Deleted comment...')
        return redirect('user')
        #return HttpResponseRedirect(reverse('foto', args=[str(pk)]))



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



def add_comment(request,foto_id):
    if request.method == 'GET':
        return render(request, 'foto/add_comment.html', {'form': CommentsForm()})
    else:
        try:
            form = CommentsForm(request.POST)
            newcomment = form.save(commit=False)
            newcomment.user = request.user
            newcomment.foto_id = foto_id
            newcomment.save()
            print('Form is working...')
            return redirect('user')
        except ValueError:
            return render(request, 'foto/add_comment.html', {'form': CommentsForm(), 'error': 'Ошибка'})



def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        fotos = Foto.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
        categories = Category.objects.all()
        context = {'Fotos': fotos, 'categories': categories, 'search': search}
        return render(request, 'foto/search.html', context)
    else:
        pass