from django import forms
from .models import CustomArticles, Genre, TagPost


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label='Заголовок статьи', widget=forms.TextInput(attrs={'class': 'art_title'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'art_content'}), label='Содержание статьи')
    genre = forms.ModelChoiceField(queryset=Genre.objects.exclude(slug='vse-kategorii'), label='Выбор жанра статьи', empty_label=None)
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), label='Выбор тэгов')
