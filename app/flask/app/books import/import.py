import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://xdsltfznyrmffg:3ac7542170c59e36bbcf57e5619b90f57c8d538be0ce3f892fc45db0eb403ac0@ec2-174-129-253-125.compute-1.amazonaws.com:5432/d8b2l04n622ohs")
db = scoped_session(sessionmaker(bind=engine))

def bookimport():
    reader = csv.reader(open("books.csv"))
    for isbn, title, author, year in reader:
        if isbn == "isbn":
            continue
        else:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                        {"isbn": isbn, "title": title, "author": author, "year": year})
            print(f"Added {title} written by {author} in {year}.")
    db.commit()
