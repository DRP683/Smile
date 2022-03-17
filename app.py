from flask import Flask
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello, world</h1>'
def render_homepage():
    return render_template('home.html')

@app.route('/menu')
def render_menu_page():
    return render_template('menu.html')

@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')

app.run(host='0.0.0.0')
