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

class CustomColumns(BaseModel):
    datatype = TextField()
    display = TextField(constraints=[SQL("DEFAULT '{}'")])
    editable = BooleanField(constraints=[SQL("DEFAULT 1")])
    is_multiple = BooleanField(constraints=[SQL("DEFAULT 0")])
    label = TextField(unique=True)
    mark_for_delete = BooleanField(constraints=[SQL("DEFAULT 0")])
    name = TextField()
    normalized = BooleanField()

    class Meta:
        table_name = 'custom_columns'

    def __str__(self):
        return " ,".join(map(str, self.pretty_row()))
    def pretty_row(self):
        return [self.label, self.name, self.datatype, self.mark_for_delete, self.editable, self.display, self.is_multiple, self.normalized]
    @staticmethod
    def pretty_header():
        return ["Label", "Name", "Datatype", "del", "edit", "display", "mult", "norm"]
    @staticmethod
    def cols_width():
        return [20, 20, 10, 5, 5, 40, 5, 5]

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
    def __str__(self):
        return self.lang_code

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
    def __str__(self):
        return self.name

class Ratings(BaseModel):
    link = TextField(constraints=[SQL("DEFAULT ''")])
    rating = IntegerField(null=True, unique=True)

    class Meta:
        table_name = 'ratings'

    def __str__(self):
        return str(self.rating)

class Series(BaseModel):
    link = TextField(constraints=[SQL("DEFAULT ''")])
    name = TextField(unique=True)
    sort = TextField(null=True)

    class Meta:
        table_name = 'series'
    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name

