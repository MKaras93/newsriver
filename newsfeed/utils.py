from .models import Article
from django.core.exceptions import ValidationError
import newsfeed.newsapi_feed as nf


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
            news = Article()
            news.create_from_dict(article)
            try:
                news.full_clean()
            except ValidationError:
                print('Skipping:', article['title'])
                skipped += 1
            else:
                news.save()
                loaded += 1

    print('Loaded - ' + str(loaded) + ' Skipped - ' + str(skipped))
