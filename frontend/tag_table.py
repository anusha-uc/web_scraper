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
    mycursor.execute("SELECT * FROM tag")
    res=mycursor.fetchall()
    response=""
    for r in res:
        response=response+"<p>"+"Id : "+str(r[0])+"<br> Tag Name : "+str(r[1])+"</p>"+"<br>"
    return response