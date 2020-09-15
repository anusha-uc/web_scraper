Web Scraping

* Create database name as scrape.
* Restore the SQL dump file attached in the folder.
* With SQL server running, 
	-> Open scrape_app folder.
	-> Run index.py file in terminal/cmd (fetches the data from toscrape.com site and stores the data in the database).

Explanation on Database table:
* Tables are as follows:
	-> author (id, Description, name, DOB)
	-> quotes (id, quote, author_id) => (author_id is the foreign key for id from author table)
	-> quote_tag (q_id, t_id) => (these are the foreign keys of quote id and tag id)
	-> tag (id, name)

Front end : Flask (for displaying the table)
	   
Insatallation of Flask
	-> pip install Flask (in cmd/terminal)
	-> pip install virtualenv 

	-> Go to scrape_app folder
	-> go to front end folder
	-> In terminal/cmd, 
		=> to get all the tables,run commands for the following tables
		1) author table
		   	env FLASK_APP=author_table.py flask run
		2) quotes table
	   		env FLASK_APP=quote_table.py flask run
		3) quote_tag table
			env FLASK_APP=quote_tag _table.py flask run
		4) tag table
			env FLASK_APP=tag_table.py flask run
		
		To view author, quotes and tags together,
		->env FLASK_APP=seequote.py flask run


