# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:50:05 2017

@author: Zachary Oleitschuk
"""
import psycopg2


def get_top_articles():
    # Connect to the news db and create a cursor object
    conn = psycopg2.connect('dbname=news')
    cursor = conn.cursor()

    query_string = """
        SELECT articles.title, path_views.views
        FROM articles
        JOIN
            (SELECT replace(path,'-',' ') as title, count(*) as views
                FROM log
                WHERE method='GET'
                    AND status='200 OK'
                    AND path!='/'
                GROUP BY path
                ORDER BY views DESC
            ) AS path_views
        ON replace(
                lower(replace(articles.title, '''', '')),
                   'there are a lot of',
                   'so many')
            LIKE concat(
                '%',
                replace(path_views.title, '/article/', ''),
                '%')
        ORDER BY path_views.views DESC
        LIMIT 3;
        """
    cursor.execute(query_string)
    rows = cursor.fetchall()

    # Print results to the command line
    for row in rows:
        print('"' + row[0] + '"' + ' - ' + str(row[1]) + ' views')

    # Close the cursor and connection
    cursor.close()
    conn.close()


def get_authors_by_views():
    # Connect to the news db and create a cursor object
    conn = psycopg2.connect('dbname=news')
    cursor = conn.cursor()

    query_string = """
        SELECT authors.name, sum(article_views.views) as author_views
        FROM authors
        JOIN
            (SELECT * FROM articles
                JOIN
                    (SELECT replace(path,'-',' ') as title, count(*) as views
                        FROM log
                        WHERE method='GET'
                            AND status='200 OK'
                            AND path!='/'
                        GROUP BY path
                        ORDER BY views DESC
                    ) AS path_views
                ON replace(
                        lower(replace(articles.title, '''', '')),
                        'there are a lot of',
                        'so many')
                    LIKE concat(
                        '%',
                        replace(path_views.title, '/article/', ''),
                        '%')
            ) AS article_views
        ON authors.id=article_views.author
        GROUP BY authors.id
        ORDER BY author_views DESC;
        """

    cursor.execute(query_string)
    rows = cursor.fetchall()

    # Print results to the command line
    for row in rows:
        print(row[0] + ' - ' + str(row[1]))

    # Close the cursor and connection
    cursor.close()
    conn.close()


def get_error_log():
    conn = psycopg2.connect('dbname=news')
    cursor = conn.cursor()

    query_string = """
        SELECT a.date, (CAST(a.requests AS FLOAT)*100/(a.requests+b.requests))
            FROM
                (SELECT date(time) AS date, status, count(*) AS requests
                    FROM log
                    GROUP BY date, status) AS a,
                (SELECT date(time) AS date, status, count(*) AS requests
                    FROM log
                    GROUP BY date, status) AS b
            WHERE a.date=b.date
                AND a.status!='200 OK'
                AND a.status!=b.status
                AND (CAST(a.requests AS FLOAT)*100/(a.requests+b.requests))>1
            ORDER BY a.date DESC;
    """

    cursor.execute(query_string)
    rows = cursor.fetchall()

    # Print results to the command line
    for row in rows:
        print(str(row[0]) + ' - ' + str(round(row[1], 1)) + '% errors')

    # Close the cursor and connection
    cursor.close()
    conn.close()


if __name__ == '__main__':
    print('Top 3 artciles by number of views:')
    print('----------------------------------')
    get_top_articles()
    print('\nAuthor Ranking by total article views:')
    print('--------------------------------------')
    get_authors_by_views()
    print('\nDays where more than 1% of requests resulted in an error:')
    print('-----------------------------------------------------------')
    get_error_log()
