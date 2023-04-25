from random import randint

#Given an account number and pin return the first user that has a matching account number and pin
def user_login(connection, account_number, pin):
   cursor = connection.cursor()

   query = (f'SELECT * FROM users WHERE accountNumber = \"{account_number}\" AND pin = \"{pin}\"')

   cursor.execute(query)

   column_names = [col[0] for col in cursor.description]

   response = cursor.fetchone()

   #Convert the user to a dictionary where each column title corresponds to teh user's value in that column
   user = dict((column_names[i], response[i]) for i in range(len(response)))
   return user

#Create a new account given a name and password
def create_account(connection, name, password):
   account_number = generate_account_number()

   cursor = connection.cursor()

   #Add a new account into the users table
   addUser = (f'INSERT INTO users (accountNumber, pin, name, money) VALUES ({account_number}, \"{password}\", \"{name}\", 50)')

   cursor.execute(addUser)

   connection.commit()
   cursor.close()

   #Return the user by logging him in
   return user_login(connection, account_number, password)

#Generate a random 7-digit number and return it as an account number
def generate_account_number():
   numb = ""
   for i in range(7):
      numb += str(randint(0, 9))
   return int(numb)