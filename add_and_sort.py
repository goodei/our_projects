import redis

from request import rbk,par_habr_geek

from db_Users import db_session,Urls

from urllib.parse import urlparse

import json

from encoder import MyEncoder,decode

from settings import REDIS_SETTINGS


r = redis.Redis(**REDIS_SETTINGS)

def save_to_r(link_adr,func):
    load = get_from_r(link_adr)
    new_data = func(link_adr.url)
    if load:
        old_date_max = load[0]['published']
        new_articles = [x for x in new_data if x['published'] > old_date_max]
        result_articles = new_articles + load
        new_data = result_articles[:10]
    r.set('Url:{}'.format(link_adr.id),json.dumps(new_data, cls = MyEncoder))
    
        

def get_from_r(link_adr):
    data = r.get('Url:{}'.format(link_adr.id))
    if data is None:
        return []
    return json.loads(data.decode('utf-8'), object_hook = decode)


def sequence_save():
    u_url = Urls
    u_link = u_url.query.order_by(Urls.id).all()
    for link in u_link:
        part = urlparse(link.url)
        site = link
        if part.netloc == 'static.feed.rbc.ru':
            save_to_r(site,rbk)
        else:
            save_to_r(site,par_habr_geek)



if __name__ == "__main__":
    sequence_save()


    # for link in u_link:
    #     print('Cайт :{} + ВНУТРИ : {} \n'.format(link,get_from_r(link)))


