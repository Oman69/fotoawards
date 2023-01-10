from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .forms import FotoForm, CommentsForm, SubscribeForm
from .models import Foto, Category, Comments
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .service import send
from .tasks import send_spam_email

# Create your views here.
PRODUCTS_PER_PAGE = 4

def home(request):
    # Вытаскиваем все объекты классов Фото и Категории
    categories = Category.objects.all()
    fotos = Foto.objects.all()

    # Сортировка
    sorting = request.GET.get('ordering', '')
    if sorting:
        fotos = fotos.order_by(sorting)

    # Убираем дубликаты при выводе
    groupnames = set()
    distinct_fotos = []
    for item in fotos:
        if item.title not in groupnames:
            distinct_fotos.append(item)
            groupnames.add(item.title)
    fotos = distinct_fotos

    # Пагинация
    page = request.GET.get('page', 1)
    product_paginator = Paginator(fotos, PRODUCTS_PER_PAGE)
    try:
        fotos = product_paginator.page(page)
    except EmptyPage:
        fotos = product_paginator.page(product_paginator.num_pages)
    except:
        fotos = product_paginator.page(PRODUCTS_PER_PAGE)

    # Добавляем контекст
    context = {'Fotos': fotos, 'categories': categories, 'is_paginated': True, 'paginator': product_paginator, 'page_obj': fotos}
    return render(request, 'foto/home.html', context)



def category(request, category_id):
    fotos = Foto.objects.filter(category_id=category_id)

    # Сортировка
    sorting = request.GET.get('ordering', '')
    if sorting:
        fotos = fotos.order_by(sorting)

    # Убираем дубликаты при выводе
    groupnames = set()
    distinct_fotos = []
    for item in fotos:
        if item.title not in groupnames:
            distinct_fotos.append(item)
            groupnames.add(item.title)
    fotos = distinct_fotos

    # Пагинация
    page = request.GET.get('page', 1)
    product_paginator = Paginator(fotos, PRODUCTS_PER_PAGE)
    try:
        fotos = product_paginator.page(page)
    except EmptyPage:
        fotos = product_paginator.page(product_paginator.num_pages)
    except:
        fotos = product_paginator.page(PRODUCTS_PER_PAGE)


    categories = Category.objects.all()
    category_id = Category.objects.get(pk=category_id)
    context = {
        'filter_foto': fotos,
        'categories': categories,
        'category_id': category_id,
        'is_paginated': True,
        'paginator': product_paginator,
        'page_obj': fotos
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
            return redirect('home')
            #return redirect('foto', foto_id=foto_id)
        except ValueError:
            return render(request, 'foto/foto.html', {'form': CommentsForm(), 'error': 'Ошибка'})







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


def delete_foto(request, foto_id):
    foto = get_object_or_404(Foto, pk=foto_id, user=request.user)
    if request.method == 'GET':
        foto.delete()
        print('Foto comment...')
        return redirect('user')


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


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id, user=request.user)
    if request.method == 'GET':
        comment.delete()
        print('Deleted comment...')
        return redirect('user')
        #return redirect('foto')



def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        fotos = Foto.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
        categories = Category.objects.all()
        context = {'Fotos': fotos, 'categories': categories, 'search': search}
        return render(request, 'foto/search.html', context)
    else:
        pass

# Форма подписки
def subscribe(request):

    if request.method == 'GET':
        return render(request, 'foto/subscribe.html', {'form': SubscribeForm()})
    else:
        try:
            subscribe_form = SubscribeForm(request.POST, request.FILES)
            new_subscribe = subscribe_form.save(commit=False)
            new_subscribe.user = request.user
            new_subscribe.save()
            #send(subscribe_form.instance.email)
            send_spam_email.delay(subscribe_form.instance.email)
            return redirect('home')
        except ValueError:
            return render(request, 'foto/subscribe.html', {'form': SubscribeForm(), 'error': 'Ошибка'})