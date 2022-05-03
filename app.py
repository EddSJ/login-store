from flask import Flask, jsonify, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_cors import CORS, cross_origin
  
  
app = Flask(__name__)

CORS(app)
  
  
app.secret_key = 'nopales'
  
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'FVJpgw76FR'
app.config['MYSQL_PASSWORD'] = '0uDPWv3khs'
app.config['MYSQL_DB'] = 'FVJpgw76FR'
  
mysql = MySQL(app)
  
@app.route('/')
def index():
    return (
    '<h1>Bienvenido a la API de Loggin</h1>'
    )

@cross_origin
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.json and 'password' in request.json:
        username = request.json['username']
        password = request.json['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
        else:
            msg = 'Incorrect username / password !'
            
    return jsonify({
        'message': msg,
        'loggedin': session.get('loggedin'),
        'id': account['id'],
    })

@cross_origin
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    #response in json
    return jsonify({'message': 'Logged out successfully !'})
  
@cross_origin
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.json and 'password' in request.json and 'email' in request.json :
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return jsonify({'message': msg})

if __name__ == '__main__':
    app.run(debug=True,)