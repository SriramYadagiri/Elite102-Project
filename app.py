#TODO:
# - Close Accounts
# - Edit Accounts
# - Recover your account number
# - Admin privelages
# - Wire Transfer
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
        return render_template('account.html', balance=banking.get_balance(user), history=banking.get_history(connection, user), name=user["name"].upper())

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
        name = request.form['nm']
        pin = request.form['pw']
        
        global user
        user = create_account(connection, name, pin)
        flash(f'Your account number is: {user["accountNumber"]}')
        return redirect(url_for('login'))
    else:
        return render_template('create-account.html')

@app.route('/edit-account')
def edit_account():
    global user
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

app.run(debug=True)