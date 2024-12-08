from peewee import TextField, IntegerField, BooleanField, FloatField, SQL

from calibre_db import BaseModel, UnknownField


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
