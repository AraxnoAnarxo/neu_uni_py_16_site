from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

def site_parsing():

    max_page = 15
    pages = []

    car_name_list = []
    car_year_list = []
    price_list = []
    price_list_len = []
    car_list_len = []
    params_list = []
    params_list_test = []
    engine_power_list = []
    dict_car = dict.fromkeys(['Марка', 'Год', 'Цена'])

    for x in range(1, max_page + 1):
        pages.append(requests.get('https://auto.drom.ru/chevrolet/tahoe/page' + str(x)))

    for n in pages:
        soup = BeautifulSoup(n.text, 'html.parser')

        car_name = soup.find_all('div', class_="b-advItem__title")

        for rev in car_name:
            #print(rev.text)
            a = str(rev.text)
            car_list_len.append(a)
            car = re.split(r',', a)
            car_name_list.append(car[0])
            car_year = re.sub(r'[ ]', '', car[1])
            car_year_list.append(car_year)


        # param_other = soup.find_all('div', class_ = 'b-advItem__param')
        #
        # for rev in param_other:
        #     #params_list.append(rev.text)
        #     params_str_tmp = str(rev.text)
        #
        #     #params_str_tmp.splitlines()
        #     #print(type(params_str_tmp))
        #     # params_str = re.split(r'\n', params_str_tmp)
        #     params_list.append(params_str_tmp)
        #     # #print(type(params_str))
        #     # print(params_list)
        #     # #engine_power_list.append(a)



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
        #print(el)
        price_int = int(el)
        price_list_int.append(price_int)

    i = 0
    for x in range(len(price_list_int)):
        i += price_list_int[x]

    site_name = 'auto.drom.ru'
    print_p1 = f'Данные по запросу автомобиля {car_name_list[0]} с сайта {site_name}. '
    average_price = i / len(price_list_int)
    print_p2 = f'Средняя цена автомобиля: {average_price} рублей. '
    min_price = min(price_list_int)
    max_price = max(price_list_int)
    print_p3 = f'Максимальная цена: {max_price} рублей. \nМинимальная цена: {min_price} рублей. '
    offers_all = len(car_name_list[::2])
    print_p4 = f'Всего предложений: {offers_all}.'
    print_str = f'{print_p1}\n{print_p2}{print_p3}{print_p4}'

    return print_str






    # dict_car['Марка'] = car_name_list[::2]
    # dict_car['Год'] = car_year_list[::2]
    # dict_car['Цена'] = price_list
    #
    # return dict_car

    # df = pd.DataFrame(dict_car)
    #
    # return df

    # df.to_csv('df.csv')
    # # df.to_csv('df_02.csv')
    #
    # # читаем csv
    # DataFrame_from_csv = pd.read_csv('df.csv')
    # print(DataFrame_from_csv)




