from typing import Type

from texttable import Texttable
import calibre_db
from calibre_db import Comments
from calibre_db.links import *
from calibre_db.metadata import CalibreMetadata


def pretty(data: list):
    return ", ".join(map(str, data))


class Book(calibre_db.Books):
    def __init__(self, _from: calibre_db.Books):
        super().__init__()
        self.__dict__.update(_from.__dict__)
        self.lang_code = []
        self.author = []
        self.comment = []
        self.publisher = []
        self.rating = []
        self.series = []
        self.tag = []

    def __str__(self):
        return f'{" ,".join(self.pretty_row())}'
    @staticmethod
    def header():
        return ["Title", "Author", "Publisher", "Lang", "Rat.", "Series", "Tags", "Comments"]
    def pretty_row(self):
        return [self.title, pretty(self.author), pretty(self.publisher), pretty(self.lang_code), pretty(self.rating), pretty(self.series), pretty(self.tag), pretty(self.comment)]

class Books(dict):
    def __init__(self, metadata: CalibreMetadata):
        super().__init__()
        self.metadata = metadata
        for k, v in self.metadata.book.items():
            self[k] = Book(v)
        self.append('author', BooksAuthorsLink)
        self.append('publisher', BooksPublishersLink)
        self.append('lang_code', BooksLanguagesLink)
        self.append('rating', BooksRatingsLink)
        self.append('series', BooksSeriesLink)
        self.append('tag', BooksTagsLink)
        self.append_comment()

    def __str__(self):
        book_table = Texttable()
        book_table.set_deco(Texttable.HEADER | Texttable.VLINES)

        book_table.header(["Title", "Author", "Publisher", "Lang", "Rat.", "Series", "Tags", "Comments"])
        book_table.set_cols_align(['l', 'l', 'l', 'c', 'c', 'l', 'l', 'l'])
        book_table.set_cols_width([50, 30, 20, 5, 4, 20, 30, 60])
        for book in self.values():
            book_table.add_row(book.pretty_row())
        return book_table.draw()

    def append(self, attr: str, model: Type[BaseModel]):
        for link in list(model.select()):
            # print(f' {attr} link {link} {link.book} {self[link.book]} link.{attr}={getattr(link, attr)} {getattr(self.metadata, attr)[getattr(link, attr)]}')
            getattr(self[link.book], attr).append(getattr(self.metadata, attr)[getattr(link, attr)])

    def append_comment(self):
         for link in list(Comments.select()):
             self[link.book].comment.append(link.text)
