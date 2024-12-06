from calibre_db import Authors, Books

def get_authors() -> dict:
    query = Authors.select()
    authors = {}
    for entry in query:
        authors[entry.id] = entry
    return authors

def get_books() -> dict:
    query = Books.select()
    books = {}
    for entry in query:
        books[entry.id] = entry
    return books

class CalibreMetadata():
    def __init__(self):
        self.authors = get_authors()
        self.books = get_books()
    def __str__(self):
        return f'{{Authors: {self.authors}, Books: {self.books}}}'