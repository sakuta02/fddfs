from django.contrib import admin, messages
from .models import CustomArticles, News, Genre, TagPost


@admin.register(CustomArticles)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at', 'slug', 'visits']
    list_display = ('id', 'title', 'genre', 'created_at', 'updated_at', 'is_published', 'brief_info')
    list_display_links = ('id', 'title')
    ordering = ('-updated_at', )
    list_editable = ('is_published', 'genre')
    actions = ['set_published', 'set_unpublished']
    search_fields = ['title', 'genre__name']
    list_filter = ['genre', 'is_published']

    @admin.display(description='Длина')
    def brief_info(self, customarticle: CustomArticles):
        return f'{len(customarticle.text)} символов'

    @admin.action(description='Опубликовать')
    def set_published(self, request, queryset):
        queryset.update(is_published=CustomArticles.Status.PUBLISHED)
        self.message_user(request, f'Опубликованно {queryset.count()} записей')

    def get_queryset(self, request):
        return CustomArticles.objects.all()

    @admin.action(description='Снять с публикации')
    def set_unpublished(self, request, queryset):
        queryset.update(is_published=CustomArticles.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {queryset.count()} записей', messages.WARNING)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'is_published')
    list_display_links = ('id', 'title')
    list_editable = ('is_published', )
    search_fields = ('title', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')
