from django.urls import path
from .views import news_url, AddPage, Articles, ShowPost, EditPage, DeletePage, NewsListView, ShowProfile, EditProfile

urlpatterns = [
    path('news/<int:page>/', NewsListView.as_view(), name='news'),
    path('news/', news_url, name='main-url'),
    path('articles/post/<slug:slug>/', ShowPost.as_view(), name='article'),
    path('articles/add_page/', AddPage.as_view(), name='add_page'),
    path('articles/<str:genre>/<int:page>', Articles.as_view(), name='articles'),
    path('articles/edit/<slug:slug>/', EditPage.as_view(), name='edit_page'),
    path('articles/delete/<slug:slug>/', DeletePage.as_view(), name='delete_page'),
    path('profile/<int:id>', ShowProfile.as_view(), name='profile'),
    path('profile/edit/<int:pk>', EditProfile.as_view(), name='edit_profile')
]

