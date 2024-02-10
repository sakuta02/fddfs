from django import forms

from .models import CustomArticles, Genre, TagPost


class AddPostForm(forms.ModelForm):
    genre = forms.ModelChoiceField(queryset=Genre.objects.exclude(slug='vse-kategorii'), label='Выбор жанра статьи',
                                   empty_label=None)
    tag = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), label='Доступные тэги')

    class Meta:
        model = CustomArticles
        fields = ('title', 'text', 'img', 'genre', 'tag')
        widgets = {'title': forms.TextInput(attrs={'class': 'art_title'}),
                   'text': forms.Textarea(attrs={'class': 'art_content'})}
        labels = {'title': 'Заголовок статьи:', 'text': 'Содержание статьи:', 'img': 'Вы можете загрузить фотографию к посту'}
