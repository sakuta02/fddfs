from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomArticles, Genre, TagPost, News, Comment
import locale
from .forms import AddPostForm, EditProfileModel, CommentForm, EditForm
from .utils import DataMixin
from django.contrib.auth import get_user_model
from users.models import User

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


# redirect Views --------------------------------------------------------
def news_url(request):
    return HttpResponseRedirect(redirect_to=reverse('news', args=(1,)))


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

    def get_queryset(self, *args, **kwargs):
        genre = get_object_or_404(Genre, slug=self.kwargs['genre'])
        tag_slug = self.request.GET.get('tag')
        search = self.request.GET.get('search')

        if genre.id == 1:
            articles = CustomArticles.published.all()
        else:
            articles = CustomArticles.published.filter(genre=genre).select_related('genre')

        if tag_slug:
            tag = get_object_or_404(TagPost, slug=tag_slug)
            articles = articles.filter(tag=tag, is_published=1).prefetch_related('tag')

        if search:
            articles = articles.filter(title__icontains=search)

        return articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return self.get_mixin_context(context, genre=self.kwargs['genre'], tag=self.request.GET.dict().get('tag'),
                                      page=self.kwargs['page'])


# Работа с кастомными записями ------------------------------------------

class ShowPost(LoginRequiredMixin, CreateView):
    template_name = 'article/show_article.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context['auth'] = CustomArticles.published.filter(slug=self.kwargs['slug'],
                                                              author=self.request.user).exists()
        else:
            context['auth'] = False
        context['slug'] = self.kwargs['slug']
        post = get_object_or_404(CustomArticles.published, slug=self.kwargs['slug'])
        context['p'] = post
        context['comments'] = Comment.objects.filter(post=post)
        return context

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.post = get_object_or_404(CustomArticles, slug=self.kwargs['slug'])
        return super().form_valid(form)


class AddPage(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'article/add_article.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        return super().form_valid(form)


class EditPage(UpdateView):
    model = CustomArticles
    template_name = 'article/add_article.html'
    form_class = EditForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if CustomArticles.objects.filter(slug=self.kwargs['slug'], author=self.request.user).exists():
                return super().get(request, *args, **kwargs)
            else:
                raise Http404('У вас нету доступа к редактированию данной статьи')
        else:
            raise Http404('У вас нету доступа к редактированию данной статьи')


class DeletePage(DeleteView):
    template_name = 'article/delete_article.html'
    model = CustomArticles
    success_url = reverse_lazy('articles', args=('vse-kategorii', 1))

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if CustomArticles.objects.filter(slug=self.kwargs['slug'], author=self.request.user).exists():
                return super().get(request, *args, **kwargs)
            else:
                raise Http404('У вас нету доступа к редактированию данной страницы')
        else:
            raise Http404('У вас нету доступа к редактированию данной страницы')


# Профиль пользователя --------------------------------------------------


class ShowProfile(ListView):
    template_name = 'user/show_user.html'
    context_object_name = 'articles'
    model = CustomArticles
    paginate_by = 7

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['user'] = get_object_or_404(User, pk=self.kwargs['id'])
        if context['user'].photo:
            url_pic = '/static/' + str(context['user'].photo)
        else:
            url_pic = r'/static/images/profile.png'
        context['url_pic'] = url_pic
        return context

    def get_queryset(self):
        sett = CustomArticles.objects.filter(author_id=self.kwargs['id'])
        if sett:
            return sett
        else:
            return CustomArticles.objects.none()


# -----------------------------------------------------------------------


class EditProfile(UpdateView):
    template_name = 'user/edit_user.html'
    model = get_user_model()
    form_class = EditProfileModel
    success_url = reverse_lazy('articles', args=('vse-kategorii', 1))

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user = self.request.user
            if get_object_or_404(get_user_model(), pk=self.kwargs['pk']) == user:
                return super().get(request, *args, **kwargs)
            else:
                raise Http404('У вас нету доступа к редактированию данной страницы')
        else:
            raise Http404('У вас нету доступа к редактированию данной страницы')
