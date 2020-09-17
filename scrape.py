import mysql.connector
import connection
import pdb

class Scrape:
    def __init__(self,quote,author,tag,qoute_tag):
        connectionDb_obj=connection.ConnectionDB()
        self.mydb = connectionDb_obj.connect_db()             
        self.mycursor = self.mydb.cursor()
        self.quotes = quote   #{'quote':[id,author_id] }
        self.authors = author  # {'name':[id,description,dob]}
        self.tags = tag       # {'tag':id}
        self.qoute_tags = qoute_tag # {'qid':tagid}

    
    #insert into author table
    def author(self,name,description,dob):
        self.mycursor.execute("insert into author (name,Description,DOB) values(%s,%s,%s)",(name,description,dob)) 
        author_id = self.mycursor.lastrowid 
        self.authors[name] = [author_id,description,dob]
        self.mydb.commit()
        return author_id

    #returns author id
    def getAuthorId(self,name):
        if name in self.authors:
            return self.authors[name][0] 
        else:
            return False

    #checks for existing quotes and then inserts into table
    def quote(self,quote,author_id):
        if quote in self.quotes:
            return self.quotes[quote][0]
        self.mycursor.execute("INSERT INTO quotes (quote,author_id) VALUES (%s,%s)", (quote,author_id))
        quote_id = self.mycursor.lastrowid
        self.quotes[quote] = [quote_id,author_id]
        self.mydb.commit()
        return quote_id

    #checks for tag id. if exists, inserts into tag table
    def tags_function(self,tag):
        if tag in self.tags:
            return self.tags[tag] 
        else:
            self.mycursor.execute("insert into tag (name) values(%s)",(tag,)) 
            tag_id = self.mycursor.lastrowid 
            self.tags[tag] = tag_id
            self.mydb.commit()
            return tag_id
    
    #checks for quote id and tag id and inserts 
    def qoute_tag(self,qoute_id,tag_id):
        if qoute_id in self.qoute_tags:
            if tag_id not in self.qoute_tags[qoute_id]:
                self.mycursor.execute("insert into quote_tag (q_id,t_id) values(%s,%s)",(qoute_id,tag_id))
                self.qoute_tags[qoute_id].append(tag_id)
        else:
            self.qoute_tags[qoute_id] = [tag_id]
            self.mycursor.execute("insert into quote_tag (q_id,t_id) values(%s,%s)",(qoute_id,tag_id))
        self.mydb.commit()
