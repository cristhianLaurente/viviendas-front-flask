from flask import Flask, render_template, request, redirect, url_for, session 
import requests as req

app = Flask(__name__)

app.secret_key = 'key-secret'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/portafolio')
def portafolio():
    
    response = req.get('http://localhost:3001/properties')
    result = response.json()    
    if 'token' in session:
        key = session['token']
    else:
        key = false
    return render_template('portfolio.html', properties =  result['data'], token = key )

@app.route('/property-detail')
def propertyDetail():
    return render_template('propertydetails.html')

@app.route('/registro')
def registro():
    return render_template('reguistro.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    addRegister = {"name": name, "lastname": lastname, "email": email, "password":password}
    response = req.post('http://localhost:3001/user', json= addRegister )
    result = response.json()
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logeo', methods=['POST'])
def logeo():
    email = request.form['email']    
    password = request.form['password']
    addLogged = {"email": email, "password": password}
    response = req.post('http://localhost:3001/login', json= addLogged)
    result = response.json()
    session['token'] = result['token']
    return redirect(url_for('portafolio'))

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')


@app.route('/admin')
def read():
    response = req.get('http://localhost:3001/properties')
    result = response.json()
    return render_template('properties.html', properties =  result['data'])


if __name__ == "__main__":
    app.run(debug=True)