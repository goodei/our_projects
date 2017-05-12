from sqlalchemy import create_engine

from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Text, DateTime, ForeignKey

# sqlalchemy синхронизирует наш объект в программном коде с записью в бд



engine = create_engine('sqlite:///rss.sqlite') # создаём engin - выбираем с какой бд будем работать. 
                                                # Будем работать с Sqlite и файл с базой будет blog.sqlite в той же папке где и прога
db_session = scoped_session(sessionmaker(bind=engine))  #создаём сессию работы с бд, это соединение с бд
                                                        # в это соед мы будем отправлять наши данные и получать
Base = declarative_base()   # создаём класс с названием Base - мы создаём деклоративный класс и мы опишем структуру таблиц
                            # в питон коде и будем потом работать с ней как с питон кодом
Base.query = db_session.query_property()     # привязываем к declarative_base возмоэность делать запросы к бд


association_table = Table('association_table', Base.metadata,
    Column('User_id', Integer, ForeignKey('User.id')),
    Column('Urls_id', Integer, ForeignKey('Urls.id'))
)




class User(Base):       #объявляем нашу таблицу как класс User и наследуем его от класса Base
                        # класс User будет обладать всеми вохможностями которыми обладает класс Base, а он может то, что 
                        # может класс declarative_base из Sqlalchemy 
    __tablename__ = 'User'     # атрибут класса tablename - как нашей бд газвать таблицу, 
                                # ниже создаём столбцы для этой таблицы
    id = Column(Integer, primary_key = True)    # у класса Users будет атрибут(колонка в табл id)
    log_email = Column(String(50), unique = True)  # тут unique значит, что бд будет сама проверять уникальность 
    password_u = Column(String(70))
    urls = relationship('Urls', secondary=association_table, backref ='user_ass')
    
       

    def __repr__(self):   #   метод, если мы сделаем print(User), то смотри ниже формат печати
        return '<User {} {}>'.format(self.log_email, self.password_u)

class Urls(Base):       #объявляем нашу таблицу как класс User и наследуем его от класса Base
                        # класс User будет обладать всеми вохможностями которыми обладает класс Base, а он может то, что 
                        # может класс declarative_base из Sqlalchemy 
    __tablename__ = 'Urls'     # атрибут класса tablename - как нашей бд газвать таблицу, 
                                # ниже создаём столбцы для этой таблицы
    id = Column(Integer, primary_key = True)    # у класса Users будет атрибут(колонка в табл id)
    url = Column(String(50))
    tag = Column(String(120)) 
    user = relationship('User', secondary=association_table, backref ='urls_ass') 

    
    def __repr__(self):   #   метод, если мы сделаем print(Urls), то смотри ниже формат печати
        return '<Url {} {}>'.format(self.url, self.tag)



        

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)