#from sqlalchemy.orm import relationship
from db_Users import db_session, User, Urls    #имротируем из файла try_bd.py db_session(наше соед с бд)
                                        # и класс User


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

def create_log(e_mail, password):
    user = [e_mail, password]
    print(user)

    post_u = User(log_email = e_mail, password_u = password)

    db_session.add(post_u)
    db_session.commit()



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

    u_url = Urls
    us_tag = u_url.query.get(1)     # select * from Urls where Urls.id = 1

    print(us_tag.user_ass)          # select User.* from User, association, Urls 
                                    #               where Urls.id = 1 and association.User_id = User.id

    first_user = u.query.get(2)     # select Urls.* 
                                    # from User, association, Urls where User.id = 2 and association.Urls_id = Urls.id
    print(first_user.urls_ass)      #*** AND Why it works? )
    return 'Catch success'




def check_mail(e_mail):
    u = User            #объект класса User
    user_mail = u.query.filter(User.log_email == e_mail).all()    
    



    return user_mail

def query_password(password, e_mail):
    u = User            #объект класса User
    user_mail = u.query.filter(User.log_email == e_mail).first()   # select * from User where mmail=mail
    if user_mail:
        return user_mail.password_u == password
    return False

    
    

def check_password(e_mail):
    while True:
        password = str(input('pls type your password: '))
        if query_password(password, e_mail):
            print('Success')
            return True
        
        try_again = int(input('If try again put 1'))
        if try_again != 1:
            return False
    return False





def hello_user():
    print('Hi-Hi )')
    flag_sign = int(input('If you are a already signed in, print 1 if no 0: '))

    if flag_sign == 1:
        e_mail = str(input('pls enter in account, type your e-mail: '))
        if check_mail(e_mail):
            print(check_mail(e_mail))
            if check_password(e_mail):
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
        create_log(e_mail, password)



    print('Bi-Bi-Bi')



def main():
    first_try()
    hello_user()

main()