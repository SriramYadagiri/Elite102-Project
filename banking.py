from decimal import Decimal
from os import system

def open_bank(user, connection):
    print("a. Check Balance")
    print("b. Deposit")
    print("c. Withdraw")
    print("d. Edit Your Account")
    print("e. Close Your Account")
    print("f. View Account Activity")
    print("g. Logout")

    if (user["admin"]):
        print("\nAdmin Privileges")
        print("h. Modify other accounts")
        print("i. Close accounts")

    print()
    option = input("\nChoose an option: ")

    system("cls")

    match option.lower():
        case "a":
            check_balance(user)
        case "b":
            deposit(user, connection)
        case "c":
            withdraw(user, connection)
        case "d":
            edit_account(user, connection)
        case "e":
            close_account(user, connection)
            return
        case "f":
            show_history(user, connection)
        case "g":
            user = None
            return
        case _:
            print("Invalid Option")
            print()
            open_bank(user, connection)
    
    open_bank(user, connection)

def check_balance(user):
    print(f'\nYou have ${user["money"]} in your account.\n')

def edit_account(user, connection):
    print("\nWhat would you like to change...\n")
    print("a. password")
    print("b. name")
    print()
    option = input("Choose an option: ").lower()



    if option == "a":
        change_password(user, connection)
    elif option == "b":
        change_name(user, connection)
    else:
        print("Invalid Input")
        edit_account()

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

def deposit(user, connection):
    amount = input("How much would you like to deposit? ")

    cursor = connection.cursor()
    
    deposit_user_money = (f'UPDATE users SET money = money+{amount} WHERE id={user["id"]}')

    cursor.execute(deposit_user_money)

    update_history = (f'INSERT INTO history (id, type, amount) VALUES ({user["id"]}, \"{"deposit"}\", {amount})')
    cursor.execute(update_history)

    connection.commit()
    cursor.close()

    user["money"] += Decimal(amount)
    print("Deposited money...")

    

def withdraw(user, connection):
    amount = input("How much would you like to withdraw? ")

    cursor = connection.cursor()
    
    withdraw_user_money = (f'UPDATE users SET money = money-{amount} WHERE id={user["id"]}')

    cursor.execute(withdraw_user_money)

    update_history = (f'INSERT INTO history (id, type, amount) VALUES ({user["id"]}, \"{"withdrawal"}\", {amount})')
    cursor.execute(update_history)

    connection.commit()
    cursor.close()

    user["money"] -= Decimal(amount)
    print("Widthdrew money...")

def show_history(user, connection):
    cursor = connection.cursor()

    get_history = (f'SELECT * FROM history WHERE id={user["id"]}')

    cursor.execute(get_history)

    for row in cursor:
        print(f'{row[1].title()} of ${row[2]}')
    
    print()