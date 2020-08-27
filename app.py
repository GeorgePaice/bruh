from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def render_homepage():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/fans')
def fans():
    return render_template('fans.html')


@app.route('/lights')
def lights():
    return render_template('lights.html')


@app.route('/switches')
def switches():
    return render_template('switches.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


app.run(host='0.0.0.0', debug=True)


