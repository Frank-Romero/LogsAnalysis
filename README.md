# FSND Logs Analysis

This is the 3rd project in the Udacity FSND program, using Python and SQL to
analyze data from the news database. The file LogsAnalysis.py contains 3 methods:


get_top_pop_articles() is used to get the three most popular articles. It does this using Python's 
psycopg2 module, allowing the use of a SQL query that counts the items in the path column of the 
table log that are similar to the slug column in the table articles giving an accurate number of
the number of views an article gets. The results returned are limited to the first 3 highest results
and the corresponding article's title is also returned.


get_pop_authors() is used to get the list of authors sorted by popularity. It does this using Python's 
psycopg2 module, allowing the use of a SQL query that joins the num column from the table authors to a
subquery foo on the condition that the id column of the table authors is the same as the author column
of the subquery foo. Subquery foo counts the number of items in the path column of the table log that 
are similar to the slug column in the table articles giving an accurate number of the number of views
an article gets. The accumulated results are then further grouped under the items of the author column 
from the table articles in a descending order. An accurate count of the total article views each author
has received is returned in that descending order, along with the corresponding count's author.


get_high_errors() is used to get the days that have experienced errors greater than 1% of that day's views. 
It does this using Python's psycopg2 module, allowing the use of a SQL query that counts the number of times
that each item, organized into a more legible date format, in the time column has experienced a 404 error and
counts the total number of queries. This count of totals and errors is done within two seperate subqueries, where
the status column is counted and grouped by the time column, and then for the errors only incremented when the 
status column matches the corresponding 404 error. The results of the 404 count, num1, are divided by the results 
of the total count, denom1, and are cast as decimal, multiplied by 100, and rounded to provide a percentage 
instead of decimal. The resulting item is returned only if the result is greater than 1, and it is returned 
with the associated day formatted to be easily read. 


This project was created with Python 2.7.12, so Python 2.7.X should be used.
The following steps to run the project:

-download and unzip the provided logsAnalysis.zip file containing the files

-download and unzip https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

-load the data using psql -d news -f newsdata.sql

-navigate to the newly unzipped logsAnalysis folder

-run LogsAnalysis.py