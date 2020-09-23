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


@app.route('/login', methods=["GET", "POST"])
def render_login_page():
    if is_logged_in():
        return redirect('/')

    if request.method == "POST":
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()

        query = """SELECT id, fname, password FROM customer WHERE email = ?"""
        con = create_connection(DB_NAME)
        cur = con.cursor()
        cur.execute(query, (email,))
        user_data = cur.fetchall()
        con.close()
        # if given the email is not in the database this will raise an error
        # would be better to find out how to see if the query return an empty resultset
        try:
            userid = user_data[0][0]
            firstname = user_data[0][1]
            db_password = user_data[0][2]
        except IndexError:
            return redirect("/login?error=Email+invalid+or+password+incorrect")

        # check if the password is incorrect for that email address

        if not bcrypt.check_password_hash(db_password, password):
            return redirect(request.referrer + "?error=Email+invalid+or+password+incorrect")

        session['email'] = email
        session['userid'] = userid
        session['firstname'] = firstname
        print(session)
        return redirect('/')

    return render_template('login.html', logged_in=is_logged_in())


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
    query = "SELECT id, name, description, quantity, image, price, link FROM switches"

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

@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():
    if is_logged_in():
        return redirect('/')

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
            return redirect('/signup?error=Password+must+be+8+characters+or+more')

        hashed_password = bcrypt.generate_password_hash(password)

        con = create_connection(DB_NAME)

        query = "INSERT INTO customer(id, fname, lname, email, password) " \
                "VALUES(NULL,?,?,?,?)"

        cur = con.cursor()  # You need this line next
        try:
            cur.execute(query, (fname, lname, email, hashed_password))  # this line actually executes the query
        except sqlite3.IntegrityError:
            return redirect('/signup?error=Email+is+already+used')

        con.commit()
        con.close()
        return redirect('/login')

    return render_template('signup.html', logged_in=is_logged_in())



app.run(host='0.0.0.0', debug=True)


