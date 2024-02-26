from .models import CustomArticles
from django.http import Http404
from django.views.generic import View


class DataMixin:
    flag = None
    paginate_by = 7

    def get_mixin_context(self, context, **kwargs):
        if self.flag == 1:
            context.update(kwargs)
            return context
        elif self.flag == 2:
            context.update(kwargs)
            return context


class CheckUserMixin(View):

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if CustomArticles.objects.filter(slug=self.kwargs['slug'], author=self.request.user).exists():
                return super().get(request, *args, **kwargs)
            else:
                raise Http404('У вас нету доступа к редактированию данной страницы')
        else:
            raise Http404('У вас нету доступа к редактированию данной страницы')
