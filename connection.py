import mysql.connector as mysql
from credentials import Credential


class ConnectionDB(Credential):
    # gets data from credentials.py
    def __init__(self):
        Credential.__init__(self)

    # returns database connection object
    def start(self):
        database = mysql.connect(
            host=self.host,
            user=self.user_name,
            password=self.password,
            database=self.database_name
        )
        return database
