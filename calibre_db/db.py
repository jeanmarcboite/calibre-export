from peewee import *

sqlite_db = SqliteDatabase(None)
class UnknownField(object):
    def __init__(self, *_, **__): pass

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = sqlite_db
class Authors(BaseModel):
    link = TextField(constraints=[SQL("DEFAULT ''")])
    name = TextField(unique=True)
    sort = TextField(null=True)

    class Meta:
        table_name = 'authors'

    def __str__(self):
        return self.name

class Books(BaseModel):
    author_sort = TextField(index=True, null=True)
    flags = IntegerField(constraints=[SQL("DEFAULT 1")])
    has_cover = BooleanField(constraints=[SQL("DEFAULT 0")], null=True)
    isbn = TextField(constraints=[SQL("DEFAULT ''")], null=True)
    last_modified = UnknownField(constraints=[SQL("DEFAULT '2000-01-01 00:00:00+00:00'")])  # TIMESTAMP
    lccn = TextField(constraints=[SQL("DEFAULT ''")], null=True)
    path = TextField(constraints=[SQL("DEFAULT ''")])
    pubdate = UnknownField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)  # TIMESTAMP
    series_index = FloatField(constraints=[SQL("DEFAULT 1.0")])
    sort = TextField(index=True, null=True)
    timestamp = UnknownField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)  # TIMESTAMP
    title = TextField(constraints=[SQL("DEFAULT 'Unknown'")])
    uuid = TextField(null=True)

    class Meta:
        table_name = 'books'

    def __str__(self):
        return self.title

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

