import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
import mysql.connector
import connection
import pdb
import scrape

mydb = connection.connect_db()             #databaseconnection
mycursor = mydb.cursor()

def main():
    scrapeobj=scrape.Scrape({},{},{},{}) #creating class object and passing empty dict
    scrapeobj.deleteRecords()
    URL = 'http://toscrape.com' #root url
    #page = requests.get(URL)               #stores root url content
    response=urllib2.urlopen(URL)            #response object from url
    html_contents=response.read()           #stores html page content
    soup = BeautifulSoup(html_contents, 'html.parser')     #creates soup object from html content

    pdb.set_trace()         #debugging

    for a in soup.find_all('a', href=True): #find all a tages
        if a.text=="A website":          #check if conc=tent of a tag is "A website"
            URL=a['href']               #IF TRUE COPY THE HREF OF QOUTES
    #page = requests.get(URL)            #GOTO QOUTES PAGE
    response=urllib2.urlopen(URL)            #response object from url
    html_contents=response.read()           #stores html page content
    soup = BeautifulSoup(html_contents, 'html.parser') #creates soup object from html content

    n=int(input("Enter no of pages to scrape : "))
   
    for i in range(1,n+1):
        #pdb.set_trace()
        for quote_div in soup.find_all('div',class_='quote'): #GETTING QOUTE DIV
            author_name=quote_div.find('small',class_='author').text
            author_id=scrapeobj.getAuthorId(author_name) #id or false
            if not author_id:                                 #if id of author not found 
                for a in quote_div.find_all('a', href=True):
                    if a.text=="(about)":     
                        URL="http://quotes.toscrape.com"+a['href'] 
                        response=urllib2.urlopen(URL)
                        html_contents=response.read()
                        author_soup = BeautifulSoup(html_contents, 'html.parser') #getting author info
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
        response=urllib2.urlopen(URL)           #response object from url
        html_contents=response.read()           #stores html page content
        soup = BeautifulSoup(html_contents, 'html.parser') #GETTING DATA
    
if __name__=="__main__":
    main()