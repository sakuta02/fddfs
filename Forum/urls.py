from django.urls import path
from .views import news_view, news_url, article, articles

urlpatterns = [
    path('news/<int:page>/', news_view, name='news'),
    path('news/', news_url, name='main-url'),
    path('article/post/<slug:slug>/', article, name='article'),
    path('article/<str:genre>/', articles, name='articles'),
]
