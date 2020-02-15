from flask import Flask, render_template
from parser import site_parsing
from parser_2 import site_parsing_2
from parser_3 import site_parsing_3

app = Flask(__name__)

@app.route('/')
@app.route('/main')
def main_page():
    return render_template('main.html')

@app.route('/parser')
def show_parsing_html():
    return render_template('parser.html')

@app.route('/parsing_result')
def parser():
    #car_name_site, site_name, average_price, max_price, min_price, offers_all = site_parsing()
    #return render_template('parsing_result.html', car_name_site = car_name_site, site_name = site_name, average_price = average_price, max_price = max_price, min_price = min_price, offers_all = offers_all)
    data = site_parsing()
    return render_template('parsing_result.html', data = data)

@app.route('/parsing_result_2')
def parser_2():
    data = site_parsing_2()
    return render_template('parsing_result_2.html', data = data)

@app.route('/parsing_result_3')
def parser_3():
    data = site_parsing_3()
    return render_template('parsing_result_3.html', data = data)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')





if __name__ == '__main__':
    app.run(debug = True)