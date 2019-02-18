from django.shortcuts import render
from .models import Article
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def display_articles_set(request, query=''):
    query=query.lower()
    if query != '':
        art_set = Article.objects.filter(tag=query, displayed=False).order_by('-publishedAt')[:20]
    else:
        art_set = Article.objects.filter(displayed=False).order_by('-publishedAt')[:20]

    title = 'Unread articles - ' + query
    template = loader.get_template('newsfeed/newsfeed_template.html')
    context = {'arts': art_set,
               'title': title}
    resp = HttpResponse(template.render(context, request))
    Article.objects.filter(id__in=art_set).update(displayed=True)
    return resp
