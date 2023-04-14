from random import randint

def login(connection):
   print("a. Login")
   print("b. Create Account")
   print()
   choice = input("Select an option: ")
   choice = choice.lower()

   if choice == "a": user = user_login(connection)
   elif choice == "b": user = create_account(connection)
   else:
      print("\nInvalid Input!\n")
      login()

   return user

def user_login(connection):
   print()
   account_number = input("Account Number: ")
   pin = input("7-digit Pin: ")

   cursor = connection.cursor()

   query = (f'SELECT * FROM users WHERE accountNumber = {account_number} AND pin = \"{pin}\"')

   cursor.execute(query)

   column_names = [col[0] for col in cursor.description]

   response = cursor.fetchone()

   user = dict((column_names[i], response[i]) for i in range(len(response)))
   return user

def create_account(connection):
   name = input("Name: ")
   password = input("Set a password (7 characters or less): ")
   account_number = generate_account_number()

   print(f'Your account number is {account_number}. Make sure to save this number!')

   cursor = connection.cursor()

   addUser = (f'INSERT INTO users (id, accountNumber, pin, name, money) VALUES ({account_number}, \"{password}\", \"{name}\", 50)')

   cursor.execute(addUser)

   connection.commit()
   cursor.close()

   print()
   print("Login: ")
   return user_login(connection)

def generate_account_number():
   numb = ""
   for i in range(7):
      numb += str(randint(0, 9))
   return int(numb)