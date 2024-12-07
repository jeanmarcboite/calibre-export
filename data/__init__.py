
from calibre_db.metadata import CalibreMetadata
from data.book import Book, Books


class CalibreLibrary():
    def read(self) -> object:
        self.calibre = CalibreMetadata()
        self.books = Books(self.calibre)

    def __str__(self):
        return f'{self.books}'

library = CalibreLibrary()

