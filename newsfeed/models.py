from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from .utils import fetch_articles
import datetime
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
    refreshedAt = models.DateTimeField()
    priority = models.BooleanField(default=False)

    def __str__(self):
        return self.tag_text

    def refresh_articles(self):
        fetch_articles(self.tag_text)
        self.refreshedAt = datetime.datetime.now()
        self.priority = False


class Article(models.Model):
    author = NoneToEmptyStringField(max_length=100, default='', blank=True, null=False)
    description = NoneToEmptyStringField(max_length=500, default='')
    title = models.CharField(max_length=200, unique=False, blank=False, null=False)
    url = models.URLField(unique=True)
    urlToImage = NoneToEmptyUrlField(default='')
    publishedAt = models.DateTimeField()
    displayed = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title[:100]

    def add_tag(self, tag_text):
        try:
            new_tag = Tag.objects.get(tag_text=tag_text)
        except ObjectDoesNotExist:
            new_tag = Tag(tag_text=tag_text)
            new_tag.save()
        self.tag.add(new_tag)




