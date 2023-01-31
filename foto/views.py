import jsonpickle

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from .forms import FotoForm, CommentsForm, SubscribeForm, CommentsSecondLevelForm
from .models import Foto, Category, Comments, User, CommentsSecondLevel
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

from .service import send
from .tasks import send_spam_email, lazy_delete_foto

# Create your views here.
PRODUCTS_PER_PAGE = 4


def home(request):
    # Вытаскиваем все объекты классов Фото и Категории
    categories = Category.objects.all()
    fotos = Foto.objects.annotate(comments_count=Count('comments'), voices_count=Count('voices'))

    # Сортировка
    sorting = request.GET.get('ordering', None)
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
        commentsSecond = CommentsSecondLevel.objects.filter(pk=foto_id.pk)
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
            'commentsSecond': commentsSecond,
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
        except ValueError:
            return render(request, 'foto/foto.html', {'form': CommentsForm(), 'error': 'Ошибка'})


#Лайки
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

#Личный кабинет пользователя
def user(request):
    filter_foto = Foto.objects.filter(user=request.user)
    categories = Category.objects.all()

    # Фильтрация
    filtering = request.GET.get('filtering', '')

    if filtering == 'on_moderation':
        new_filter = []
        for item in filter_foto:
            if item.affected == False:
                new_filter.append(item)
    elif filtering == 'on_delete':
        new_filter = []
        for item in filter_foto:
            if item.deleted == True:
                new_filter.append(item)
    elif filtering == 'accepted':
        new_filter = []
        for item in filter_foto:
            if item.affected == True:
                new_filter.append(item)
    else:
        new_filter = filter_foto


    context = {'Fotos': new_filter, 'categories': categories}
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



def edit_foto(request, foto_id):
    foto = get_object_or_404(Foto, pk=foto_id, user=request.user)
    if request.method == 'GET':
        form = FotoForm(instance=foto)
        return render(request, 'foto/add_foto.html', {'foto': foto, 'form': form})
    else:
        try:
            form = FotoForm(request.POST, instance=foto)
            form.save()
            print(foto.images, request.POST)
            if foto.images != request.POST.get('images', False):
                foto.affected = False
                foto.save()
            return redirect('user')
        except ValueError:
            return render(request, 'foto/add_foto.html', {'foto': foto, 'form': form, 'error': 'Bad data!'})



#Удалить фотографию
def delete_foto(request, foto_id):
    foto = get_object_or_404(Foto, pk=foto_id, user=request.user)
    frozen = jsonpickle.encode({'foto_pk': foto.pk})
    if request.method == 'GET':
        foto.deleted = True
        foto.save()
        #Синхронное удаление
        #foto.delete()
        #Отложенное удаление фотографии через 60 секунд
        lazy_delete_foto.apply_async((frozen, ), countdown=60)
        return redirect('user')


#Отменить удаление
def no_delete_foto(request, foto_id):
    foto = get_object_or_404(Foto, pk=foto_id, user=request.user)
    if request.method == 'GET':
        foto.deleted = False
        foto.save()
        return redirect('user')


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
            return redirect('home')
        except ValueError:
            return render(request, 'foto/add_comment.html', {'form': CommentsForm(), 'error': 'Ошибка'})


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id, user=request.user)
    if request.method == 'GET':
        form = CommentsForm(instance=comment)
        return render(request, 'foto/edit.html', {'comment': comment, 'form': form})
    else:
        try:
            form = CommentsForm(request.POST, instance=comment)
            form.save()
            return redirect('home')
        except ValueError:
            return render(request, 'foto/edit.html', {'comment': comment, 'form': form, 'error': 'Bad data!'})


def delete_comment(request, comment_id):
    if request.method == 'GET':
        comment = get_object_or_404(Comments, pk=comment_id, user=request.user)
        print(request.GET)
        comment.delete()
        print('Deleted comment...')
        #return redirect('foto', foto)
        return redirect('home')


def delete_comment_asinc(request):
    if request.method == 'DELETE':
        print('Вошли в функцию')
        comment = get_object_or_404(Comments, pk=request.GET.get('pk'), user=request.user)
        comment.delete()
        return HttpResponse('Комментарий удален')


def add_comment_second_level(request,comment_id):
    if request.method == 'GET':
        return render(request, 'foto/add_comment_second_level.html', {'form': CommentsSecondLevelForm()})
    else:
        try:
            form = CommentsSecondLevelForm(request.POST)
            newSecondComment = form.save(commit=False)
            newSecondComment.user = request.user
            newSecondComment.comment_id = comment_id
            newSecondComment.save()

            print('NewForm is working...')
            return redirect('home')
        except ValueError:
            return render(request, 'foto/add_comment_second_level.html', {'form': CommentsSecondLevelForm(), 'error': 'Ошибка'})


def del_comment_second_level(request, comment_id):
    comment = get_object_or_404(CommentsSecondLevel, pk=comment_id, user=request.user)
    if request.method == 'GET':
        comment.delete()
        print('Deleted comment...')
        return redirect('home')

def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        fotos = Foto.objects.filter(Q(title__icontains=search) | Q(description__icontains=search)| Q(user__username__icontains=search))
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
            send(subscribe_form.instance.email)
            #send_spam_email.delay(subscribe_form.instance.email)
            #send_spam_email.apply_async((subscribe_form.instance.email,), countdown=60)
            return redirect('home')
        except ValueError:
            return render(request, 'foto/subscribe.html', {'form': SubscribeForm(), 'error': 'Ошибка'})


def moderation(request):
    # Вытаскиваем все объекты классов Фото и Категории
    fotos = Foto.objects.all()
    users = User.objects.all()
    #Фильтрация
    filtering = request.GET.get('filtering', '')

    if filtering == 'on_moderation':
        new_filter = []
        for item in fotos:
            if item.affected == False:
                new_filter.append(item)
    elif filtering == 'on_delete':
        new_filter = []
        for item in fotos:
            if item.deleted == True:
                new_filter.append(item)
    elif filtering == 'accepted':
        new_filter = []
        for item in fotos:
            if item.affected == True:
                new_filter.append(item)
    else:
        new_filter = fotos


    #Фильтрация по пользователям
    user = request.GET.get('user', '')
    if user:
        new_filter = Foto.objects.filter(user=user)
    else:
        print('Вывод всех фото')

    # Добавляем контекст
    context = {'Fotos': new_filter, 'Users': users}
    return render(request, 'foto/moderation.html', context)


def approve(request, foto_id):
    foto = get_object_or_404(Foto, pk=foto_id)
    if request.method == 'GET':
        foto.affected = True
        foto.save()
        print('Foto approved...')
        return redirect('moderation')


def dismiss(request, foto_id):
    foto = get_object_or_404(Foto, pk=foto_id)
    if request.method == 'GET':
        foto.dismissed = True
        foto.save()
        print('Foto dismissed...')
        return redirect('moderation')