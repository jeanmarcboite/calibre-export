from typing import Type

import calibre_db
from calibre_db import BaseModel
from calibre_db.links import *
from calibre_db.metadata import CalibreMetadata


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
        return f'{self.title}, {self.author}, {self.publisher}, {self.lang_code}, {self.rating}, {self.series}, {self.tag}'


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

    def __str__(self):
        r = '\n'
        for book in self.values():
            r += f'{book}\n'
        return r

    def append(self, attr: str, model: Type[BaseModel]):
        for link in list(model.select()):
            # print(f' {attr} link {link} {link.book} {self[link.book]} link.{attr}={getattr(link, attr)} {getattr(self.metadata, attr)[getattr(link, attr)]}')
            getattr(self[link.book], attr).append(getattr(self.metadata, attr)[getattr(link, attr)])

