#!/usr/bin/env python2.7.12

import psycopg2


DBNAME = "news"


"""get the three most popular articles in desc order"""


def get_top_pop_articles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select articles.title, count(log.path) as num from articles,
                    log where log.path = concat('/article/', articles.slug) and
                    log.status = '200 OK' group by articles.title order by num
                    desc limit 3;
                """)
    top_articles = c.fetchall()
    count = 1
    for title, num in top_articles:
        print '\n  {}: "{}" -- {} views \n'.format(count, title, num)
        count += 1
    db.close()
    return top_articles


"""get the list of authors by order of popularity"""


def get_pop_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select authors.name, num from authors join (select
                    articles.author, count(log.path) as num from articles, log
                    where log.path = concat('/article/', articles.slug) and
                    log.status = '200 OK' group by articles.author order by num
                    desc) foo on authors.id = foo.author;
                """)
    top_authors = c.fetchall()
    count = 1
    for name, num in top_authors:
        print '\n  {}: {} -- {} views \n'.format(count, name, num)
        count += 1
    db.close()
    return top_authors


"""get the days that have greater than 1% of errors"""


def get_high_errors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select num1.day1 as day, (round(100 * (cast(num1.num as
                    decimal(18,3))/cast(denom1.denom as decimal(18,3))), 2) ||
                    '% errors') as errors from (select to_char(log.time,
                    'FMMonth DD, YYYY') as day1, count(log.status) as num
                    from log where log.status = '404 NOT FOUND' group by
                    to_char(log.time, 'FMMonth DD, YYYY') order by
                    to_char(log.time, 'FMMonth DD, YYYY')) as num1 join (select
                    to_char(log.time, 'FMMonth DD, YYYY') as day1,
                    count(log.status) as denom from log group by to_char
                    (log.time, 'FMMonth DD, YYYY') order by to_char(log.time,
                    'FMMonth DD, YYYY')) as denom1 on num1.day1 = denom1.day1
                    where (100 * round(cast(num1.num as decimal(18,2))/cast
                    (denom1.denom as decimal(18,2)), 3)) > 1
                    order by num1.day1;
                """)
    high_errors = c.fetchall()
    count = 1
    for day, errors in high_errors:
        print '\n  {}: {} -- {}\n'.format(count, day, errors)
        count += 1
    db.close()
    return high_errors


print "1. What are the most popular three articles of all time?"
get_top_pop_articles()
print "2. Who are the most popular article authors of all time?"
get_pop_authors()
print "3. On which days did more than 1% of requests lead to errors?"
get_high_errors()
