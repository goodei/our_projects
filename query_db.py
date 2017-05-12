#from sqlalchemy.orm import relationship
from db_Users import db_session, User, Urls, association_table    #имротируем из файла try_bd.py db_session(наше соед с бд)
                                        # и класс User
from sqlalchemy.dialects import sqlite

from db_Users import engine

#from db_Users import pub, priv

import rsa



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




def catch_tags(e_mail):     # если пользователь существует, забирает его urls
    u = User            #объект класса User
    #us = u.query.filter(User.log_email == e_mail).all()    # select * from User where mail = e_mail
    us = u.query.filter(User.log_email == e_mail).first()    # select * from User where mail = e_mail
    
    return us.urls_ass




def check_mail(e_mail):
    u = User            #объект класса User
    user_mail = u.query.filter(User.log_email == e_mail).first()    
    return user_mail

def query_password(password, e_mail, priv):
    print('in qiery_password')
    u = User            #объект класса User
    user_mail = u.query.filter(User.log_email == e_mail).first()   # select * from User where mmail=mail
    if user_mail:
        user_password =  user_mail.password_u
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


def crypto(user_existence):
    users_mail = user_existence
    keys = []

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

    keys.append(privkey)
    keys.append(pubkey)
    
    return keys

def input_from_cons(privkey, pubkey):

    flag_sign = int(input('If you are a already signed in, print 1 if no 0: '))

    if flag_sign == 1:
        e_mail = str(input('pls enter in account, type your e-mail: '))
        if check_mail(e_mail):                                          # проверяем наличие в б.д. такого юзера
            #print(check_mail(e_mail))
            if check_password(e_mail, privkey):                         # сверяем его пароль
                print(catch_tags(e_mail))                               # выводим связанные с ним urls
            

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

        create_log(e_mail, password_crypto)             # создаём запись о user в бд



def hello_user():       # отсюда вызываем функцию шифрования и функцию консольного ввода
    print('Hi-Hi )')
    keys = []

    u = User            #объект класса User
    users_mail = u.query.all()  
    keys = crypto(users_mail)       # вызов функции отвечающей за создание ключей для шифрования
    privkey = keys[0]               # собственно полученный приватный ключ для шифрования
    pubkey = keys[1]                # публичный ключ для дешифрования

    
    input_from_cons(privkey, pubkey)    # вызов функции консольного ввода, отсюда дёргаем всё остальное


    print('Bi-Bi-Bi')



def main():
   
    hello_user()

if __name__ == '__main__':
    main()

