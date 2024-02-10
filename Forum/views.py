from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import CustomArticles, Genre, TagPost
import locale
from .forms import AddPostForm

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def news_view(request, page):
    return render(request, 'news.html', context={'page': page})


def news_url(request):
    return HttpResponseRedirect(redirect_to=reverse('news', args=(1,)))


class ShowPost(DetailView):
    template_name = 'article.html'
    context_object_name = 'p'

    def get_object(self, queryset=None):
        return get_object_or_404(CustomArticles.published, slug=self.kwargs['slug'])


class Articles(ListView):
    template_name = 'articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        genre = get_object_or_404(Genre, slug=self.kwargs['genre'])
        tag = self.request.GET.get('tag')
        if tag is not None:
            tag = get_object_or_404(TagPost, slug=tag)
            if genre.id != 1:
                return tag.tags.filter(genre=genre, is_published=1).select_related('genre').prefetch_related('tag')
            else:
                return tag.tags.filter(is_published=1).prefetch_related('tag')
        else:
            if genre.id != 1:
                return CustomArticles.published.filter(genre=genre).select_related('genre')
            else:
                return CustomArticles.published.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['genre'] = self.kwargs['genre']
        context['tag'] = self.request.GET.dict().get('tag')
        return context


# Работа с кастомными записями ------------------------------------------
class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'add_page.html'

    def form_valid(self, form):
        form.save()  # Добавить валидатор для слага
        return super().form_valid(form)


class EditPage(UpdateView):
    model = CustomArticles
    template_name = 'add_page.html'
    fields = ['title', 'text', 'img', 'genre', 'tag']  # Изменить этот вью!


class DeletePage(DeleteView):
    template_name = 'delete_page.html'
    model = CustomArticles
    success_url = reverse_lazy('articles', args=('vse-kategorii',))

# -----------------------------------------------------------------------
