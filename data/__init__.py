
from calibre_db.metadata import CalibreMetadata
from data.book import Book, Books


class Library():
    def __init__(self):
        self.calibre = CalibreMetadata()
        self.books = Books(self.calibre)

    def __str__(self):
        return f'Library: {{Books: {self.books}}}'

