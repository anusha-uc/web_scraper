import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
import connection
import pdb

mydb = connection.connect_db()             #databaseconnection
mycursor = mydb.cursor()

class Scrape:
    def __init__(self,quote,author,tag,qoute_tag):
        self.quotes=quote   #{'' }
        self.authors=author  # {'name':[id,description,dob]}
        self.tags=tag       # {'tag':id}
        self.qoute_tags=qoute_tag # {'qid':tagid}

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
        quote_id=mycursor.lastrowid 
        self.quotes[quote_id]=[quote,author_id]
        return quote_id

    def tags_function(self,tag):
        if tag in self.tags.keys():
            return self.tags[tag] 
        else:
            mycursor.execute("insert into tag (name) values(%s)",(tag,)) #storing to database
            tag_id=mycursor.lastrowid 
            self.tags[tag]=tag_id
            return tag_id
    
    def qoute_tag(self,qoute_id,tag_id):
        mycursor.execute("insert into quote_tag (q_id,t_id) values(%s,%s)",(qoute_id,tag_id))
        if qoute_id in self.qoute_tags.keys():
            self.qoute_tags[qoute_id].append(tag_id)
        else:
            self.qoute_tags[qoute_id]=[tag_id]


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
        pdb.set_trace()
        for quote_div in soup.find_all('div',class_='quote'): #GETTING QOUTE DIV
            author_name=quote_div.find('small',class_='author').text
            author_id=scrapeobj.getAuthorId(author_name) #id or false
            if not author_id:                                 #if id of author not found 
                for a in quote_div.find_all('a', href=True):
                    if a.text=="(about)":     
                        URL="http://quotes.toscrape.com"+a['href'] 
                        page = requests.get(URL)
                        author_soup = BeautifulSoup(page.content, 'html.parser') #getting author info
                        name=author_soup.find('h3',class_='author-title').text
                        desc=str(author_soup.find('div',class_='author-description').text)
                        date=author_soup.find('span',class_='author-born-date').text
                        author_id=scrapeobj.author(name,desc,date)
            quote_id=scrapeobj.quote(quote_div.find('span',class_='text').text,author_id)
            tags=quote_div.find_all('a',class_='tag')
            for tag in tags:    #getting tags
                tag_id=scrapeobj.tags_function(tag.text)
                scrapeobj.qoute_tag(quote_id,tag_id)

            mydb.commit()

        URL="http://quotes.toscrape.com/page/"+str(i+1) #next url to scrape
        
        page = requests.get(URL)            
        soup = BeautifulSoup(page.content, 'html.parser') #GETTING DATA