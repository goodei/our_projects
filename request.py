import feedparser

from dateutil.parser import parse

from datetime import datetime,timedelta,timezone

from db_Users import db_session,Urls

from urllib.parse import urlparse

import redis


r = redis.Redis(host='localhost', port=6379, db=0)
time_now = datetime.now()
time_now = time_now.replace(tzinfo=timezone.utc)

"https://habrahabr.ru/rss/hubs/all/"
"https://geektimes.ru/rss/hubs/all/"

site = "https://habrahabr.ru/rss/hubs/all/"
site_2 = "http://static.feed.rbc.ru/rbc/logical/footer/news.rss"
site_3 = "https://geektimes.ru/rss/hubs/all/"


def par_habr_geek(url):
    parsing= feedparser.parse(url)
    if parsing.status == 200:
        posts = []
        for post in parsing.entries:
            if ((time_now - parse(post.published)).seconds)/3600 < 3:
                news = {
                    'published':parse(post.published),
                    'summary_detail':post.summary_detail['value'],
                    'title':post.title
                }
                posts.append(news)
        return sorted(posts,key= lambda x:x['published'],reverse = True)


def rbk(url):
    parsing= feedparser.parse(url)
    if parsing.status == 200:
        posts = []
        for post in parsing.entries:
            upd_time = datetime.strptime(post.published,'%a, %d %b %Y %X %z').replace(tzinfo=timezone.utc)
            delta_time = time_now - upd_time
            if (delta_time.total_seconds())/3600 <3:
                news = {
                    'published':upd_time,
                    'title':post.title,
                    'id':post.id
                }
                posts.append(news)
        return sorted(posts,key= lambda x:x['published'],reverse = True)

u_url = Urls
u_link = u_url.query.order_by(Urls.id).all()

            
if __name__ == "__main__":
    for link in u_link:
        part = urlparse(link.url)
        if part.netloc == 'static.feed.rbc.ru':
            r.set('Url:{}'.format(link.id),rbk(link.url))
        else:
            r.set('Url:{}'.format(link.id),par_habr_geek(link.url))



    