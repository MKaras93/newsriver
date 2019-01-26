from newsapi import NewsApiClient
import psycopg2
# from .models import Article
import json
# Init

#1. Collect data from query -> returns json with the data.
#2. Insert data into database/csv, recognising the same news. Same news are discarded.
#3. Get a collection of undisplayed news from db


def load_news(q='news'):
    newsapi = NewsApiClient(api_key='c644d0c6cff44d31a5180b9cc91c35bc')

    all_articles = newsapi.get_everything(language='en',
                                          q=q,
                                          sort_by='publishedAt',
                                          page_size=100,
                                          page=1)

    return all_articles


def save_articles(article_list, conn):
    # save article to database. No checks right now.
    command = """
        INSERT INTO fresh_news (author, description, title, url, urlToImage, publishedAt, displayed)
        VALUES (%(author)s, %(description)s, %(title)s, %(url)s, %(urlToImage)s, %(publishedAt)s, FALSE)
        """
    cur = conn.cursor()
    cur.executemany(command, article_list)
    cur.close()
    conn.commit()


def open_connection():
    return psycopg2.connect(dbname='news_db')


def create_table(conn):
    command = """
        DROP TABLE fresh_news;
        CREATE TABLE fresh_news(
            news_id SERIAL PRIMARY KEY,
             author VARCHAR(1000),
             description VARCHAR(1000),
             title VARCHAR(1000) NOT NULL,
             url VARCHAR(1000) NOT NULL,
             urlToImage VARCHAR(1000),
             publishedAt VARCHAR(1000),
             displayed boolean DEFAULT TRUE
        )"""

    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    con.commit()


"""
con = open_connection()
create_table(con)
articles = load_news()
articles = articles['articles']
save_articles(articles, con)
con.close()
"""

