# Logs-Analysis-Project
A tool designed to be run from the command line to produce internal reports for a news website on their local news PostgreSQL database. The tool uses python to query the database with SQL and the psycopg2 library in order to return summaries on:
* the top 3 most viewed articles,
* a ranked list of authors based on total number of article views, and
* a log of all dates that had more than 1% of all requests result in an error.
# Getting Started
1. Make sure you have the news database up and running locally.
2. Run the logs analysis tool by typing `python3 logs_analysis.py` in the command line.
3. Revel in the glory of the summarized data now instantly available to you.
