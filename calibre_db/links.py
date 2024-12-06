from peewee import IntegerField, TextField, SQL

from calibre_db import BaseModel


class BooksAuthorsLink(BaseModel):
    author = IntegerField(index=True)
    book = IntegerField(index=True)

    class Meta:
        table_name = 'books_authors_link'
        indexes = (
            (('book', 'author'), True),
        )
    def __str__(self):
        return f'{self.book} {self.author}'


class BooksLanguagesLink(BaseModel):
    book = IntegerField(index=True)
    item_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    lang_code = IntegerField(index=True)

    class Meta:
        table_name = 'books_languages_link'
        indexes = (
            (('book', 'lang_code'), True),
        )


class BooksPluginData(BaseModel):
    book = IntegerField()
    name = TextField()
    val = TextField()

    class Meta:
        table_name = 'books_plugin_data'
        indexes = (
            (('book', 'name'), True),
        )


class BooksPublishersLink(BaseModel):
    book = IntegerField(unique=True)
    publisher = IntegerField(index=True)

    class Meta:
        table_name = 'books_publishers_link'


class BooksRatingsLink(BaseModel):
    book = IntegerField(index=True)
    rating = IntegerField(index=True)

    class Meta:
        table_name = 'books_ratings_link'
        indexes = (
            (('book', 'rating'), True),
        )


class BooksSeriesLink(BaseModel):
    book = IntegerField(unique=True)
    series = IntegerField(index=True)

    class Meta:
        table_name = 'books_series_link'


class BooksTagsLink(BaseModel):
    book = IntegerField(index=True)
    tag = IntegerField(index=True)

    class Meta:
        table_name = 'books_tags_link'
        indexes = (
            (('book', 'tag'), True),
        )


