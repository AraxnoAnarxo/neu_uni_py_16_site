from bs4 import BeautifulSoup
import requests
import re

def site_parsing_2():

    max_page = 40
    pages = []

    car_name_list = []
    car_year_list = []
    price_list = []
    price_list_len = []
    car_list_len = []


    for x in range(1, max_page + 1):
        pages.append(requests.get('https://auto.drom.ru/bmw/x1/page' + str(x)))

    for n in pages:
        soup = BeautifulSoup(n.text, 'html.parser')

        car_name = soup.find_all('div', class_="b-advItem__title")

        for rev in car_name:
            a = str(rev.text)
            car_list_len.append(a)
            car = re.split(r',', a)
            car_name_list.append(car[0])
            car_year = re.sub(r'[ ]', '', car[1])
            car_year_list.append(car_year)

        price = soup.find_all('div', class_ = 'b-advItem__price b-advItem__price_mobile')
        pattern = r'(\d{1}\s\d{3}\s\d{3})|(\d{3}\s\d{3})'
        for rev in price:
            b = rev.text
            price_list_len.append(b)
            price_str = re.findall(pattern, rev.text)
            price_str = str(price_str)
            price_str = price_str.replace('\\xa0', '') # избавляемся от знаков \xa0
            price_str = re.sub(r"[\]['(),\s]", '', price_str)
            price_list.append(price_str)

    price_list_int = []

    for el in price_list:
        price_int = int(el)
        price_list_int.append(price_int)

    i = 0
    for x in range(len(price_list_int)):
        i += price_list_int[x]

    car_name_site = car_name_list[0]
    site_name = 'auto.drom.ru'
    average_price = round(i / len(price_list_int))
    min_price = min(price_list_int)
    max_price = max(price_list_int)
    offers_all = len(car_name_list[::2])
    data = dict(car_name_site = car_name_site, site_name = site_name, average_price = average_price, max_price = max_price, min_price = min_price, offers_all = offers_all)

    return data