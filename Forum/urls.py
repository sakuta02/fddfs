from django.urls import path
from .views import news_view, news_url, article, articles, add_page

urlpatterns = [
    path('news/<int:page>/', news_view, name='news'),
    path('news/', news_url, name='main-url'),
    path('articles/post/<slug:slug>/', article, name='article'),
    path('articles/add_page/', add_page, name='add_page'),
    path('articles/<str:genre>/', articles, name='articles'),
]
