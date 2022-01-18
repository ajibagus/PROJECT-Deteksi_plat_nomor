from application import detection_camera
from application import app
from flask import Flask, render_template, request, redirect, url_for, session,Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

#
app.secret_key = 'your secret key'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'big_project'
  
mysql = MySQL(app)

@app.route('/')
  
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id_admin'] = account['id_admin']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('Home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id_admin', None)
    session.pop('username', None)
    return redirect(url_for('login.'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match('[^@]+@[^@]+\.[^@]*$', email):
            msg = 'Invalid email address !'
        elif not re.match('^[a-zA-Z0-9]*$', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO admin VALUES (NULL, % s, % s, % s)', (email, username, password,  ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


@app.route('/registrasiplatnomor', methods=['POST'])
def regisplat():
    msg = ''
    if request.method == 'POST'  and 'nipy' in request.form and 'nama' in request.form and 'plat_nomor' in request.form and 'plat_nomor' in request.form and 'status' in request.form :
        nipy = request.form['nipy']
        nama = request.form['nama']
        plat_nomor = request.form['plat_nomor']
        password = request.form['plat_nomor']
        status = request.form['status']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM karyawan WHERE nipy = % s', (nipy, ))
        account = cursor.fetchone()
        if account:
            msg = 'Data Already Exists !'
        elif not re.match('^[0-9]+[0-9]+[.]+[0-9]+[0-9]+[0-9]+[.]+[0-9]+[0-9]+[0-9]+[.]*$', nipy):
            msg = 'Incorrect NIPY !'
        elif not re.match('^[a-zA-Z ]*$', nama):
            msg = 'Name must contain only characters !'
        elif not re.match('^[a-zA-Z0-9]*$', plat_nomor):
            msg = 'Plate Number must contain only characters and numbers !'
        elif len(plat_nomor) not in range(2,8):
            msg = 'Plate Number must only in range 2-8 character !'
        elif not re.match('^[a-zA-Z]*$', status):
            msg = 'Status must contain only characters !'
        elif not nipy or not nama or not plat_nomor:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO karyawan VALUES (NULL, % s, % s, % s, % s, %s)', (nipy, nama, plat_nomor, password, status  ))
            mysql.connection.commit()
            msg = 'Data saved successfully !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('registrasiplatnomor.html', msg = msg)


@app.route('/data')
def tampildata():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT nipy, nama, plat_nomor,  status FROM karyawan''')
    rv = cur.fetchall()
    return render_template("data.html",value=rv)

@app.route('/masuk')
def tampillaporanmasuk ():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT nama, plat_nomor, waktu, status status FROM masuk''')
    rv = cur.fetchall()
    return render_template("masuk.html",value=rv)

@app.route('/keluar')
def tampillaporankeluar ():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT nama, plat_nomor, waktu, status status FROM keluar''')
    rv = cur.fetchall()
    return render_template("keluar.html",value=rv)


@app.route('/Home')
def Home():
    return render_template('Home.html')


@app.route('/data')
def data():
    return render_template('data.html')


@app.route('/registrasiplatnomor')
def registrasiplatnomor():
    return render_template('registrasiplatnomor.html')


@app.route('/masuk')
def masuk():
    return render_template('masuk.html')


@app.route('/keluar')
def keluar():
    return render_template('keluar.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/laporan')
def laporan():
    return render_template('laporan.html')

@app.route('/video_feed')
def video_feed():
    return Response(detection_camera.get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')






if __name__ == '__main__':
    app.run(debug=True)