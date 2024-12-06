from typing import Type

import calibre_db
from calibre_db import BaseModel
from calibre_db.links import BooksAuthorsLink, BooksLanguagesLink, BooksPublishersLink
from calibre_db.metadata import CalibreMetadata


class Book(calibre_db.Books):
    def __init__(self, _from: calibre_db.Books):
        super().__init__()
        self.__dict__.update(_from.__dict__)
        self.lang_code = []
        self.author = []
        self.comment = []
        self.publisher = []

    def __str__(self):
        return f'{self.title}, {self.authors}, {self.publishers}, {self.lang_code}'


class Books(dict):
    def __init__(self, metadata: CalibreMetadata):
        super().__init__()
        self.metadata = metadata
        for k, v in self.metadata.book.items():
            self[k] = Book(v)
        self.append('author', BooksAuthorsLink)
        self.append('publisher', BooksPublishersLink)
        self.append('lang_code', BooksLanguagesLink)

    def __str__(self):
        r = '\n'
        for k, v in self.items():
            r += f'{v.title} ({v.author}, {v.publisher}) [{v.lang_code}]\n'
        return r

    def append(self, attr: str, model: Type[BaseModel]):
        for link in list(model.select()):
            getattr(self[link.book], attr).append(getattr(self.metadata, attr)[getattr(link, attr)])

