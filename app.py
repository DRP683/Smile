from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

DB_NAME = "smile.db"

app = Flask(__name__)

def create_connection(db_file):
    """"Create a connection to the sqlite db"""
    try:
        connection = sqlite3.connect(db_file)
        #initialize_tables(connection)
        return connection
    except Error as e:
        print(e)


@app.route('/')
def render_homepage():
    return render_template( 'home.html')

@app.route('/menu')
def render_menu_page():
    #connect to database
    con = create_connection(DB_NAME)

    query = "SELECT name, description, volume, price, image, FROM product"
    products = [["Flat white", "Definietly created in New Zealand (not in the West Island) - a classic", "180mL", "flatwhite", "4.00"],
                ["Latte",	"The New Zealand latte is larger than a flat white and has more foamy milk.", "240mL",	"latte",	"4.00",],
                ["Espresso", "Straight from the machine, 60mL including crema.", "60mL", "espresso", "3.00"],
                ["Long black",	"Hot water + espresso 120mL.",	"90mL",	"longblack", "3.00"]]

    #save query
    # run query on db
    #catchall the results abd save as product_list
    # pass to menu.html render('menut.html, products=product_list
    return render_template('menu.html', products=products)

@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')

app.run(host='0.0.0.0')
