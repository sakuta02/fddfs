from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomArticles, Genre, TagPost, News
import locale
from .forms import AddPostForm
from .utils import DataMixin
from django.contrib.auth import get_user_model
from users.models import User

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


# redirect Views --------------------------------------------------------
def news_url(request):
    return HttpResponseRedirect(redirect_to=reverse('news', args=(1, )))

# Отображение контента --------------------------------------------------


class NewsListView(DataMixin, ListView):
    model = News
    flag = 2
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, page=self.kwargs['page'])


class Articles(DataMixin, ListView):
    flag = 1
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
        return self.get_mixin_context(context, genre=self.kwargs['genre'], tag=self.request.GET.dict().get('tag'),
                                      page=self.kwargs['page'])


# Работа с кастомными записями ------------------------------------------

class ShowPost(DetailView):
    template_name = 'article.html'
    context_object_name = 'p'

    def get_object(self, queryset=None):
        return get_object_or_404(CustomArticles.published, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context['auth'] = CustomArticles.published.filter(slug=self.kwargs['slug'], author=self.request.user).exists()
        else:
            context['auth'] = False
        context['slug'] = self.kwargs['slug']
        return context


class AddPage(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'add_page.html'

    def form_valid(self, form):
        article = form.save(commit=False)  # Добавить валидатор для слага
        article.author = self.request.user
        return super().form_valid(form)


class EditPage(UpdateView):
    model = CustomArticles
    template_name = 'add_page.html'
    form_class = AddPostForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if CustomArticles.objects.filter(slug=self.kwargs['slug'], author=self.request.user).exists():
                return super().get(request, *args, **kwargs)
            else:
                raise Http404('У вас нету доступа к редактированию данной статьи')
        else:
            raise Http404('У вас нету доступа к редактированию данной статьи')


class DeletePage(DeleteView):
    template_name = 'delete_page.html'
    model = CustomArticles
    success_url = reverse_lazy('articles', args=('vse-kategorii', 1))

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if CustomArticles.objects.filter(slug=self.kwargs['slug'], author=self.request.user).exists():
                return super().get(request, *args, **kwargs)
            else:
                raise Http404('У вас нету доступа к редактированию данной статьи')
        else:
            raise Http404('У вас нету доступа к редактированию данной статьи')

# Профиль пользователя --------------------------------------------------


class ShowProfile(ListView):
    template_name = 'user.html'
    context_object_name = 'articles'
    model = CustomArticles
    paginate_by = 7

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['user'] = get_object_or_404(User, pk=self.kwargs['id'])
        if context['user'].photo:
            url_pic = context['user'].photo
        else:
            url_pic = r'../../aboba/img/profile.png'
        context['url_pic'] = url_pic
        return context

    def get_queryset(self):
        user = self.kwargs['id']
        sett = CustomArticles.objects.filter(author_id=user)
        if sett:
            return sett
        else:
            return CustomArticles.objects.none()

# -----------------------------------------------------------------------

