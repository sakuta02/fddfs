from django.urls import path
from .views import news_view, news_url, AddPage, Articles, ShowPost, EditPage, DeletePage

urlpatterns = [
    path('news/<int:page>/', news_view, name='news'),
    path('news/', news_url, name='main-url'),
    path('articles/post/<slug:slug>/', ShowPost.as_view(), name='article'),
    path('articles/add_page/', AddPage.as_view(), name='add_page'),
    path('articles/<str:genre>/', Articles.as_view(), name='articles'),
    path('articles/edit/<slug:slug>/', EditPage.as_view(), name='edit_page'),
    path('articles/delete/<slug:slug>/', DeletePage.as_view(), name='delete_page')
]
