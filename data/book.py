import calibre_db

class Book(calibre_db.Books):
    def __init__(self, _from: calibre_db.Books):
        super().__init__()
        self.__dict__.update(_from.__dict__)

    def __str__(self):
        return f'{self.title}'


class Books(dict):
    def __init__(self, _from: dict):
        super().__init__()
        for k, v in _from.items():
            self[k] = Book(v)
