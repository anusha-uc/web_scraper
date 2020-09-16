import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
import mysql.connector
import connection
import pdb
import scrape
import argparse

mydb = connection.connect_db()             #databaseconnection
mycursor = mydb.cursor()

parser=argparse.ArgumentParser(description="Find pages")
parser.add_argument('pages',type=int,help='Number of pages to fetch')
args=parser.parse_args()

def main():
    #creating empty dictionary
    author_dict={}   
    tag_dict={}
    quote_dict={}
    quoteTag_dict={}

    mycursor.execute("SELECT * FROM author")
    store_result=mycursor.fetchall()
    for row in store_result:
        author_dict[row[2]]=[row[0],row[1],row[3]]         #storing row[2] i.e, author name as key in the dictionary 
                                                           #and the other attricutes as list value

    mycursor.execute("SELECT * FROM tag")
    store_result=mycursor.fetchall()
    for row in store_result:
        tag_dict[row[1]]=row[0]                     #storing row[1] i.e,name as key in the dictionary and 
                                                    #id as its key
    mycursor.execute("SELECT * FROM quotes")
    store_result=mycursor.fetchall()
    for row in store_result:
        quote_dict[row[1]]=[row[0],row[2]]

    mycursor.execute("SELECT * FROM quote_tag")
    store_result=mycursor.fetchall()
    for row in store_result:
        if row[0] in quoteTag_dict:
            quoteTag_dict[row[0]].append(row[1])
        else:                        
            quoteTag_dict[row[0]]=[row[1]]                #storing row[1] i.e,quote id as key in the dictionary and 
                                                      #tag id as its key

    scrapeobj=scrape.Scrape(quote_dict,author_dict,tag_dict,quoteTag_dict) #creating class object and passing empty dict
    # scrapeobj.deleteRecords()
    URL = 'http://toscrape.com' #root url
    #page = requests.get(URL)               #stores root url content
    response=urllib2.urlopen(URL)            #response object from url
    html_contents=response.read()           #stores html page content
    soup = BeautifulSoup(html_contents, 'html.parser')     #creates soup object from html content

    #pdb.set_trace()         #debugging

    for a in soup.find_all('a', href=True): #find all a tages
        if a.text=="A website":          #check if conc=tent of a tag is "A website"
            URL=a['href']               #IF TRUE COPY THE HREF OF QOUTES
    #page = requests.get(URL)            #GOTO QOUTES PAGE
    response=urllib2.urlopen(URL)            #response object from url
    html_contents=response.read()           #stores html page content
    soup = BeautifulSoup(html_contents, 'html.parser') #creates soup object from html content

    #n=int(input("Enter no of pages to scrape : "))
    page_count=args.pages
    for i in range(1,page_count+1):
        #pdb.set_trace()
        for quote_div in soup.find_all('div',class_='quote'): #GETTING QOUTE DIV
            author_name=quote_div.find('small',class_='author').text
            author_id=scrapeobj.getAuthorId(author_name) #id or false
            if not author_id:                                 #if id of author not found 
                for anchor_tag in quote_div.find_all('a', href=True):
                    if anchor_tag.text=="(about)":     
                        URL="http://quotes.toscrape.com"+anchor_tag['href'] 
                        response=urllib2.urlopen(URL)
                        html_contents=response.read()
                        author_soup = BeautifulSoup(html_contents, 'html.parser') #getting author info
                        name=author_soup.find('h3',class_='author-title').text
                        desc=author_soup.find('div',class_='author-description').text
                        #if(i==4):
                            #pdb.set_trace()
                        date=author_soup.find('span',class_='author-born-date').text
                        author_id=scrapeobj.author(name,desc,date)
            quote_id=scrapeobj.quote(quote_div.find('span',class_='text').text,author_id)
            tags=quote_div.find_all('a',class_='tag')
            for tag in tags:    #getting tags
                tag_id=scrapeobj.tags_function(tag.text)
                scrapeobj.qoute_tag(quote_id,tag_id)

            

        URL="http://quotes.toscrape.com/page/"+str(i+1) #next url to scrape    
        response=urllib2.urlopen(URL)           #response object from url
        html_contents=response.read()           #stores html page content
        soup = BeautifulSoup(html_contents, 'html.parser') #GETTING DATA
    mydb.commit()
if __name__=="__main__":
    main()