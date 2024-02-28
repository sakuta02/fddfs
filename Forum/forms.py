from django import forms
from slugify import slugify
from .models import CustomArticles, Genre, TagPost, Comment
from django.contrib.auth import get_user_model


class AddPostForm(forms.ModelForm):
    genre = forms.ModelChoiceField(queryset=Genre.objects.exclude(slug='vse-kategorii'), label='Выбор жанра статьи',
                                   empty_label=None)
    tag = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), label='Доступные тэги')

    class Meta:
        model = CustomArticles
        fields = ('title', 'text', 'img', 'genre', 'tag')
        widgets = {'title': forms.TextInput(attrs={'class': 'art_title'}),
                   'text': forms.Textarea(attrs={'class': 'art_content'})}
        labels = {'title': 'Заголовок статьи:', 'text': 'Содержание статьи:',
                  'img': 'Вы можете загрузить фотографию к посту'}

    def clean_title(self):
        if CustomArticles.objects.filter(slug=slugify(self.cleaned_data['title'])).exists():
            raise forms.ValidationError(
                'Статья с таким слагом уже существует! Возможно вам поможет небольшое изменение заголовка')
        return self.cleaned_data['title']


class EditProfileModel(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'photo')
        labels = {'username': 'Имя пользователя - логин аккаунта', 'email': 'Электронная почта',
                  'photo': 'Фото профиля'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        labels = {'text': 'Ваш комментарий'}

