from flask import Flask, render_template, request, session, redirect
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt
from datetime import datetime
app = Flask(__name__)

DB_NAME = "C:\\Users\\16099\\PycharmProjects\\web-app-GeorgePaice\\clicks.db"


def create_connection(db_file):
    """create a connection to the sqlite db"""
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return None


@app.route('/')
def render_homepage():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/fans')
def fans():
    # connect to the database
    con = create_connection(DB_NAME)

    # SELECT the things you want from your table(s)
    query = "SELECT id, name, description, quantity, image, price, link FROM fans"

    cur = con.cursor()  # You need this line next
    cur.execute(query)  # this line actually executes the query
    switches_list = cur.fetchall()  # puts the results into a list usable in python
    con.close()
    return render_template('fans.html', products=switches_list)


@app.route('/lights')
def lights():

    return render_template('lights.html')


@app.route('/switches')
def switches():
    # connect to the database
    con = create_connection(DB_NAME)

    # SELECT the things you want from your table(s)
    query = "SELECT id, name, description, quantity, image, price FROM switches"

    cur = con.cursor()  # You need this line next
    cur.execute(query)  # this line actually executes the query
    switches_list = cur.fetchall()  # puts the results into a list usable in python
    con.close()
    return render_template('switches.html', products=switches_list)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


app.run(host='0.0.0.0', debug=True)


