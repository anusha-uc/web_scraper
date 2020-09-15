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
    mycursor.execute("SELECT * FROM quotes")
    res=mycursor.fetchall()
    response=""
    for r in res:
        response=response+"<p>"+"Id : "+str(r[0])+"<br> Quote : "+str(r[1])+"<br> author_id : "+str(r[2])+"<br></p>"+"<br><br>"
    return response