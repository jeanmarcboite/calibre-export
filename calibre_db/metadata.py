from symtable import Class
from typing import Type

from calibre_db import Authors, Books, Publishers, BaseModel, Languages, Comments, ConversionOptions, Data, Feeds, \
    Identifiers, LastReadPositions, LibraryId, Ratings, Series, Tags


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
        self.comments = get_table(Comments)
        self.conversion_options = get_table(ConversionOptions)
        self.data = get_table(Data)
        self.feed = get_table(Feeds)
        self.identifiers = get_table(Identifiers)
        self.last_read_positions = get_table(LastReadPositions)
        self.library_id = get_table(LibraryId)
        self.rating = get_table(Ratings)
        self.series = get_table(Series)
        self.tag = get_table(Tags)

        print(self.lang_code)
        print(self.rating)
        print(self.tag)


    def __str__(self):
        return f'{{Authors: {self.author}, Books: {self.book}}}'
