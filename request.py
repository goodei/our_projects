import feedparser

from dateutil.parser import parse

from datetime import datetime,timedelta,timezone


PUBLISHED_TIME_LIMIT = 4 #hours
CONVERT_TO_OURS = 3600 #seconds

time_now = datetime.now()
time_now = time_now.replace(tzinfo=timezone.utc)


def par_habr_geek(url):
    parsing= feedparser.parse(url)
    if parsing.status == 200:
        posts = []
        for post in parsing.entries:
            if ((time_now - parse(post.published)).total_seconds())/CONVERT_TO_OURS < PUBLISHED_TIME_LIMIT:
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
            if (delta_time.total_seconds())/CONVERT_TO_OURS < PUBLISHED_TIME_LIMIT:
                news = {
                    'published':upd_time,
                    'title':post.title,
                    'link':post.link
                }
                posts.append(news)
        return sorted(posts,key= lambda x:x['published'],reverse = True)
            




    