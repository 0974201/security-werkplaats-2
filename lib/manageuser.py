import sqlite3
from sqlite3 import OperationalError
import os

class ManageUser:
    """This class is used to manage users."""

    def __init__(self, database_file): #copypasta van tablemodel.py, don't reinvent the wheel.
        self.database_file = database_file
        if not os.path.exists(self.database_file):
            raise FileNotFoundError(f"Could not find database file: {database_file}")

    #check user
    def check_user(self, user, password):
        try:
            connection = sqlite3.connect(self.database_file)
            cursor = connection.cursor()
        
            #SQL statement to check if user is present in db
            check_user_qry = "SELECT * FROM login_test WHERE gebruikersnaam = ? AND wachtwoord = ?"
            login_user = (user, password)

            cursor.execute(check_user_qry, login_user)
            user = cursor.fetchone() #fetchall geeft alle matchende rows terug, fetchone alleen één row of none als t er niet is. 
            connection.commit()

            connection.close()

        except OperationalError as e:
            print(f"Error opening database file {self.database_file}")
            raise e 
        return user