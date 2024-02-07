from django import template
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from ..models import News, CustomArticles, Genre, TagPost
from math import ceil

register = template.Library()


@register.simple_tag()
def news(page):
    return Paginator(News.published.all(), 7).page(page)


@register.simple_tag()
def pages(page):
    pg = ceil(News.published.count() / 7)
    start = page - 3
    end = page + 5
    if start < 1:
        end -= start - 1
        start = 1
    elif end > pg:
        start = start + pg - end
        end = pg
    return range(start, end)


@register.simple_tag()
def articles(genre: None, tag: None):
    genre = get_object_or_404(Genre, slug=genre)
    if tag is not None:
        tag = get_object_or_404(TagPost, slug=tag)
        if genre.id != 1:
            return tag.tags.filter(genre=genre, is_published=1).select_related('genre').prefetch_related('tag')
        else:
            return tag.tags.filter(is_published=1).prefetch_related('tag')
    else:
        if genre.id != 1:
            return CustomArticles.published.filter(genre=genre).select_related('genre')
        else:
            return CustomArticles.published.all()


@register.simple_tag()
def genres():
    return Genre.objects.all()


@register.simple_tag()
def tags():
    return TagPost.objects.all()


@register.filter()
def to_(string):
    return ' | '.join(map(str, string.all()))
