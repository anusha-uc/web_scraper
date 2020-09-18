import mysql.connector as mysql
import credentials


class ConnectionDB:
    # gets data from credentials.py
    def __init__(self):
        credential_obj = credentials.Credential()
        self.user_name = credential_obj.get_username(credential_obj)
        self.password = credential_obj.get_password(credential_obj)
        self.host = credential_obj.get_host(credential_obj)
        self.database_name = credential_obj.get_databaseName(credential_obj)

    # returns database connection object
    def connect_db(self):
        database = mysql.connect(
            host=self.host,
            user=self.user_name,
            password=self.password,
            database=self.database_name
        )
        return database
