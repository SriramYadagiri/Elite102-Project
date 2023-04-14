# TODO
# - Add adminstrators
# - Implement check balance
# - Implement deposit
# - Implement withdraw
# - Allow users to close accounts
# - Admins should be able to close and modify other accounts

import mysql.connector
from login import login
from banking import open_bank
from os import system

connection = mysql.connector.connect(user = "root", database = "bank", password = "Leg8iesh")

def main():
   print("Welcome to Sriram's Banking!\n")
   user = login(connection)
   system("cls")
   print(f'Hi {user["name"]}\n')
   open_bank(user, connection)

if __name__ == '__main__':
   main()
   connection.close()