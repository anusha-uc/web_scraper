from flask import Flask
import requests
from bs4 import BeautifulSoup
import re
import mysql.connector

app = Flask(__name__)
@app.route("/")
def fetchTables():
    mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="scrape"
)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM author")
    res=mycursor.fetchall()
    response=""
    for r in res:
        response=response+"<p>"+"Id : "+str(r[0])+"<br> Name : "+str(r[2])+"<br> Description : "+str(r[1])+"<br> DOB : "+str(r[3])+"<br><br><br><br><br></p>"+"<br><br><br><br><br>"
    return response