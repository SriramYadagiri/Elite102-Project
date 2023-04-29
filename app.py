#TODO:
# - Recover your account number - NR
# - Admin priveleges - NR
# - Wire Transfer - NR
# - Input Validation For:
#    - login
#    - Create Account
#    - Transactions

from flask import Flask, flash, redirect, url_for, request, render_template
from login import create_account, user_login
from decimal import Decimal
import banking
import mysql.connector

connection = mysql.connector.connect(user = "root", database = "bank", password = "Leg8iesh")

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

user = None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    global user
    user = None
    return redirect(url_for('home'))

@app.route('/account')
def account():
    global user
    if user == None:
        return "Invalid Address"
    else:
        return render_template('account.html', balance=banking.get_balance(user), history=banking.get_history(connection, user), name=user["username"].upper())

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        acc_numb = request.form['an']
        pin = request.form['pw']

        global user
        user = user_login(connection, acc_numb, pin)
        return redirect(url_for('account'))
    else:
        return render_template('login.html')
    
@app.route('/create-account', methods=['POST', 'GET'])
def new_account():
    if request.method == 'POST':
        fname = request.form['fnm']
        lname = request.form['lnm']
        username = request.form['unm']
        pin = request.form['pw']
        
        global user
        user = create_account(connection, fname, lname, username, pin)
        flash(f'Your account number is: {user["accountNumber"]}')
        return redirect(url_for('login'))
    else:
        return render_template('create-account.html')

@app.route('/edit-account')
def edit_account():
    global user
    if user == None:
        return "Invalid Address"
    return render_template('edit-account.html', user=user)

@app.route('/withdrawal', methods=['POST'])
def withdrawal():
    amount = Decimal(request.form["amount"])
    banking.withdraw(connection, user, amount)
    return redirect(url_for('account'))

@app.route('/deposit', methods=['POST'])
def deposit():
    amount = Decimal(request.form["amount"])
    banking.deposit(connection, user, amount)
    return redirect(url_for('account'))

@app.route('/update-username', methods=['POST'])
def update_username():
    new_name = request.form["unm"]
    banking.change_name(connection, user, new_name)
    return redirect(url_for('edit_account'))

@app.route('/update-pin', methods=['POST'])
def update_pin():
    new_pin = request.form["pin"]
    banking.change_pin(connection, user, new_pin)
    return redirect(url_for('edit_account'))

@app.route('/close-account', methods=['POST'])
def close_account():
    global user
    banking.close_account(connection, user)
    user = None
    return redirect(url_for('home'))

app.run(debug=True)