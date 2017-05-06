#from sqlalchemy.orm import relationship
from db_Users import db_session, User, Urls, association_table    #имротируем из файла try_bd.py db_session(наше соед с бд)
                                        # и класс User
from sqlalchemy.dialects import sqlite

from db_Users import engine

#from db_Users import pub, priv

import rsa


def first_try():
    u = User            #объект класса User
    us = u.query.order_by(User.id).all()    # select all from User order by User.id
    for name in us:
        print(name.log_email)

    u_url = Urls
    us_tag = u_url.query.get(1)     # select * from Urls where Urls.id = 1

    print(us_tag.user_ass)          # select User.* from User, association, Urls 
                                    #               where Urls.id = 1 and association.User_id = User.id

    first_user = u.query.get(2)     # select Urls.* 
                                    # from User, association, Urls where User.id = 2 and association.Urls_id = Urls.id
    print(first_user.urls_ass)

#db_session.commit()

def user_association(e_mail, password):

    print ('in user_association!!!')
    u = User            #объект класса User
    us = u.query.filter(User.log_email == e_mail).first()    # select * from User where mail = e_mail
    print(us.id)
    url = Urls
    url_all = url.query.all()    # select * from User 
    for tag in url_all:
        print(tag.id)
        insert_stmt = association_table.insert().values(User_id = us.id, Urls_id = tag.id)
        conn = engine.connect()
        result = conn.execute(insert_stmt)
        
        

    #db_session.commit()



def create_log(e_mail, password):
    user = [e_mail, password]
    print(user)
    #u = User   
    #us = u.query.filter(User.log_email == e_mail).first()    # select * from User where mail = e_mail
    print(check_mail(e_mail))
    if not check_mail(e_mail):

        post_u = User(log_email = e_mail, password_u = password)
        db_session.add(post_u)
        db_session.commit()
        user_association(e_mail, password)
    else:
        print('user already exist')




def catch_tags(e_mail):
    u = User            #объект класса User
    #us = u.query.filter(User.log_email == e_mail).all()    # select * from User where mail = e_mail
    us = u.query.filter(User.log_email == e_mail).first()    # select * from User where mail = e_mail
    print('!!!!',us)
    #for name in us:
    print('!!!!', us.log_email)
    print('!!!!', us.id)
    print('!!!!', us.urls_ass)
    #us_id = us.urls_ass            #***Why it doesn't work? )
    #print ('!!!', us_id)           

    #u_url = Urls
    #us_tag = u_url.query.get(1)     # select * from Urls where Urls.id = 1

    #print(us_tag.user_ass)          # select User.* from User, association, Urls 
                                    #               where Urls.id = 1 and association.User_id = User.id

    #first_user = u.query.get(6)     # select Urls.* 
                                    # from User, association, Urls where User.id = 2 and association.Urls_id = Urls.id
    #print(first_user.urls_ass)      #*** AND Why it works? )
    return 'Catch success'




def check_mail(e_mail):
    u = User            #объект класса User
    user_mail = u.query.filter(User.log_email == e_mail).all()    
    



    return user_mail

def query_password(password, e_mail, priv):
    print('in qiery_password')
    u = User            #объект класса User
    user_mail = u.query.filter(User.log_email == e_mail).first()   # select * from User where mmail=mail
    if user_mail:
        user_password =  user_mail.password_u
        print(user_password)
        print(priv)
        password_un_crypto = rsa.decrypt(user_password, priv)
        return password_un_crypto == password
    return False

    
    

def check_password(e_mail, priv):
    while True:
        password = str(input('pls type your password: '))
        password_b =  str.encode(password) 
        #password_crypto = rsa.decrypt(crypto, priv)
        
        if query_password(password_b, e_mail, priv):
            print('Success')
            return True
        
        try_again = int(input('If try again put 1'))
        if try_again != 1:
            return False
    return False

def wr_file(attributes):
    print('write in file')
    with open('db_first.txt', 'w', encoding = 'utf-8') as f:
        for i in attributes:
            f.write(i)
            print(i)
            return True


def hello_user():
    print('Hi-Hi )')

    u = User            #объект класса User
    users_mail = u.query.all()  
    if users_mail:
        print('something')
        with open('private.pem', 'r') as privatefile:
            keydata = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(keydata)
        with open('public.pem', 'r') as publicfile:
            keydata_pub = publicfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(keydata_pub)

    else:
        print('nothing')
        (pubkey, privkey) = rsa.newkeys(512)
        pub = pubkey.save_pkcs1()
        priv = privkey.save_pkcs1()
        with open('private.pem', 'w') as f:
            f.write(priv.decode('utf-8'))
        with open('public.pem', 'w') as f:
            f.write(pub.decode('utf-8'))

        #create_log(pub, priv)
        #user_mail = u.query.get(1)
        #pub = user_mail.log_email
        #priv = user_mail.password_u

   # (pubkey, privkey) = rsa.newkeys(512)

    #pub = pubkey
    #priv = privkey
    # print('KEYS')
    #print(pub)
    #print(priv)
     
        
    # шифруем
    #crypto = rsa.encrypt(message, pub)
    #print(crypto)
    #расшифровываем
    #message = rsa.decrypt(crypto, priv)
    #print(message)


    flag_sign = int(input('If you are a already signed in, print 1 if no 0: '))

    if flag_sign == 1:
        e_mail = str(input('pls enter in account, type your e-mail: '))
        if check_mail(e_mail):
            print(check_mail(e_mail))
            if check_password(e_mail, privkey):
                print(catch_tags(e_mail))
            

        else:
            e_mail = str(input('pls try again enter in account, type your e-mail: '))
            if check_mail(e_mail):
                print(check_mail(e_mail))
            else:
                print('we can not find your mail, pls sign again', e_mail)
    else:
        print('Ok, letss create new log!')
        e_mail = str(input('pls type your e-mail: '))
        password = str(input('pls type your pass: '))
        password_b = str.encode(password)               #перевод строки в bytes
        print(password_b)
        password_crypto = rsa.encrypt(password_b, pubkey)  # шифруем открытым ключом
        password_un_crypto = rsa.decrypt(password_crypto, privkey)  # шифруем открытым ключом
        #print(password_un_crypto)

        create_log(e_mail, password_crypto)             # создаём запись о user в бд



    print('Bi-Bi-Bi')



def main():
   # first_try()
    hello_user()

main()