from django.shortcuts import render
from .models import Article, Tag
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from .utils import regular_refresh


# Create your views here.
def display_articles_set(request, query=''):
    query = query.lower()

    if query != '':
        art_set = Article.objects.filter(tag=query, displayed=False).order_by('-publishedAt')[:20]
        try:
            tag = Tag.objects.get(pk=query)
        except (ObjectDoesNotExist):
            tag = Tag(tag_text=query)
        finally:
            tag.priority = True
            tag.save()
    else:
        art_set = Article.objects.filter(displayed=False).order_by('-publishedAt')[:20]

    title = 'Unread articles - ' + query
    template = loader.get_template('newsfeed/newsfeed_template.html')
    context = {'arts': art_set,
               'title': title}
    resp = HttpResponse(template.render(context, request))
    Article.objects.filter(id__in=art_set).update(displayed=True)
    return resp


def refresh():
    regular_refresh()
    return 'refreshed'
