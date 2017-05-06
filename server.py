from flask import Flask, render_template, Response, redirect, url_for, request, session, abort, flash
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_Users import db_session, User, Urls

engine = create_engine('sqlite:///rss.sqlite')

my_flask_app = Flask(__name__)


@my_flask_app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('index.html')


@my_flask_app.route('/login', methods=['POST'])
def login():
    u = User
    e_mail = str(request.form['username'])
    passwd = str(request.form['password'])
    qry_login = u.query.filter(User.log_email == e_mail, User.password_u == passwd).first()
    if qry_login is None:
    	flash('No such user or invalid password')
    else: 
    	session['logged_in'] = True
    return home()


@my_flask_app.route("/logout", methods=['POST'])
def logout():
    session['logged_in'] = False
    return home()


if __name__ == "__main__":
	my_flask_app.secret_key = os.urandom(20)
	my_flask_app.run(debug=True)