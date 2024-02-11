from django.urls import path
from .views import news_url, AddPage, Articles, ShowPost, EditPage, DeletePage, NewsListView

urlpatterns = [
    path('news/<int:page>/', NewsListView.as_view(), name='news'),
    path('news/', news_url, name='main-url'),
    path('articles/post/<slug:slug>/', ShowPost.as_view(), name='article'),
    path('articles/add_page/', AddPage.as_view(), name='add_page'),
    path('articles/<str:genre>/<int:page>', Articles.as_view(), name='articles'),
    path('articles/edit/<slug:slug>/', EditPage.as_view(), name='edit_page'),
    path('articles/delete/<slug:slug>/', DeletePage.as_view(), name='delete_page')
]
