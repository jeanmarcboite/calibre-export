import os

from calibre_db.base_model import sqlite_db


class AppContext(object):
    def __init__(self, library=None, output=None, debug=False):
        self.calibre_library = os.path.abspath(library or '.')
        self.output = os.path.abspath(output or '.')
        self.debug = debug
        database = os.path.join(self.calibre_library, 'metadata.db')
        # Check if db already exists or not
        if not os.path.exists(database):
            raise ValueError(f'DB {database} does not exist')
        sqlite_db.init(database)

