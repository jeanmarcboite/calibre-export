from peewee import SqliteDatabase, Model

sqlite_db = SqliteDatabase(None)

class UnknownField(object):
    def __init__(self, *_, **__): pass

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = sqlite_db
