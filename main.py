# TODO
# - Admins should be able to close and modify other accounts
# - Bunch of bug fixes
# - Make an actual UI

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
   main()

if __name__ == '__main__':
   main()
   connection.close()