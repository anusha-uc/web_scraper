import mysql.connector
import connection
#import pdb

mydb = connection.connect_db()             #databaseconnection
mycursor = mydb.cursor()

class Scrape:
    def __init__(self,quote,author,tag,qoute_tag):
        self.quotes=quote   #{'quote':[id,author_id] }
        self.authors=author  # {'name':[id,description,dob]}
        self.tags=tag       # {'tag':id}
        self.qoute_tags=qoute_tag # {'qid':tagid}

    def author(self,name,description,dob):
        mycursor.execute("insert into author (name,Description,DOB) values(%s,%s,%s)",(name,description,dob)) #storing to database
        author_id=mycursor.lastrowid 
        self.authors[name]=[author_id,description,dob]
        mydb.commit()
        return author_id

    def getAuthorId(self,name):
        if name in self.authors:
            return self.authors[name][0] 
        else:
            return False

    def quote(self,quote,author_id):
        if quote in self.quotes:
            return self.quotes[quote][0]
        mycursor.execute("INSERT INTO quotes (quote,author_id) VALUES (%s,%s)", (quote,author_id))
        quote_id=mycursor.lastrowid
        self.quotes[quote]=[quote_id,author_id]
        mydb.commit()
        return quote_id

    def tags_function(self,tag):
        if tag in self.tags:
            return self.tags[tag] 
        else:
            mycursor.execute("insert into tag (name) values(%s)",(tag,)) #storing to database
            tag_id=mycursor.lastrowid 
            self.tags[tag]=tag_id
            mydb.commit()
            return tag_id
    
    def qoute_tag(self,qoute_id,tag_id):
        mycursor.execute("insert into quote_tag (q_id,t_id) values(%s,%s)",(qoute_id,tag_id))
        mydb.commit()
        if qoute_id in self.qoute_tags:
            self.qoute_tags[qoute_id].append(tag_id)
        else:
            self.qoute_tags[qoute_id]=[tag_id]


    # def deleteRecords(self):
    #     mycursor.execute("DELETE FROM author")
    #     mycursor.execute("DELETE FROM quotes")
    #     mycursor.execute("DELETE FROM quote_tag")
    #     mycursor.execute("DELETE FROM tag")
    #     mydb.commit()