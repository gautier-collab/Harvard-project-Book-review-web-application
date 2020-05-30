# -------- Harvard-project-Book-review-web-application --------

Screencast presenting my website (before it was containerized): https://www.youtube.com/watch?v=Ll9wzNjucPI

This is a book review web application built as my Project 1 of the Harvard course CS50's Web Programming with Python and JavaScript. It allows signed in users to search books and post reviews. You can also retrieve book data using the website's JSON API. 

The Flask server communicates with a PostgreSQL database hosted on the cloud (on a PAAS named Heroku). 5,000 books from a CSV table have been added to that DB by running import.py.

The website uses an API provided by a book review website called Goodreads in order to display the average rating and the number of reviews that a book has received on Goodreads. Also, if someone makes a GET request to the URL of the website adding /api/"_isbn_" at the end, where "_isbn_" is the ISBN of a book (International Standard Book Number), it will return the corresponding book information in a JSON format.

To launch and access the web application, open the pulled repository in your UNIX terminal and run the following command (without sudo unless the terminal asks it):
# bash run-me.sh
