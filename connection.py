import mysql.connector as mysql
from credentials import Credential


class ConnectionDB(Credential):
    # gets data from credentials.py
    def __init__(self):
        Credential.__init__(self)
        # credential_obj = credentials.Credential()
        # self.user_name = credential_obj.get_username(credential_obj)
        # self.password = credential_obj.get_password(credential_obj)
        # self.host = credential_obj.get_host(credential_obj)
        # self.database_name = credential_obj.get_databaseName(credential_obj)
        # self.user_name

    # returns database connection object
    def start(self):
        database = mysql.connect(
            host=self.host,
            user=self.user_name,
            password=self.password,
            database=self.database_name
        )
        return database
