"""
id
username
password
email
isemailed
"""

from typing import List, Dict
import simplejson as json
from flask import Flask, render_template, request, redirect, url_for, session
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'userData'
mysql.init_app(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('homepage.html')

@app.route('/login', methods=[ 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode(encoding='UTF-8', errors='strict')).hexdigest()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM userTable WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchall()
        if account:
            message = 'Logged in successfully!'
            user = account[0]
            user_id = int(user['id'])
            return redirect('/profile/{}'.format(user_id))
        else:
            # Account doesnt exist or username/password incorrect
            message = 'Incorrect username/password!'
    return render_template('login.html', msg=message)

@app.route('/logout', methods=['GET'])
def logout():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():

    return render_template('success.html', msg=message)

@app.route('/<int:user_id>', methods=['POST'])
def activate(user_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM userTable WHERE id = %s', (user_id))
    result = cursor.fetchall()
    user = result[0]
    inputData = (user['username'], user['password'], user['email'],
                 user['isemailed'], True, user_id)
    sql_update_query = """UPDATE userTable t SET t.username = %s, t.password = %s, t.email = %s, t.isemailed = %s,  WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return render_template('success.html')
"""
id
username
password
email
isemailed
"""

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0')