from newsfeed.models import Article
import newsfeed.newsapi_feed as nf


def fetch_articles(q='news'):
    all_articles = nf.load_news(q)
    articles_list = all_articles['articles']

    for article in articles_list:
        news = Article()
        news.create_from_dict(article)
        news.save()
    print(str(len(articles_list)) + ' articles loaded.')
