from django.db import models

# Create your models here.


def unnull(val):
    return val if isinstance(val, str) else ''


class Tag(models.Model):
    tag_text = models.CharField(max_length=30, primary_key=True)
    refresh_freq = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.tag_text


class Article(models.Model):
    author = models.CharField(max_length=100, default='', blank=True, null=False)
    description = models.CharField(max_length=500, default='')
    title = models.CharField(max_length=200, unique=True, blank=False, null=False)
    url = models.URLField(unique=True)
    urlToImage = models.URLField(default='')
    publishedAt = models.DateTimeField()
    displayed = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag)

    def create_from_dict(self, dict_):
        self.author = unnull(dict_['author'])
        self.description = unnull(dict_['description'])
        self.title = dict_['title']
        self.url = dict_['url']
        self.urlToImage = unnull(dict_['urlToImage'])
        self.publishedAt = dict_['publishedAt']
        self.displayed = False

    def __str__(self):
        return self.title[:100]

    def add_tag(self, tag_text):
        tag = Tag.objects.get(tag_text)
        self.tag = tag



