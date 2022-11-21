import sqlite3
from sqlite3 import OperationalError
import os

class ManageUser:
    """This class is used to manage users."""

    def __init__(self, database_file): #copypasta van tablemodel.py, don't reinvent the wheel.
        self.database_file = database_file
        if not os.path.exists(self.database_file):
            raise FileNotFoundError(f"Could not find database file: {database_file}")

    #add new user
    def add_new_user(self, user, password, admin): #copypasta van demodatabase.py
        try:
            connection = sqlite3.connect(self.database_file)
            
            cursor = connection.cursor()
        
            #SQL statement to insert new user, didn't pass along the id bc it's on auto-increment anyways.
            #okay fixed the auto-increment issue. only thing that's left now is the admin stuff
            insert_new_user = "INSERT INTO login_test (gebruikersnaam, wachtwoord, is_admin) VALUES (?, ?, ?)"
            new_user = (user, password, admin)
        
            cursor.execute(insert_new_user, new_user)
            connection.commit()
            print('test')
            connection.close()

        except OperationalError as e:
            print(f"Error opening database file {self.database_file}")
            raise e 
        
    def edit_user(self, user, password, admin):
        return "e"

    def check_user(self, user, password):
        try:
            connection = sqlite3.connect(self.database_file)
            
            cursor = connection.cursor()
        
            #SQL statement to check if user is present in db
            check_user = "SELECT * FROM login_test WHERE gebruikersnaam = ? AND wachtwoord = ?"
            login_user = (user, password)
            print('test')

            cursor.execute(check_user, login_user)
            user = cursor.fetchall()
            
            connection.commit()
            connection.close()

        except OperationalError as e:
            print(f"Error opening database file {self.database_file}")
            raise e 
        return user
    
    def delete_user(self, user):
        return "a sports"
        