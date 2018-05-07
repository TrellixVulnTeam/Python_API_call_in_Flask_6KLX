import collections
import random

import cursor as cursor
from flask import Flask, render_template, request, Response, session, url_for
from flaskext.mysql import MySQL
import json

from werkzeug.utils import redirect

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'contact_list'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s.html' % page_name)


@app.route('/add_data', methods=['POST'])
def add_data():
    conn = mysql.connect()
    cursor = conn.cursor()
    name = request.form['name']
    phone_number = request.form['phone_number']
    codes = random.randint(100000, 999999)
    users = json.dumps(codes)
    c = cursor.execute("INSERT INTO user (name, phone_number, code) VALUES (%s,%s,%s)",
                       (name, phone_number, int(codes)))
    conn.commit()
    if (c == True):
        print("Your Verificatiopn code is----/n")
        return Response(users, status=2000)
    else:
        return 'Not Registered'



@app.route("/show")
def hello():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("Select * from user")
    a = cursor.fetchall()
    users = json.dumps(a)
    return Response(users, status=200)


@app.route('/login', methods=['POST'])
def login():
    conn = mysql.connect()
    cursor = conn.cursor()
    code = request.form['code']
    phone_number = request.form['phone_number']
    cursor.execute("select * from user where code = %s and phone_number = %s", (code, phone_number))
    check = cursor.fetchone()
    users = json.dumps(check)
    if check is None:
        return 'You are not verified'
    else:
        print('You are verified and your credentials are /n ')
        return Response(users, status=2000)


@app.route('/fnf', methods=['POST'])
def fnf():
    conn = mysql.connect()
    cursor = conn.cursor()
    fnf = request.form['phone_number']
    data = fnf.split(',')
    alldata = []
    fl = []
    fr = []
    for i in data:
        alldata.append(i)
    for j in alldata:
        cursor.execute("select name, phone_number from user where phone_number = %s", j)
        data = cursor.fetchone()
        if data is not None:
            fr = {'name': data[0],
                  'phone_number': data[1]}
            fl.append(fr)
    list = {'list': fl}
    users = json.dumps(list)
    return Response(users, status=2000)

    #  comma = input().split(",")
    # cursor.execute("select name, phone_number from user where phone_number = %s", phone_number)
    # check = cursor.fetchone()
    # objects_list = []
    # for row in check:
    #     d = collections.OrderedDict()
    #     d['id'] = row.id
    #     d['name'] = row.name
    #     d['phone_number'] = row.phone_number
    #     objects_list.append(d)
    #
    # users = json.dumps(objects_list)
    # if users is None:
    #     return 'You are not verified'
    # else:
    #     return Response(users, status=2000)


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    return render_template('hello.html')


if __name__ == '__main__':
    app.run()
