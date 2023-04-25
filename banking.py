#Returns the user's balance
def get_balance(user):
    return user['money']

#Changes the user's password to a new given one
def change_password(user, connection, new_password):
    cursor = connection.cursor()

    changeUserPassword = (f'UPDATE users SET pin = \"{new_password}\" WHERE id = {user["id"]}')

    cursor.execute(changeUserPassword)

    connection.commit()
    cursor.close()

    user["pin"] = new_password

#Changes the user's name to a new given one
def change_name(user, connection, new_name):
    cursor = connection.cursor()

    changeUserName = (f'UPDATE users SET name = \"{new_name}\" WHERE id = {user["id"]}')

    cursor.execute(changeUserName)

    connection.commit()
    cursor.close()

    user["name"] = new_name

#Deletes the user's account from the users table
def close_account(user, connection):
    cursor = connection.cursor()

    delete_account = f'DELETE FROM users WHERE id={user["id"]}'

    cursor.execute(delete_account)
    connection.commit()
    cursor.close()

#Given an amount the method adds that amount to the user's balance 
#The method then adds the transaction into the user's account history
def deposit(connection, user, amount):
    print(user)
    user["money"] += amount

    cursor = connection.cursor()
    
    #Deposit the money
    deposit_user_money = (f'UPDATE users SET money = money+{float(amount)} WHERE id={user["id"]}')

    cursor.execute(deposit_user_money)

    #Update the user's account history
    update_history = (f'INSERT INTO bank_history (id, type, amount, balance) VALUES ({user["id"]}, \"{"deposit"}\", {amount}, {user["money"]})')
    cursor.execute(update_history)

    connection.commit()
    cursor.close()
    
#Given an amount the method subtracts that amount from the user's balance 
#The method then adds the transaction into the user's account history
def withdraw(connection, user, amount):
    print(amount)
    user["money"] -= amount

    cursor = connection.cursor()
    
    #Withdraws the money
    withdraw_user_money = (f'UPDATE users SET money = money-{float(amount)} WHERE id={user["id"]}')

    cursor.execute(withdraw_user_money)

    #Updates the user's account history
    update_history = (f'INSERT INTO bank_history (id, type, amount, balance) VALUES ({user["id"]}, \"{"withdrawal"}\", {amount}, {user["money"]})')
    cursor.execute(update_history)

    connection.commit()
    cursor.close()

#Returns an array of all the transactions the given user has had.
#The array includes:
#  - the type of transaction: withdrawal, deposit, transfer
#  - the amount of money involved in the transaction
#  - the date and time of the transaction
#  - the user's balance after the transaction
def get_history(connection, user):
    cursor = connection.cursor()

    #Get all rows that refer to the given user's history
    get_history = (f'SELECT * FROM bank_history WHERE id={user["id"]}')

    cursor.execute(get_history)

    history = []

    #For each row add each piece of data
    for row in cursor:
        history.append([row[1].title(), row[2], row[3], row[4]])
    
    return history