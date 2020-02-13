from flask import Flask, render_template
from parser import site_parsing

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
    #a = site_parsing()
    return site_parsing()
    #return render_template('/parser.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')





if __name__ == '__main__':
    app.run(debug = True)