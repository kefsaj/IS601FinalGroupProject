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
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    return render_template('success.html')

@app.route('/activate/<int:user_id>', methods=['POST'])
def activate(user_id):
    return render_template('success.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0')