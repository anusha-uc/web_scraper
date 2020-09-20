import mysql.connector
from connection import ConnectionDB
import pdb


class Scrape(ConnectionDB):
    def __init__(self):
        
        ConnectionDB.__init__(self)
        # connectionDb_obj = connection.ConnectionDB()
        self.mydb = self.start()
        self.mycursor = self.mydb.cursor()

        # stores value from database to dictionary
        select_query = "SELECT * FROM author"
        store_result = self.fetch_fromDB(select_query)
        self.authors = {}
        for row in store_result:
            self.authors[row[2]] = [row[0], row[1], row[3]]

        # stores value from database to dictionary
        select_query = "SELECT * FROM tag"
        store_result = self.fetch_fromDB(select_query)
        self.tags = {}
        for row in store_result:
            self.tags[row[1]] = row[0]

        # stores value from database to dictionary
        select_query = "SELECT * FROM quotes"
        store_result = self.fetch_fromDB(select_query)
        self.quotes = {}
        for row in store_result:
            self.quotes[row[1]] = [row[0], row[2]]

        # stores value from database to dictionary
        select_query = "SELECT * FROM quote_tag"
        store_result = self.fetch_fromDB(select_query)
        self.qoute_tags = {}
        for row in store_result:
            if row[0] in self.qoute_tags:
                self.qoute_tags[row[0]].append(row[1])
            else:
                self.qoute_tags[row[0]] = [row[1]]

        
        # self.quotes = quote  # {'quote':[id,author_id] }
        # self.authors = author  # {'name':[id,description,dob]}
        # self.tags = tag       # {'tag':id}
        # self.qoute_tags = qoute_tag  # {'qid':tagid}

      # fetches query
    def fetch_fromDB(self, select_query):
        self.mycursor.execute(select_query)
        return self.mycursor.fetchall()


    # insert into author table

    def author(self, name, description, dob):
        self.mycursor.execute(
            "insert into author (name,Description,DOB) values(%s,%s,%s)", (name, description, dob))
        author_id = self.mycursor.lastrowid
        self.authors[name] = [author_id, description, dob]
        self.mydb.commit()
        return author_id

    # returns author id
    def getAuthorId(self, name):
        if name in self.authors:
            return self.authors[name][0]
        else:
            return False

    # checks for existing quotes and then inserts into table
    def quote(self, quote, author_id):
        if quote in self.quotes:
            return self.quotes[quote][0]
        self.mycursor.execute(
            "INSERT INTO quotes (quote,author_id) VALUES (%s,%s)", (quote, author_id))
        quote_id = self.mycursor.lastrowid
        self.quotes[quote] = [quote_id, author_id]
        self.mydb.commit()
        return quote_id

    # checks for tag id. if exists, inserts into tag table
    def tags_function(self, tag):
        if tag in self.tags:
            return self.tags[tag]
        else:
            self.mycursor.execute("insert into tag (name) values(%s)", (tag,))
            tag_id = self.mycursor.lastrowid
            self.tags[tag] = tag_id
            self.mydb.commit()
            return tag_id

    # checks for quote id and tag id and inserts
    def qoute_tag(self, qoute_id, tag_id):
        if qoute_id in self.qoute_tags:
            if tag_id not in self.qoute_tags[qoute_id]:
                self.mycursor.execute(
                    "insert into quote_tag (q_id,t_id) values(%s,%s)", (qoute_id, tag_id))
                self.qoute_tags[qoute_id].append(tag_id)
        else:
            self.qoute_tags[qoute_id] = [tag_id]
            self.mycursor.execute(
                "insert into quote_tag (q_id,t_id) values(%s,%s)", (qoute_id, tag_id))
        self.mydb.commit()
