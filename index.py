from flask import Flask, render_template, request, redirect, url_for
import requests as req

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/portafolio')
def portafolio():
    
    response = req.get('http://localhost:3001/properties')
    result = response.json()
    print(result['data'])
    return render_template('portfolio.html', properties =  result['data'])


@app.route('/registro')
def registro():
    return render_template('reguistro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logeo')
def logeo():
    correo = request.form['email']    
    # password = request.form['password']
    print(correo, 'ga')
    # addLogged = {"email": email, "password": password}
    # response = req.post('http://localhost:3001/login', json= addLogged)
    # result = response.json()
    # print(result)
    return redirect(url_for('portafolio'))

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')


@app.route('/admin')
def read():
    return render_template('añadir.html')


if __name__ == "__main__":
    app.run(debug=True)