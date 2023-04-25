from random import randint

def user_login(connection, account_number, pin):
   cursor = connection.cursor()

   query = (f'SELECT * FROM users WHERE accountNumber = \"{account_number}\" AND pin = \"{pin}\"')

   cursor.execute(query)

   column_names = [col[0] for col in cursor.description]

   response = cursor.fetchone()

   user = dict((column_names[i], response[i]) for i in range(len(response)))
   return user

def create_account(connection, name, password):
   account_number = generate_account_number()

   cursor = connection.cursor()

   addUser = (f'INSERT INTO users (accountNumber, pin, name, money) VALUES ({account_number}, \"{password}\", \"{name}\", 50)')

   cursor.execute(addUser)

   connection.commit()
   cursor.close()

   return user_login(connection, account_number, password)

def generate_account_number():
   numb = ""
   for i in range(7):
      numb += str(randint(0, 9))
   return int(numb)