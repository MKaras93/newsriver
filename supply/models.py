from django.db import models

# Create your models here.


class Article(models.Model):
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    title = models.CharField(max_length=200)
    url = models.URLField()
    urlToImage = models.URLField()
    publishedAt = models.DateTimeField()
    displayed = models.BooleanField(default=False)

def new