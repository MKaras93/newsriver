from .models import Article
from django.core.exceptions import ValidationError
import newsfeed.newsapi_feed as nf


def drop_unused_keys(article):
    """drops the keys which are not used by Article model."""
    used_keys = [atr.name for atr in Article._meta.get_fields()]

    for key in list(article):
        if key not in used_keys:
            article.pop(key, None)
    return


def fetch_articles(q='news', q_list=''):
    skipped = 0
    art_count = 0
    loaded = 0
    if not q_list:
        q_list = [q]

    for query in q_list:
        all_articles = nf.load_news(query)
        articles_list = all_articles['articles']

        for article in articles_list:
            art_count += len(articles_list)
            drop_unused_keys(article)

            # assumption: if article has a new url, it's a new article TODO: same articles published by different source
            news, created = Article.objects.update_or_create(
                url=article['url'],
                defaults=article)

            if not created:
                print('Skipping:', article['title'])
                skipped += 1
            else:
                loaded += 1

            # try:
            #     news.full_clean()
            # except ValidationError:
            #     pass
            # else:
            #     news.save()
            #     loaded += 1
            news.add_tag(query)

    return 'Loaded - ' + str(loaded) + ' Skipped - ' + str(skipped)
