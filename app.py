#Video 8a time 2:55

from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt

DB_NAME = "smile.db"

app = Flask(__name__)
app.secret_key = "banana"
def create_connection(db_file):
    """"Create a connection to the sqlite db"""
    try:
        connection = sqlite3.connect(db_file)
        #initialize_tables(connection)
        return connection
    except Error as e:
        print(e)

    return None


@app.route('/')
def render_homepage():
    return render_template( 'home.html', logged_in=is_logged_in())

@app.route('/menu')
def render_menu_page():

    # connect to database
    con = create_connection(DB_NAME)

    # SELECT the things you want from your table(s)
    query = "SELECT name, description, volume, price, image FROM product"


    cur = con.cursor()  # Make a cursor
    cur.execute(query)  # Execute query
    product_list = cur.fetchall()  # put the result into the
    con.close()  # Close connections

    return render_template('menu.html', products=product_list, logged_in=is_logged_in())

@app.route('/contact')
def render_contact_page():
    return render_template('contact.html', logged_in=is_logged_in())

@app.route('/login')
def render_login_page():
    if request.method == "POST":
        email = request.form['email'].strip.lower
        password = request.form['password'].strip


        query = """SELECT id, fname, password FROM customer WHERE email = ?"""
        con = create_connection(DB_NAME)
        cur = con.cursor()
        cur.execute(query, (email,))
        user_data = cur.fetchall()
        con.close()

        try:
            userid = user_data[0][0]
            firstname = user_data[0][1]
            db_password = user_data[0][2]
        except IndexError:
            return redirect("/login?error=Email+invalid+or+password+incorrect")

        session['email'] = email
        session['userid'] = userid
        session['firstname'] = firstname
        print(session)

        if not Bcrypt.check_password_hash(db_password, password):
            return redirect(request.referrer + "/login?error=Email+invalid+or+password+incorrect")

    return render_template("login.html", logged_in=is_logged_in())

@app.route('/signup', methods=["GET", "POST"])
def render_signup_page():
    if request.method == 'POST':
        print(request.form)
        fname = request.form.get('fname').strip().title()
        lname = request.form.get('lname').strip().title()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            return redirect('/signup?error=Passwords+dont+match')

        if len(password) < 8:
            return redirect('/signup?error=Password+must+have+at+least+8+characters')

        # connect to database
        con = create_connection(DB_NAME)

        # SELECT the things you want from your table(s)
        query = "INSERT into customer(id, fname, lname, email, password) VALUES(NULL,?, ?, ?, ?)"

        cur = con.cursor()  # Make a cursor
        try:
            cur.execute(query, (fname, lname, email, password))  # Execute query
        except sqlite3.IntegrityError:
            return redirect('/signup?error=Email+already+used')

        con.commit()  # put the result into the
        con.close()  # Close connections
    return render_template("signup.html", logged_in=is_logged_in())

def is_logged_in():
    if session.get('email') is None:
        print('not logged in')
        return False
    else:
        print('Logged in')
        return True

app.run(host='0.0.0.0')