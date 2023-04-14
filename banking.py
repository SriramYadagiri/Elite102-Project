from os import system

def open_bank(user, connection):
    system("cls")

    print(f'Hi {user["name"]}')
    display_options(user, connection)

def display_options(user, connection):
    print("\na. Check Balance")
    print("b. Deposit")
    print("c. Withdraw")
    print("d. Edit Your Account")
    print("e. Close Your Account")
    print("f. Logout")
    print()
    option = input("\nChoose an option: ")

    match option.lower():
        case "a":
            check_balance(user)
        case "d":
            edit_account(user, connection)
        case _:
            print("Invalid Option")
            print()
            display_options(user, connection)
            

def check_balance(user):
    print(f'You have ${user["money"]} in your account.')

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

def change_name(user, connection):
    new_name = input("\nWhat do you want to change your name to: ")
    change = input(f'Are you sure you want to change your name to \"{new_name}\" (Y/N) ').lower()

    if change != "n":
        cursor = connection.cursor()

        changeUserName = (f'UPDATE users SET name = \"{new_name}\" WHERE id = {user["id"]}')

        cursor.execute(changeUserName)

        connection.commit()
        cursor.close()