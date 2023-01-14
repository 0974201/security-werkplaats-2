import sqlite3
from sqlite3 import OperationalError
import os

class EditTable:
    """idek mane"""

    def __init__(self, database_file): #copypasta van tablemodel.py, don't reinvent the wheel.
        self.database_file = database_file
        if not os.path.exists(self.database_file):
            raise FileNotFoundError(f"Could not find database file: {database_file}")

    #get vraag
    def vraag(self, id): #copypasta van demodatabase.py
        try:
            connection = sqlite3.connect(self.database_file)
            cursor = connection.cursor()
        
            #SQL statement to get vraag from db
            cursor.execute("SELECT * FROM vragen WHERE id = ?", [id])
            vraag = cursor.fetchone()

            connection.close()

        except OperationalError as e:
            print(f"Error opening database file {self.database_file}")
            raise e 
        return vraag
        
    def leerdoel(self, id): #copypasta van demodatabase.py
        try:
            connection = sqlite3.connect(self.database_file)
            cursor = connection.cursor()
        
            #SQL statement to get leerdoel from db
            cursor.execute("SELECT * FROM leerdoelen WHERE id = ?", [id])
            leerdoel = cursor.fetchone()

            connection.close()

        except OperationalError as e:
            print(f"Error opening database file {self.database_file}")
            raise e 
        return leerdoel

    def auteur(self, id): #copypasta van demodatabase.py
        try:
            connection = sqlite3.connect(self.database_file)
            cursor = connection.cursor()
        
            #SQL statement to get auteur from db
            cursor.execute("SELECT * FROM auteurs WHERE id = ?", [id])
            auteur = cursor.fetchone()

            connection.close()

        except OperationalError as e:
            print(f"Error opening database file {self.database_file}")
            raise e 
        return auteur

    def edit_vraag(self, leerdoel, vraag, auteur, id):
        try:
            connection = sqlite3.connect(self.database_file)
            cursor = connection.cursor()
        
            #SQL statement to update an existing user
            update_vraag_qry = "UPDATE vragen SET leerdoel = ?, vraag = ?, auteur = ? WHERE id = ?"
            edit_vraag = (leerdoel, vraag, auteur, id)

            cursor.execute(update_vraag_qry, edit_vraag)
            connection.commit()

            connection.close()

        except OperationalError as e:
            print(f"Error opening database file {self.database_file}")
            raise e
        