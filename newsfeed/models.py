from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime
import os
import sys
from newsapi import NewsApiClient
# Create your models here.


class NoneToEmptyStringField(models.CharField):
    def get_prep_value(self, value):
        if value is None:
            return ''
        return value


class NoneToEmptyUrlField(models.URLField):
    def get_prep_value(self, value):
        if value is None:
            return ''
        return value


class Tag(models.Model):
    tag_text = models.CharField(max_length=30, primary_key=True)
    refresh_freq = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=True)
    refreshedAt = models.DateTimeField(null=True)
    priority = models.BooleanField(default=False)

    def __str__(self):
        return self.tag_text

    def refresh_articles(self):
        art_list = download_articles(self.tag_text)
        load_articles(art_list, self.tag_text)
        self.refreshedAt = timezone.now()
        self.priority = False
        self.save()


class Article(models.Model):
    author = NoneToEmptyStringField(max_length=100, default='', blank=True, null=False)
    description = NoneToEmptyStringField(max_length=500, default='')
    title = models.CharField(max_length=500, unique=False, blank=False, null=False)
    url = models.URLField(unique=True, max_length=500)
    urlToImage = NoneToEmptyUrlField(default='', max_length=500)
    publishedAt = models.DateTimeField()
    displayed = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title[:100]

    def add_tag(self, tag_text):
        tag_text=tag_text.lower()
        try:
            new_tag = Tag.objects.get(tag_text=tag_text)
        except ObjectDoesNotExist:
            new_tag = Tag(tag_text=tag_text)
            new_tag.save()
        self.tag.add(new_tag)


def download_articles(q='news'):
    q = q.lower()
    newsapi = NewsApiClient(api_key=NA_KEY)

    all_articles = newsapi.get_everything(language='en',
                                          q=q,
                                          sort_by='publishedAt',
                                          page_size=100,
                                          page=1)
    articles_list = all_articles['articles']
    return articles_list


def load_articles(articles_list, tag=''):
    tag = tag.lower()
    art_count = 0
    skipped = 0
    loaded = 0
    for article in articles_list:
        art_count += len(articles_list)
        
        # dropping unused keys:
        used_keys = [atr.name for atr in Article._meta.get_fields()]
        for key in list(article):
            if key not in used_keys:
                article.pop(key, None)

        # assumption: if article has a new url, it's a new article TODO: same articles published by different source

        news, created = Article.objects.update_or_create(
            url=article['url'],
            defaults=article)

        if not created:
            # print('Skipping:', article['title'])
            skipped += 1
        else:
            loaded += 1

        news.add_tag(tag)

    print('Refreshing tag ' + tag + ': Loaded - ' + str(loaded) + ' Skipped - ' + str(skipped))
    return


try:
    NA_KEY = os.environ["NA_KEY"]
except KeyError:
    print("Get Newsapi key and set it as NA_KEY environment variable.")
    # sys.exit(1)
