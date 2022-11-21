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
            #hopefully things won't go to shit.
            #update 2:40: IT WENT TO SHIT.
            insert_new_user = "INSERT INTO login_test (id, gebruikersnaam, wachtwoord, is_admin) VALUES (?, ?, ?, ?)"
            new_user = (1, user, password, admin)
            print(f'(new_user)')
        
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
        return "a"
    
    def delete_user(self, user):
        return "sports"
        