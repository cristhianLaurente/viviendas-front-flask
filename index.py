from flask import Flask, render_template, request, redirect, url_for
import requests as req

app = Flask(__name__)

@app.route('/')
def index():
    response = req.get('https://jsonplaceholder.typicode.com/users')
    result = response.json()
    print(result)
    return render_template('index.html')

@app.route('/portafolio')
def portafolio():
    return render_template('portfolio.html')


@app.route('/registro')
def registro():
    return render_template('reguistro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')



if __name__ == "__main__":
    app.run(debug=True)