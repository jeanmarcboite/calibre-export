from peewee import *

from calibre_db.base_model import BaseModel, UnknownField


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


class Comments(BaseModel):
    book = IntegerField(unique=True)
    text = TextField()

    class Meta:
        table_name = 'comments'

class ConversionOptions(BaseModel):
    book = IntegerField(index=True, null=True)
    data = BlobField()
    format = TextField(index=True)

    class Meta:
        table_name = 'conversion_options'
        indexes = (
            (('format', 'book'), True),
        )

class Data(BaseModel):
    book = IntegerField(index=True)
    format = TextField(index=True)
    name = TextField()
    uncompressed_size = IntegerField()

    class Meta:
        table_name = 'data'
        indexes = (
            (('book', 'format'), True),
        )

class Feeds(BaseModel):
    script = TextField()
    title = TextField(unique=True)

    class Meta:
        table_name = 'feeds'

class Identifiers(BaseModel):
    book = IntegerField()
    type = TextField(constraints=[SQL("DEFAULT 'isbn'")])
    val = TextField()

    class Meta:
        table_name = 'identifiers'
        indexes = (
            (('book', 'type'), True),
        )

class Languages(BaseModel):
    lang_code = TextField(unique=True)
    link = TextField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'languages'

class LastReadPositions(BaseModel):
    book = IntegerField(index=True)
    cfi = TextField()
    device = TextField()
    epoch = FloatField()
    format = TextField()
    pos_frac = FloatField(constraints=[SQL("DEFAULT 0")])
    user = TextField()

    class Meta:
        table_name = 'last_read_positions'
        indexes = (
            (('user', 'device', 'book', 'format'), True),
        )

class LibraryId(BaseModel):
    uuid = TextField(unique=True)

    class Meta:
        table_name = 'library_id'

class MetadataDirtied(BaseModel):
    book = IntegerField(unique=True)

    class Meta:
        table_name = 'metadata_dirtied'

class Publishers(BaseModel):
    link = TextField(constraints=[SQL("DEFAULT ''")])
    name = TextField(unique=True)
    sort = TextField(null=True)

    class Meta:
        table_name = 'publishers'

class Ratings(BaseModel):
    link = TextField(constraints=[SQL("DEFAULT ''")])
    rating = IntegerField(null=True, unique=True)

    class Meta:
        table_name = 'ratings'

class Series(BaseModel):
    link = TextField(constraints=[SQL("DEFAULT ''")])
    name = TextField(unique=True)
    sort = TextField(null=True)

    class Meta:
        table_name = 'series'

class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False

class Tags(BaseModel):
    link = TextField(constraints=[SQL("DEFAULT ''")])
    name = TextField(index=True)

    class Meta:
        table_name = 'tags'

