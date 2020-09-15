import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
import connection
import pdb

mydb = connection.connect_db()             #databaseconnection
mycursor = mydb.cursor()

class Scrape:
    def __init__(self,quote,author,tag,qouteTag):
        self.quotes=quote   #
        self.authors=author  # {'name':[id,description,dob]}
        self.tags=tag       # {'tag':id}
        self.qouteTag=qouteTag # {'qid':tagid}
    def author(self,name,description,dob):
        mycursor.execute("insert into author (name,Description,DOB) values(%s,%s,%s)",(name,desc,date)) #storing to database
        author_id=mycursor.lastrowid 
        self.authors[name]=[author_id,description,dob]
        return author_id

    def getAuthorId(self,name):
        if name in self.authors.keys():
            return self.authors[name][0] 
        else:
            return False

    def quote(self,quote,author_id):
        mycursor.execute("INSERT INTO quotes (quote,author_id) VALUES (%s,%s)", (quote,author_id))
        q_id=mycursor.lastrowid 
        self.quotes[q_id]=[quote,author_id]
        return q_id
    def tags1(self,tag):
        if tag in self.tags.keys():
            return self.tags[tag] 
        else:
            mycursor.execute("insert into tag (name) values(%s)",(tag,)) #storing to database
            tagId=mycursor.lastrowid 
            self.tags[tag]=tagId
            return tagId
    
    def qoute_tag(self,qoute_id,tag_id):
        mycursor.execute("insert into quote_tag (q_id,t_id) values(%s,%s)",(qoute_id,tag_id))
        if qoute_id in self.qouteTag.keys():
            self.qouteTag[qoute_id].append(tag_id)
        else:
            self.qouteTag[qoute_id]=[tag_id]


    def deleteRecords(self):
        mycursor.execute("DELETE FROM author")
        mycursor.execute("DELETE FROM quotes")
        mycursor.execute("DELETE FROM quote_tag")
        mycursor.execute("DELETE FROM tag")

    
    
    
    
if __name__=="__main__":
    scrapeobj=Scrape({},{},{},{}) #creating class object and passing empty dict
    scrapeobj.deleteRecords()
    URL = 'http://toscrape.com' #root url
    page = requests.get(URL)               #stores root url content
    soup = BeautifulSoup(page.content, 'html.parser')
    for a in soup.find_all('a', href=True): #find all a tages
        if a.text=="A website":          #check if conc=tent of a tag is "A website"
            URL=a['href']               #IF TRUE COPY THE HREF OF QOUTES
    page = requests.get(URL)            #GOTO QOUTES PAGE
    soup = BeautifulSoup(page.content, 'html.parser') #GETTING DATA

    n=int(input("Enter no of pages to scrape : "))
    

    for i in range(1,n+1):
        print(URL)
        for qdiv in soup.find_all('div',class_='quote'): #GETTING QOUTE DIV
            author_name=qdiv.find('small',class_='author').text
            authorId=scrapeobj.getAuthorId(author_name) #id or false
            if not authorId:                                 #if id of author not found 
                for a in qdiv.find_all('a', href=True):
                    if a.text=="(about)":     
                        URL="http://quotes.toscrape.com"+a['href'] 
                        page = requests.get(URL)
                        a_soup = BeautifulSoup(page.content, 'html.parser') #getting author info
                        name=a_soup.find('h3',class_='author-title').text
                        desc=str(a_soup.find('div',class_='author-description').text)
                        date=a_soup.find('span',class_='author-born-date').text
                        authorId=scrapeobj.author(name,desc,date)
            quote_id=scrapeobj.quote(qdiv.find('span',class_='text').text,authorId)
            tags=qdiv.find_all('a',class_='tag')
            for tag1 in tags:    #getting tags
                tagId=scrapeobj.tags1(tag1.text)
                scrapeobj.qoute_tag(quote_id,tagId)

               

                

            mydb.commit()

        URL="http://quotes.toscrape.com/page/"+str(i+1)
        
        page = requests.get(URL)            #GOTO QOUTES PAGE
        soup = BeautifulSoup(page.content, 'html.parser') #GETTING DATA







