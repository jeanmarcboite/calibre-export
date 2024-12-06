import calibre_db

class Book(calibre_db.Books):
    def __init__(self, _from: calibre_db.Books):
        super().__init__()
        self.__dict__.update(_from.__dict__)
        self.authors = list()

    def __str__(self):
        return f'{self.title}, {self.authors}'


class Books(dict):
    def __init__(self, _from: dict, authors: dict, books_authors_link: list):
        super().__init__()
        for k, v in _from.items():
            self[k] = Book(v)
        for link in books_authors_link:
            self[link.book].authors.append(authors[link.author])
