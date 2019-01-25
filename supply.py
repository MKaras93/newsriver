from newsapi import NewsApiClient
import psycopg2
import json
# Init

#1. Collect data from query -> returns json with the data.
#2. Insert data into database/csv, recognising the same news. Same news are discarded.
#3. Get a collection of undisplayed news from db


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

def was_news_loaded(news):
    """returns true if news is already in the database"""
    # can be done in database or before loading. If before loading, I have to extract similiar data
    # news was loaded if url or (headline and source and publication date) are same in old and new.
    # should be done on SQL side, insert into with conditions
    # let's setup a postgres db.


def db_connect():
    conn = psycopg2.connect(dbname='news', user='postgres', password='postgres')
    return conn