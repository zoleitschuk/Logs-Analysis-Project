# Logs-Analysis-Project
A tool designed to be run from the command line to produce internal reports for a news website on their local news PostgreSQL database. The tool uses python to query the database with SQL and the psycopg2 library in order to return summaries on:
* the top 3 most viewed articles,
* a ranked list of authors based on total number of article views, and
* a log of all dates that had more than 1% of all requests result in an error.
## Getting Started
1. Create the news database in PostgreSQL
	* From the command line, launch the psql console by typing: `psql`
	* Check to see if a news database already exists by listing all databases with the command: `\l`
	* If a news database already exists, drop it with the command: `DROP DATABASE news;`
	* Create the news database with the command: `CREATE DATABASE news;`
exit the console by typing: `\q`
2. Download the schema and data for the news database:
	1. [Click here to download](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
3. Unzip the downloaded file. You should now have an sql script called newsdata.sql.
4. From the command line, navigate to the directory containing newsdata.sql.
5. Import the schema and data in newsdata.sql to the news database by typing: `psql -d news -f newsdata.sql`
6. Run the logs analysis tool by typing `python3 logs_analysis.py` in the command line.
7. Revel in the glory of the summarized data now instantly available to you.
