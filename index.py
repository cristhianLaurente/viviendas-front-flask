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
    print(result)   
    if 'token' in session:
        key = session['token']
    else:
        key = ''
    return render_template('portfolio.html', properties =  result['data'], token = key )

@app.route('/property-detail')
def propertyDetail():
    id = request.args.get('id')
    if 'token' in session:
        response = req.get(f'http://localhost:3001/property/{id}')
        print(response)
        if response.status_code == 200:
            result = response.json()
            return render_template('propertydetails.html', property=result['data'])
        else:
            print('mall')
    else:
        return redirect(url_for('portafolio'))

@app.route('/registro')
def registro():
    if 'token' in session:        
        return redirect(url_for('portafolio'))
    else:
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
    if 'token' in session:
        return redirect(url_for('portafolio'))
    else:
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


@app.route('/admin')
def admin():
    if 'superuser' in session :
        response = req.get('http://localhost:3001/properties')
        result = response.json()
        return render_template('properties.html', properties =  result['data'])
    else :
        return redirect(url_for('loginadmin'))

@app.route('/loginadmin')
def loginadmin():
    if 'superuser' in session:
        return redirect(url_for('admin'))
    else:
        return render_template('loginadmin.html')

@app.route('/loginadminuser', methods=['POST'])
def loginadminuser():
    email = request.form['email']    
    password = request.form['password']
    addLogged = {"email": email, "password": password}
    response = req.post('http://localhost:3001/login', json= addLogged)
    result = response.json()
    session['superuser'] = result['token']
    return redirect(url_for('admin'))
   

@app.route('/edit')
def edit():
    id = request.args.get('id')
    if 'superuser' in session:
        token = session['superuser']
        headers = {"token": token}
        response = req.get(f'http://localhost:3001/property/{id}', headers = headers)
        if response.status_code == 200 :
            result = response.json()
            return render_template('editproperty.html', property = result['data'])
        else:
            print('mallll') 
    else:
        return render_template('loginadmin')


@app.route('/add')
def add():
    if 'superuser' in session:
        return render_template('addproperty.html')
    else:
        return redirect(url_for('loginadmin'))

@app.route('/addproperty', methods=['POST'] )
def addproperty():
    if 'superuser' in session:
        token = session['superuser']
        headers = {"token": token}
        title = request.form['title']    
        tipo = request.form['type']
        address = request.form['address']
        rooms = request.form['rooms']
        price = request.form['price']
        area = request.form['area']
        addProperty = {"title": title, "type": tipo, "address": address, "rooms":rooms, "price": price, "area":area}
        response = req.post('http://localhost:3001/property/', headers= headers, json=addProperty)
        if response.status_code == 201:
            return redirect(url_for('admin'))
        else:
            print('mall')
    else:
        return redirect(url_for('loginadmin'))


@app.route('/editproperty', methods=['POST'])
def editproperty():
    id = request.args.get('id')
    if 'superuser' in session:
        token = session['superuser']
        headers = {"token": token}
        title = request.form['title']    
        tipo = request.form['type']
        address = request.form['address']
        rooms = request.form['rooms']
        price = request.form['price']
        area = request.form['area']
        updateProperty = {"title": title, "type": tipo, "address": address, "rooms":rooms, "price": price, "area":area}
        response = req.put(f'http://localhost:3001/property/{id}', headers= headers, json=updateProperty)
        if response.status_code == 200 :
            return redirect(url_for('admin'))
        else:
            print('mallll')            
    else :
        return redirect(url_for('loginadmin'))
    
@app.route('/delete')
def delete():
    id = request.args.get('id')
    if 'superuser' in session:
        token = session['superuser']
        headers = {"token": token}
        response = req.delete(f'http://localhost:3001/property/{id}', headers=headers)
        if response.status_code == 200:
            return redirect(url_for('admin'))
        else :
            print('malll')
    else:
        return redirect(url_for('loginadmin'))
if __name__ == "__main__":
    app.run(debug=True)