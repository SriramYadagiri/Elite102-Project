from os import system

def open_bank(user, connection):
    system("cls")

    print(f'Hi {user["name"]}')
    display_options()

def display_options():
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
            check_balance()
        case _:
            print("Invalid Option")
            print()
            display_options()
            

def check_balance(user):
    print(f'You have ${user["money"]} in your account.')