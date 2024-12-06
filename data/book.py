import calibre_db
from calibre_db.links import BooksAuthorsLink, BooksLanguagesLink, BooksPublishersLink
from calibre_db.metadata import get_publishers, CalibreMetadata


class Book(calibre_db.Books):
    def __init__(self, _from: calibre_db.Books):
        super().__init__()
        self.__dict__.update(_from.__dict__)
        self.authors = list()
        self.comments = list()
        self.languages = list()
        self.publishers = []

    def __str__(self):
        return f'{self.title}, {self.authors}, {self.publishers}'


class Books(dict):
    def __init__(self, metadata: CalibreMetadata):
        super().__init__()
        for k, v in metadata.books.items():
            self[k] = Book(v)
        for link in list(BooksAuthorsLink.select()):
            self[link.book].authors.append(metadata.authors[link.author])

        for link in list(BooksPublishersLink.select()):
            self[link.book].publishers.append(metadata.publishers[link.publisher])
