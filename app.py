from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def render_homepage():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


app.run(host='0.0.0.0', debug=True)


