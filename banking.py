def get_balance(user):
    return user['money']

def change_password(user, connection):
    new_password = input("\nWhat do you want to change your password to: ")
    change = input(f'Are you sure you want to change your password to {new_password} (Y/N) ').lower()

    if change != "n":
        cursor = connection.cursor()

        changeUserPassword = (f'UPDATE users SET pin = \"{new_password}\" WHERE id = {user["id"]}')

        cursor.execute(changeUserPassword)

        connection.commit()
        cursor.close()

        user["pin"] = new_password

def change_name(user, connection):
    new_name = input("\nWhat do you want to change your name to: ")
    change = input(f'Are you sure you want to change your name to \"{new_name}\" (Y/N) ').lower()

    if change != "n":
        cursor = connection.cursor()

        changeUserName = (f'UPDATE users SET name = \"{new_name}\" WHERE id = {user["id"]}')

        cursor.execute(changeUserName)

        connection.commit()
        cursor.close()

        user["name"] = new_name

def close_account(user, connection):
    change = input("Are you sure you want to delete you account. This is PERMANENT! (Y/N) ")

    if (change == "n"): return

    cursor = connection.cursor()

    delete_account = f'DELETE FROM users WHERE id={user["id"]}'

    cursor.execute(delete_account)
    connection.commit()
    cursor.close()

    print("account deleted...")

def deposit(connection, user, amount):
    print(user)
    user["money"] += amount

    cursor = connection.cursor()
    
    deposit_user_money = (f'UPDATE users SET money = money+{float(amount)} WHERE id={user["id"]}')

    cursor.execute(deposit_user_money)

    update_history = (f'INSERT INTO bank_history (id, type, amount, balance) VALUES ({user["id"]}, \"{"deposit"}\", {amount}, {user["money"]})')
    cursor.execute(update_history)

    connection.commit()
    cursor.close()

    

def withdraw(connection, user, amount):
    print(amount)
    user["money"] -= amount

    cursor = connection.cursor()
    
    withdraw_user_money = (f'UPDATE users SET money = money-{float(amount)} WHERE id={user["id"]}')

    cursor.execute(withdraw_user_money)

    update_history = (f'INSERT INTO bank_history (id, type, amount, balance) VALUES ({user["id"]}, \"{"withdrawal"}\", {amount}, {user["money"]})')
    cursor.execute(update_history)

    connection.commit()
    cursor.close()

def get_history(connection, user):
    cursor = connection.cursor()

    get_history = (f'SELECT * FROM bank_history WHERE id={user["id"]}')

    cursor.execute(get_history)

    history = []

    for row in cursor:
        history.append([row[1].title(), row[2], row[3], row[4]])
    
    return history