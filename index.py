import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
import mysql.connector
import connection
import pdb
import scrape
import argparse

class Index():
    def __init__(self):
        connectionDB_obj = connection.ConnectionDB()
        self.mydb = connectionDB_obj.connect_db()             
        self.mycursor = self.mydb.cursor()
    
    #returns mydb object
    def get_mydb(self):
        return self.mydb

    #returns mycursor object
    def get_mycursor(self):
        return self.mycursor
    
    #fetches query
    def fetch_fromDB(self,query):
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

def main():
    index_obj = Index()
    mydb = index_obj.get_mydb()
    mycursor = index_obj.get_mycursor()

    #argparse
    parser = argparse.ArgumentParser(description = "Find pages")
    parser.add_argument('pages',type = int,help = 'Number of pages to fetch')
    args = parser.parse_args()

    #creating empty dictionary
    author_dict = {}   
    tag_dict = {}
    quote_dict = {}
    quoteTag_dict = {}

    #stores value from database to dictionary
    query = "SELECT * FROM author"
    store_result = index_obj.fetch_fromDB(query)
    for row in store_result:
        author_dict[row[2]] = [row[0],row[1],row[3]]         

    #stores value from database to dictionary
    query = "SELECT * FROM tag"
    store_result = index_obj.fetch_fromDB(query)
    for row in store_result:
        tag_dict[row[1]] = row[0]                     
    
    #stores value from database to dictionary                                                
    query = "SELECT * FROM quotes"
    store_result = index_obj.fetch_fromDB(query)
    for row in store_result:
        quote_dict[row[1]] = [row[0],row[2]]

    #stores value from database to dictionary
    query = "SELECT * FROM quote_tag"
    store_result = index_obj.fetch_fromDB(query)
    for row in store_result:
        if row[0] in quoteTag_dict:
            quoteTag_dict[row[0]].append(row[1])
        else:                        
            quoteTag_dict[row[0]] = [row[1]]                

    #create class object
    scrapeobj = scrape.Scrape(quote_dict,author_dict,tag_dict,quoteTag_dict) 
    
    #fetching root URL
    Scrape_URL = 'http://toscrape.com' 
    response = urllib2.urlopen(Scrape_URL)            
    html_contents = response.read()           
    beautifulSoup_obj = BeautifulSoup(html_contents, 'html.parser')     

    #finds "A website" in all anchor tag and saves in the root URL
    for anchor_tag in beautifulSoup_obj.find_all('a', href = True): 
        if anchor_tag.text == "A website":          
            Scrape_URL = anchor_tag['href']               
    #getting response from the urllib2 request
    response = urllib2.urlopen(Scrape_URL)            
    html_contents = response.read()           
    beautifulSoup_obj = BeautifulSoup(html_contents, 'html.parser') #creates beautifulSoup_obj object from html content

    #takes total page number in the argument 
    page_count = args.pages

    #looping through number of page
    for page_no in range(1,page_count+1):
        for quote_div in beautifulSoup_obj.find_all('div',class_ = 'quote'): 
            author_name = quote_div.find('small',class_ = 'author').text
            author_id = scrapeobj.getAuthorId(author_name) 
            #checks if author_id exists
            if not author_id:                                 
                for anchor_tag in quote_div.find_all('a', href = True):
                    if anchor_tag.text == "(about)":     
                        Scrape_URL = "http://quotes.toscrape.com" + anchor_tag['href'] 
                        response = urllib2.urlopen(Scrape_URL)
                        html_contents = response.read()
                        author_beautifulSoup_obj = BeautifulSoup(html_contents, 'html.parser') 
                        name = author_beautifulSoup_obj.find('h3',class_ = 'author-title').text
                        desc = author_beautifulSoup_obj.find('div',class_ = 'author-description').text
                        date = author_beautifulSoup_obj.find('span',class_ = 'author-born-date').text
                        author_id = scrapeobj.author(name,desc,date)

            quote_id = scrapeobj.quote(quote_div.find('span',class_ = 'text').text,author_id)
            tags = quote_div.find_all('a',class_ = 'tag')
            for tag in tags:    
                tag_id = scrapeobj.tags_function(tag.text)
                scrapeobj.qoute_tag(quote_id,tag_id)

        #increments the page number
        Scrape_URL = "http://quotes.toscrape.com/page/" + str(page_no + 1)     
        response = urllib2.urlopen(Scrape_URL)           
        html_contents = response.read()          
        beautifulSoup_obj = BeautifulSoup(html_contents, 'html.parser') 
    mydb.commit()

if __name__ == "__main__":
    main()