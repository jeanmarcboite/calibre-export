import calibre_db
from calibre_db.links import BooksAuthorsLink


class Book(calibre_db.Books):
    def __init__(self, _from: calibre_db.Books):
        super().__init__()
        self.__dict__.update(_from.__dict__)
        self.authors = list()

    def __str__(self):
        return f'{self.title}, {self.authors}'


class Books(dict):
    def __init__(self, _from: dict, authors: dict):
        super().__init__()
        for k, v in _from.items():
            self[k] = Book(v)
        for link in list(BooksAuthorsLink.select()):
            self[link.book].authors.append(authors[link.author])
