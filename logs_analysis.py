#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A number of functions for printing a number of useful metrics on a local news
PostgreSQL database to the command line.

Created on Thu Jul 13 11:50:05 2017

@author: Zachary Oleitschuk
"""
import psycopg2


def execute_query(query):
    """Executes a query on the  news database and returns resutls.

    Connects to and queries the local news db based on the passed query arg.
    Then closes the connection to the database and returns the result of the
    query.

    Args:
        query - string containing sql to be executed

    Returns:
        results - the results of executing the input query string
    """
    conn = psycopg2.connect('dbname=news')
    cursor = conn.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return results


def get_top_articles():
    """Prints top 3 articles by views to command line.

    Connects to and queries the local news db for the top 3 articles based
    on the number of successful views of the article. A sorted list of pairs
    of article - article views is then printed to the command line and the db
    connection is closed.

    Args:
        n/a

    Returns:
        n/a
    """

    # We query the news db in order to return an ordered table of articles and
    # article view pairs. By joining the log and articles tables on
    # log.path and articles.slug columns we get a table of total article
    # views.
    query = """
        SELECT articles.title, path_views.views
        FROM articles
        JOIN
            (SELECT path, count(*) as views
                FROM log
                WHERE method='GET'
                    AND status='200 OK'
                    AND path!='/'
                GROUP BY path
            ) AS path_views
        ON path_views.path LIKE concat('%', articles.slug, '%')
        ORDER BY path_views.views DESC
        LIMIT 3;
        """

    results = execute_query(query)

    # Print results to the command line
    for title, views in results:
        print('"{}" - {} views'.format(title, views))


def get_authors_by_views():
    """Prints an ordered list of authors based on number of article views

    Connects to and queries the local news db for all article authors and
    orders that list by the total number of article views each author has
    received in descending order. A sorted list of pairs of author - total
    article views is then printed to the command line and the db connection is
    closed.

    Args:
        n/a

    Returns:
        n/a
    """

    # We query the news db in order to return an ordered table of author and
    # article view pairs. By joining the log and articles tables on modified
    # log.path and articles.title columns we a table of total article views.
    # We can then join that table with the authors table on the FK relationship
    # and group by author while summing on article views to get a table of
    # authors and their total article views.
    query = """
        SELECT authors.name, sum(article_views.views) as author_views
        FROM authors
        JOIN
            (SELECT * FROM articles
                JOIN
                    (SELECT path, count(*) as views
                        FROM log
                        WHERE method='GET'
                            AND status='200 OK'
                            AND path!='/'
                        GROUP BY path
                    ) AS path_views
                ON path_views.path LIKE  concat('%', articles.slug, '%')
            ) AS article_views
        ON authors.id=article_views.author
        GROUP BY authors.id
        ORDER BY author_views DESC;
        """

    results = execute_query(query)

    # Print results to the command line
    for author, views in results:
        print('{} - {}'.format(author, views))


def get_error_log():
    """Prints a list of all days where error percent was greater than 1%

    Connects to and queries the local news db for all dates that had more than
    1% of requests that resulted in an error and sorts dates in descending
    order. A sorted list of date - error percent pairs is then printed to the
    command line and the db connection is closed.

    Args:
        n/a

    Returns:
        n/a
    """

    # We query the db to get pairs of dates and error percentages where
    # the error percentage is greater than 1% by performing a filtered self-
    # join on the log table. The self-join results in a.requests containing
    # a count of the failed requests and b.requests containing a count of
    # the successful requests.
    query = """
        SELECT a.date, (CAST(a.requests AS FLOAT)*100/(b.requests))
            FROM
                (SELECT date(time) AS date, count(*) AS requests
                    FROM log
                    WHERE status!='200 OK'
                    GROUP BY date) AS a,
                (SELECT date(time) AS date, count(*) AS requests
                    FROM log
                    GROUP BY date) AS b
            WHERE a.date=b.date
                AND (CAST(a.requests AS FLOAT)*100/(b.requests))>1
            ORDER BY a.date DESC;
    """

    results = execute_query(query)

    # Print results to the command line
    for date, err_percent in results:
        print('{:%B %d, %Y} - {:.1f}% errors'.format(date, err_percent))


if __name__ == '__main__':
    title = 'Top 3 artciles by number of views:'
    print(title)
    print('-' * len(title))
    get_top_articles()

    title = '\nAuthor Ranking by total article views:'
    print(title)
    print('-' * len(title))
    get_authors_by_views()

    title = '\nDays where more than 1% of requests resulted in an error:'
    print(title)
    print('-' * len(title))
    get_error_log()
