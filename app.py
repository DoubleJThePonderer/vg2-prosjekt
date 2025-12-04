from flask import Flask,request, redirect, render_template, session, url_for
import mysql.connector
import re

app = Flask(__name__)
app.secret_key = '28ku3fl8Gq17'

def get_dbconection():
    return mysql.connector.connect(
    host="10.200.14.23",
    user="remoteuser",
    password="IMIKUB",
    database="Users"
    )

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    mydb = get_dbconection()
    msg =''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password =%s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            return render_template('index.html',
msg='Logged in successfully!')
        else:
            msg='Incorrect username/password'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    mydb = get_dbconection()
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'account already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'invalid email address'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only letters and numbers'
        elif not username or not password or not email:
            msg = 'Please fill out the form'
        else:
            cursor.execute('INSERT INTO accounts VALUES(NULL, %s, %s, %s)', (username, password, email))
            mydb.commit()
            msg = 'you have successfully registerd'
    return render_template('register.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)