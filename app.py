from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase 
from SignUp import SignUp

db = dbase.dbConnection()

app = Flask(__name__)
#Rutas de la aplicacion

@app.route('/')
def home():
    users = db['EmployeesDetails']
    usersReceived = users.find()
    
    return render_template('index.html', users = usersReceived)

#Method post
@app.route('/SignUp',methods=['POST'])
def addEmployeer():
    users = db['EmployeesDetails']
    name = request.form['name']
    lastName = request.form['lastName']
    password = request.form['password']
    email = request.form['email']
    phone = request.form['phone']
    adress = request.form['adress']
    position = request.form['position']
    
        # Verificar el formato del email utilizando una expresión regular
    import re
    if not re.match(r'[\w.-]+@ejad\.com\.mx', email):
        return jsonify({'message': 'El formato del email no es válido. Debe ser de la forma example@ejad.com.mx'}), 400

    # Verificar si el email ya existe en la base de datos
    existing_user = users.find_one({'Email': email})
    if existing_user:
        return jsonify({'message': 'El email ya está registrado. Por favor, utiliza otro email.'}), 400
    
    
    if name and lastName and password and email and phone and adress and adress and position:
        user = SignUp(name,lastName,password,email,phone,adress,position)
        users.insert_one(user.toDBCollection())
        response = jsonify({
            'name': name,
            'lastName': lastName,
            'password':  password,
            'email' : email,
            'phone' : phone,
            'adress' : adress,
            'position' : position
        })
        return redirect(url_for('home'))
    else:
        return notFound()
    
#method delete
@app.route('/delete/<string:user_name>')
def delete(user_name):
    users = db['EmployeesDetails']
    users.delete_one({'name' : user_name}) 
    return redirect(url_for('home'))
   
#method put
@app.route('/edit/<string:user_name>', methods=['POST'])
def edit(user_name):
    users = db['EmployeesDetails']
    name = request.form['name']
    lastName = request.form['lastName']
    password = request.form['password']
    email = request.form['email']
    phone = request.form['phone']
    adress = request.form['adress']
    position = request.form['position']
    
    if name and lastName and password and email and phone and adress and adress and position:
        users.update_one({'name' : user_name}, {'$set' : {'name' : name,'lastName' : lastName,'password' : password,'email' : email,'phone' : phone,'adress' : adress,'position' : position}})
        response = jsonify({'message': 'El empleado ' + user_name + ' ha actualizado'})
        return redirect(url_for('home'))
    else:
        return notFound()

@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' +request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response
    
if __name__ == '__main__':
    app.run(debug=True, port=4000)
    