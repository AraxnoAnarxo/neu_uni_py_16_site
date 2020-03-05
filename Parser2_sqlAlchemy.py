from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bs4 import BeautifulSoup
import requests
import re

engine = create_engine('sqlite:///orm.sqlite', echo=True)

Base = declarative_base()

class Car(Base):
    __tablename__ = 'cars_02_sqlalchemy'
    id = Column(Integer, primary_key = True)
    car_name = Column(String)
    car_year = Column(Integer)

    def __init__(self, car_name, car_year):
        self.car_name = car_name
        self.car_year = car_year

    def __str__(self):
        return f'{self.id}, {self.car_name}, {self.car_year}'

class Price(Base):
    __tablename__ = 'price_02_sqlalchemy'
    id = Column(Integer, primary_key=True)
    car_price = Column(Integer)

    def __init__(self, car_price):
        self.car_price = car_price

    def __str__(self):
        return f'{self.id}, {self.car_price}'



Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()


def site_parsing_2():

    max_page = 40
    pages = []

    for x in range(1, max_page + 1):
        pages.append(requests.get('https://auto.drom.ru/bmw/x1/page' + str(x)))

    for n in pages:
        soup = BeautifulSoup(n.text, 'html.parser')

        car_name = soup.find_all('div', class_="b-advItem__title")

        for rev in car_name:
            a = str(rev.text)
            car = re.split(r',', a)
            car_name_sql = str(car[0])
            car_year = re.sub(r'[ ]', '', car[1])
            car_year_sql = int(car_year)

            car_obj = Car(car_name_sql, car_year_sql)
            session.add(car_obj)
            session.commit()



        price = soup.find_all('div', class_ = 'b-advItem__price b-advItem__price_mobile')
        pattern = r'(\d{1}\s\d{3}\s\d{3})|(\d{3}\s\d{3})'
        for rev in price:
            price_str = re.findall(pattern, rev.text)
            price_str = str(price_str)
            price_str = price_str.replace('\\xa0', '') # избавляемся от знаков \xa0
            price_str = re.sub(r"[\]['(),\s]", '', price_str)
            price_int = int(price_str)
            price_obj = Price(price_int)
            session.add(price_obj)
            session.commit()


site_parsing_2()

query = session.query(Car, Price)

query = query.join(Car, Car.id == Price.id)
records = query.all()

for obj1, obj2 in records:
    print(obj1,obj2)

