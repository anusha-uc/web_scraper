import mysql.connector
import credentials

def connect_db():
    user_name=credentials.get_username()
    password=credentials.get_password()
    database = mysql.connector.connect(
        host="localhost",
        user=user_name,
        password=password,
        database="scrape"
    )
    return database   


