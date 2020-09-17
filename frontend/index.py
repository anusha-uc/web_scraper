from flask import Flask,render_template
import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
app = Flask(__name__)
@app.route("/quotestable")
def fetchquotestable():
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
    return render_template('quotestable.html',result=res)

@app.route("/authorstable")
def fetchauthorstable():
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
    return render_template("authorstable.html",result=res)

@app.route("/tagstable")
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
    return render_template("tagstable.html",result=res)

if __name__=="__main__":
    app.run()