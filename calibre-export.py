import filecmp
import logging
import os
import shutil
import sqlite3
import pathlib

import fire
logger = logging.getLogger(__name__)

class Export(object):
    def __init__(self, database: str, output: str, debug: bool = False):
        self.database = database
        self.output = output
        self.debug = debug

    def authors(self):
        return self.__copy_books("authors", "sort")
    def tags(self):
        # no sort field in tags table
        return self.__copy_books("tags")
    def series(self):
        return self.__copy_books("series", "sort")
    def column(self, label: str, value = 1):
        return export_custom_column(self.database, label, self.output, value, self.debug)


    def __copy_books(self, table: str, attribute = "name"):
        if self.debug:
            logger.setLevel(logging.DEBUG)
        try:
            db_con = sqlite3.connect(f'{self.database}/metadata.db')
            items = {}
            for item in fetchall(db_con, f'select id, name, {attribute} from {table}'):
                # item[author_id] = item[author_sort]
                items[item[0]] = [item[1], item[2]]
            logger.debug(items)

            for book in fetchall(db_con, f'select * from books_{table}_link'):
                item = items[book[2]]
                if len(item[1].split()) <= 5:
                    output_subdirectory = f'{self.output}/{item[1]}'
                    b = fetchall(db_con, f'select title, sort, path from books where id == {book[1]}')[0]
                    copy_files(f'{self.database}/{b[2]}', output_subdirectory)
        except sqlite3.OperationalError as e:
            logger.error(f'{type(e)}: {e}')

def export_custom_column(database: str, label: str, output: str, value = 1, debug: bool = False):
    if debug:
        logger.setLevel(logging.DEBUG)
    try:
        db_con = sqlite3.connect(f'{database}/metadata.db')
        row = db_con.cursor().execute(f'select id, datatype from custom_columns where label == \"{label}\"').fetchone()
        if row is None:
            logger.error(f'no such column: {label}')
        elif row[1] == 'bool':
            for book in fetchall(db_con, f'select book from custom_column_{row[0]} where value == {value}'):
                copy_book(db_con, database, book[0], output)
        else:
            values = fetchall(db_con, f'select value, id from custom_column_{row[0]} order by value')
            for value in values:
                copy_shelf(db_con, database, value[0], value[1], output, row[0], debug)
    except sqlite3.OperationalError as e:
        logger.error(f'{type(e)}: {e}')

def copy_book(db_con: sqlite3.Connection, database: str, book_id, output):
    book = db_con.cursor().execute(f'select path from books where id == {book_id}').fetchone()
    if book is None:
        logger.error(f'no book with id: {book_id}')
    else:
        copy_files(f'{database}/{book[0]}', output)

def copy_shelf(db_con: sqlite3.Connection, database: str, shelf, shelf_id, output, col, debug=False):
    output_directory = f'{output}/{shelf}'
    logger.warning(f'Create directory {output_directory}')
    books = fetchall(db_con, f'select book from books_custom_column_{col}_link where value == {shelf_id}')
    book_list = []
    for book in books:
        b = fetchall(db_con, f'select title, sort, path from books where id == {book[0]}')
        book_list.append(b[0])
    logger.debug(f'books: {book_list}')
    for book in sorted(book_list, key=lambda bk: bk[1]):
        copy_files(f'{database}/{book[2]}', output_directory)



def copy_files(input_directory, output_directory):
    only_files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
    for f in [s for s in only_files if s.endswith(".epub")]:
        copy_file(f, input_directory, output_directory)
def copy_file(filename, input_directory, output_directory):
    pathlib.Path(output_directory).mkdir(parents=True, exist_ok=True)
    from_file = f'{input_directory}/{filename}'
    to_file = f'{output_directory}/{filename}'
    try:
        logger.debug(f"cmp {from_file} {to_file}: {filecmp.cmp(from_file, to_file, shallow=True)}")
        if not filecmp.cmp(from_file, to_file, shallow=True):
            logger.info(f'[update] cp {from_file} {to_file}')
            shutil.copy2(from_file, to_file)
    except FileNotFoundError:
        logger.debug(f'cp {from_file} {to_file}')
        shutil.copy2(from_file, to_file)


def set_logger():
    logger.setLevel(logging.ERROR)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)

def fetchall(db_con: sqlite3.Connection, command: str):
    cursor = db_con.cursor()
    rows = cursor.execute(command).fetchall()
    logger.debug(f'{command}: {rows}')

    return rows


if __name__ == '__main__':
    set_logger()
    #fire.Fire(dict(authors=export_authors, series=export_series, tags=export_tags, column=export_custom_column))
    fire.Fire(Export)