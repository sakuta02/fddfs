from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import CustomArticles, News, Genre
from django.db.models import F
import datetime
import locale
from .forms import AddPostForm
from slugify import slugify

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

def news_view(request, page):
    return render(request, 'news.html', context={'page': page})


def news_url(request):
    return HttpResponseRedirect(redirect_to=reverse('news', args=(1, )))


def article(request, slug):
    post = get_object_or_404(CustomArticles, slug=slug)
    date: datetime = post.created_at
    date = date.strftime('%d.%m.%Y в %H:%M')
    post.visits = post.visits + 1
    post.save()
    return render(request, 'article.html', context={'p': post, 'date': date})


def articles(request, genre: None):
    tag = request.GET.dict().get('tag')
    return render(request, 'articles.html', context={'genre': genre, 'tag': tag})


def add_page(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                form.instance.img = request.FILES['img']
                form.save()
                return HttpResponseRedirect(reverse('articles', args=['vse-kategorii']))
            except Exception as e:
                form.add_error(None, 'Ошибка при добавлении статьи. Возможно вы указали заголовок, который уже существует')
        return render(request, 'add_page.html', {'form': form})
    else:
        form = AddPostForm()
        return render(request, 'add_page.html', {'form': form})


def save_image(name, img):
    with open(fr'Forum/static/img/{name}-{img.name}', 'wb+') as f:
        for chunk in img.chunks():
            f.write(chunk)