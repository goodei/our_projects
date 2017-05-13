from flask import Flask, render_template, Response, redirect, url_for, request, session, abort, flash
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_Users import db_session, User, Urls
from query_db import crypto, check_password, query_password
from add_and_sort import get_from_r
#import rsa

engine = create_engine('sqlite:///rss.sqlite')

my_flask_app = Flask(__name__)


@my_flask_app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        u = User
        e_mail = session.get('e_mail')
        us = u.query.filter(User.log_email == e_mail).first()
        taglist = []
        for i in us.urls_ass:
            taglist.append(i.tag)
        statii=[]
        for link in us.urls_ass:
            articles = get_from_r(link)
            for a in articles:
                a['source'] = link.tag
            statii += articles
        statii = sorted(statii,key= lambda x:x['published'],reverse = True)



        return render_template('index.html', taglist=taglist, statii = statii)
        # teglist = get_from_r(str(urls.querry.filter)) # создать запрос который будет выдавать список тегов, создать словарь по содержимому


@my_flask_app.route('/login', methods=['POST'])
def login():
    u = User
    e_mail = str(request.form['username'])
    passwd = str(request.form['password'])
    password_b =  str.encode(passwd)
    users_mail = u.query.all()  
    keys = crypto(users_mail)
    priv = keys[0]               # собственно полученный приватный ключ для шифрования
    pubkey = keys[1]
    qry_login = u.query.filter(User.log_email == e_mail).first()
    if qry_login is None:
        flash('No such user or invalid password')
    else: 
        if query_password(password_b, e_mail, priv) == True:
            session['logged_in'] = True
            session['e_mail'] = e_mail
            return home()
        else:
            return home() # вывести кнопку регистрации

    


@my_flask_app.route("/logout", methods=['POST'])
def logout():
    session['logged_in'] = False
    return home()


if __name__ == "__main__":
    my_flask_app.secret_key = os.urandom(20)
    my_flask_app.run(debug=True)