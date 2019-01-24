from newsapi import NewsApiClient
import json
# Init

def load_news():
    newsapi = NewsApiClient(api_key='c644d0c6cff44d31a5180b9cc91c35bc')

    # /v2/top-headlines
    # top_headlines = newsapi.get_top_headlines(q='bitcoin',
    #                                           sources='bbc-news,the-verge',
    #                                           category='business',
    #                                           language='en',
    #                                           country='us')

    # /v2/everything
    all_articles = newsapi.get_everything(language='en',
                                          q='news',
                                          sort_by='publishedAt',
                                          page_size=100,
                                          page=1)

    return all_articles


def print_articles(news):
    for article in news['articles']:
        print(article['publishedAt'] + ' - ' + article['title'] + '\n')
