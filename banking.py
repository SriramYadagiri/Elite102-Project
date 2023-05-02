def get_balance(user):
    return user['money']

def wire(connection, user, receiver, amount):
    user["money"] -= amount

    cursor = connection.cursor()
    
    get_receiver_money_id = (f'SELECT money, id FROM users WHERE accountNumber={receiver}')

    cursor.execute(get_receiver_money_id)
    rows = cursor.fetchall()
    print(rows)
    receiver_money = float(rows[0][0])
    receiver_id = rows[0][1]

    update_user_money = (f'UPDATE users SET money = money-{float(amount)} WHERE id={user["id"]}')
    update_reciever_money = (f'UPDATE users SET money = money+{float(amount)} WHERE id={receiver_id}')

    cursor.execute(update_user_money)
    cursor.execute(update_reciever_money)

    update_user_history = (f'INSERT INTO bank_history (id, type, amount, balance) VALUES ({user["id"]}, "Wire Transfer", \"{float(amount)}\", \"{user["money"]}\")')
    update_receiver_history = (f'INSERT INTO bank_history (id, type, amount, balance) VALUES ({receiver_id}, "Wire Transfer", \"{float(amount)}\", \"{receiver_money+float(amount)}\")')
    cursor.execute(update_user_history)
    cursor.execute(update_receiver_history)

    connection.commit()
    cursor.close()


def change_password(connection, user, new_password):
    cursor = connection.cursor()

    changeUserPassword = (f'UPDATE users SET pin = \"{new_password}\" WHERE id = {user["id"]}')

    cursor.execute(changeUserPassword)

    connection.commit()
    cursor.close()

    user["pin"] = new_password

def change_name(connection, user, new_name):
    cursor = connection.cursor()

    changeUserName = (f'UPDATE users SET username = \"{new_name}\" WHERE id = {user["id"]}')

    cursor.execute(changeUserName)

    connection.commit()
    cursor.close()

    user["username"] = new_name

def close_account(connection, user):
    cursor = connection.cursor()

    delete_account = f'DELETE FROM users WHERE id={user["id"]}'

    cursor.execute(delete_account)
    connection.commit()
    cursor.close()

def deposit(connection, user, amount):
    user["money"] += amount

    cursor = connection.cursor()
    
    deposit_user_money = (f'UPDATE users SET money = money+{float(amount)} WHERE id={user["id"]}')

    cursor.execute(deposit_user_money)

    update_history = (f'INSERT INTO bank_history (id, type, amount, balance) VALUES ({user["id"]}, \"{"deposit"}\", {amount}, {user["money"]})')
    cursor.execute(update_history)

    connection.commit()
    cursor.close()

    

def withdraw(connection, user, amount):
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