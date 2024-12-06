from symtable import Class
from typing import Type

from calibre_db import Authors, Books, Publishers, BaseModel, Languages


def get_table(cls: Type[BaseModel]) -> dict:
    table = {}
    for entry in cls.select():
        table[entry.id] = entry
    return table


class CalibreMetadata():
    def __init__(self):
        self.author = get_table(Authors)
        self.book = get_table(Books)
        self.publisher = get_table(Publishers)
        self.lang_code = get_table(Languages)
        print(self.lang_code)


    def __str__(self):
        return f'{{Authors: {self.author}, Books: {self.book}}}'
