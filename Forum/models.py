from django.db import models
from slugify import slugify
from django.urls import reverse


class PManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=1)


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    ref = models.TextField(verbose_name='Ссылка на оригинал')
    img_src = models.TextField(verbose_name='Ссылка на изображение')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    published = PManager()
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'


class CustomArticles(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = (0, 'Нет')
        PUBLISHED = (1, 'Да')
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, verbose_name='слаг')
    # img_src = models.TextField(blank=True, null=True, verbose_name='Путь до изображения')
    img = models.ImageField(verbose_name='фото', upload_to='custom_photos/%Y/%m', blank=True)
    created_by = models.CharField(max_length=255, verbose_name='Автор поста', default='admin')
    genre = models.ForeignKey('Genre', on_delete=models.PROTECT, null=True, verbose_name='Жанр')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.PUBLISHED, verbose_name='Опубликовано')
    text = models.TextField(verbose_name='Текст статьи')
    published = PManager()
    objects = models.Manager()
    tag = models.ManyToManyField(to='TagPost', blank=True, related_name='tags', verbose_name='Тэги')
    visits = models.IntegerField(default=0, verbose_name='Посещения')
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        url = reverse('article', kwargs={'slug': self.slug})
        return url

    class Meta:
        verbose_name = 'Пользовательские статьи'
        verbose_name_plural = 'Пользовательские статьи'


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Жанр')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Жанры'
        verbose_name_plural = 'Жанры'

    def get_absolute_url(self):
        url = reverse('articles', kwargs={'genre': self.slug})
        return url


class TagPost(models.Model):
    tag = models.CharField(max_length=128, verbose_name='Тэг')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.tag)
        super().save()

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тэги'
        verbose_name_plural = 'Тэги'
