import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
import mysql.connector
import connection
import pdb
from scrape import Scrape
import argparse

ROOT_URL = 'http://toscrape.com'

class Index(Scrape):
    def __init__(self):
        Scrape.__init__(self)
        # argparse
        parser = argparse.ArgumentParser(description="Find pages")
        parser.add_argument('pages', type=int, help='Number of pages to fetch')
        self.pages = parser.parse_args().pages

    def index_main(self):
        # fetching root URL
        response = urllib2.urlopen(ROOT_URL)
        html_contents = response.read()
        beautifulSoup_obj = BeautifulSoup(html_contents, 'html.parser')

        # finds url using re
        anchor_tag = beautifulSoup_obj.find('a', text=re.compile('A website'))
        Scrape_URL = anchor_tag['href']

        # making the request
        response = urllib2.urlopen(Scrape_URL)
        html_contents = response.read()
        beautifulSoup_obj = BeautifulSoup(html_contents, 'html.parser')

        # looping through number of page
        for page_no in range(1, self.pages + 1):
            for quote_div in beautifulSoup_obj.find_all('div', class_='quote'):
                author_name = quote_div.find('small', class_='author').text
                author_id = self.getAuthorId(author_name)
                # checks if author_id exists
                if not author_id:
                    anchor_tag = quote_div.find(
                        'a', {'href': re.compile(r'^\/author\/')})
                    Scrape_URL = "http://quotes.toscrape.com" + \
                        anchor_tag['href']
                    response = urllib2.urlopen(Scrape_URL)
                    html_contents = response.read()
                    author_beautifulSoup_obj = BeautifulSoup(
                        html_contents, 'html.parser')
                    name = author_beautifulSoup_obj.find(
                        'h3', class_='author-title').text
                    desc = author_beautifulSoup_obj.find(
                        'div', class_='author-description').text
                    date = author_beautifulSoup_obj.find(
                        'span', class_='author-born-date').text
                    author_id = self.author(name, desc, date)

                quote_id = self.quote(quote_div.find(
                    'span', class_='text').text, author_id)
                tags = quote_div.find_all('a', class_='tag')
                for tag in tags:
                    tag_id = self.tags_function(tag.text)
                    self.qoute_tag(quote_id, tag_id)

            # increments the page number
            Scrape_URL = "http://quotes.toscrape.com/page/" + str(page_no + 1)
            response = urllib2.urlopen(Scrape_URL)
            html_contents = response.read()
            beautifulSoup_obj = BeautifulSoup(html_contents, 'html.parser')
        self.mydb.commit()


if __name__ == "__main__":
    index_obj = Index()
    index_obj.index_main()
