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
    tags=""
    authorname=""
    for r in res:
        q=str(r[1])
        mycursor.execute("SELECT * FROM author where ID=(%s)",(str(r[2]),))
        ares=mycursor.fetchall()
        for a in ares:
            authorname=str(a[2])
        mycursor.execute("SELECT t_id FROM quote_tag where q_id=(%s)",(str(r[0]),))
        t_id=mycursor.fetchall()
        for t in t_id:
            mycursor.execute("SELECT name FROM tag where ID=(%s)",(str(t[0]),))
            tag=mycursor.fetchall()
            for ts in tag:
                tags=tags+str(ts[0])+ " , "
        response=response+"<div>"+"<h1>"+authorname+"</h1><p>"+q+"</p>"+"<h6>"+tags+"</h6>"+"</div>"   
        
        
    return response