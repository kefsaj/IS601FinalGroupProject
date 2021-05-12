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
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)
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


@app.route('/login', methods=['GET', 'POST'])
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
            message = 'Your username/password is incorrect!'
    return render_template('login.html', msg=message)

@app.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM userTable WHERE id = %s', (user_id))
    # Fetch one record and return result
    account = cursor.fetchone()
    return render_template('profile.html', firstname=account['firstname'], lastname=account['lastname'],
                           isemailed=isemailed['isemailed'], id=account['id'])
"""
id
username
password
email
isemailed
"""


@app.route('/register', methods=['GET'])
def register_get():
    message = ''
    return render_template('register.html', msg=message)

@app.route('/register', methods=['POST'])
def register_post():
    message = ''
    cursor = mysql.get_db().cursor()
    username = request.form['username']
    cursor.execute('SELECT * FROM userTable WHERE username = %s', (username))
    account = cursor.fetchone()
    if account:
        message = 'username already exist'
        return render_template('register.html', msg=message)
    if request.form['password'] != request.form['confirm_password']:
        message = 'password is not match'
        return render_template('register.html', msg=message)
    inputData = (request.form.get('username'),
                 hashlib.md5(request.form['password'].encode(encoding='UTF-8', errors='strict')).hexdigest(),
                 request.form.get('firstname'),
                 request.form.get('lastname'), request.form.get('school'),
                 request.form.get('department'), request.form.get('year'), False)
    sql_insert_query = """INSERT INTO userTable (username,password,firstname,lastname,isemailed) VALUES (%s, %s,%s, %s,%s, %s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)

    mysql.get_db().commit()
    username = request.form['username']
    password = hashlib.md5(request.form['password'].encode(encoding='UTF-8', errors='strict')).hexdigest()
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM userTable WHERE username = %s AND password = %s', (username, password,))
    account = cursor.fetchall()
    user = account[0]
    user_id = int(user['id'])

    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "is601final@gmail.com"
    receiver_email = request.form.get('username')
    mail_password = 'KefinSajan' # mail_password = 'xudryc-waNfy9-zopfyv'
    main_url = 'https://is601.herokuapp.com/activate/{}'.format(user_id)

    message = MIMEMultipart("alternative")
    message["Subject"] = "Activating Your Account regarding IS601 Final Project"
    message["From"] = sender_email
    message["To"] = receiver_email
    content = """\
    Subject: Activating Your Account regarding IS601 Final Project

    Please click this link to activate: """ + main_url
    part1 = MIMEText(content, "plain")
    message.attach(part1)
    context = ssl.create_default_context()
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, mail_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        message = 'The Verification by email has been sent!'

    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()
    return redirect('/profile/{}'.format(user_id), msg=message)

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