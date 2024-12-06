from typing import Type

import calibre_db
from calibre_db import BaseModel
from calibre_db.links import BooksAuthorsLink, BooksLanguagesLink, BooksPublishersLink
from calibre_db.metadata import CalibreMetadata


class Book(calibre_db.Books):
    def __init__(self, _from: calibre_db.Books):
        super().__init__()
        self.__dict__.update(_from.__dict__)
        self.authors = []
        self.comments = []
        self.languages = []
        self.publishers = []

    def __str__(self):
        return f'{self.title}, {self.authors}, {self.publishers}'


class Books(dict):
    def __init__(self, metadata: CalibreMetadata):
        super().__init__()
        self.metadata = metadata
        for k, v in self.metadata.book.items():
            self[k] = Book(v)
        self.append('author', BooksAuthorsLink)
        self.append('publisher', BooksPublishersLink)

    def append(self, attr: str, model: Type[BaseModel]):
        for link in list(model.select()):
            self[link.book].authors.append(getattr(self.metadata, attr)[getattr(link, attr)])

