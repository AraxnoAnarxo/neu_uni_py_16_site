from bs4 import BeautifulSoup
import requests
import re
import sqlite3 as lite
import sys

def site_parsing_2():

    max_page = 40
    pages = []
    id_n = 0
    id_n_1 = 0

    for x in range(1, max_page + 1):
        pages.append(requests.get('https://auto.drom.ru/bmw/x1/page' + str(x)))

    for n in pages:
        soup = BeautifulSoup(n.text, 'html.parser')

        car_name = soup.find_all('div', class_="b-advItem__title")

        for rev in car_name:
            id_n+=1
            a = str(rev.text)
            car = re.split(r',', a)
            car_name_sql = str(car[0])
            car_year = re.sub(r'[ ]', '', car[1])
            car_year_sql = int(car_year)


            cur.execute("INSERT INTO car_parsing_1 VALUES(?,?,?)",(id_n, car_name_sql, car_year_sql))

        price = soup.find_all('div', class_ = 'b-advItem__price b-advItem__price_mobile')
        pattern = r'(\d{1}\s\d{3}\s\d{3})|(\d{3}\s\d{3})'
        for rev in price:
            id_n_1 += 1
            price_str = re.findall(pattern, rev.text)
            price_str = str(price_str)
            price_str = price_str.replace('\\xa0', '') # избавляемся от знаков \xa0
            price_str = re.sub(r"[\]['(),\s]", '', price_str)
            price_int = int(price_str)
            cur.execute("INSERT INTO car_parsing_1_price VALUES(?,?)", (id_n_1, price_int))

connect = None

try:
    connect = lite.connect('site_parser.db')
    cur = connect.cursor()
    cur.execute("CREATE TABLE car_parsing_1(id INT, car_sql_column TEXT, year_sql_column INT)")
    cur.execute("CREATE TABLE car_parsing_1_price(id INT, car_price INT)")

    site_parsing_2()




except lite.Error as e:
    print(f'Error {e.args[0]}:')
    sys.exit(1)



with connect:
    cur = connect.cursor()

    rows_join = f'SELECT * FROM car_parsing_1 JOIN car_parsing_1_price ON car_parsing_1.id = car_parsing_1_price.id'

    cur.execute(rows_join)
    rows = cur.fetchall()
    for row in rows:
        print(row)