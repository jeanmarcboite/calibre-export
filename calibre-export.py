import filecmp
import logging
import os
import shutil
import sqlite3
import pathlib

import fire
logger = logging.getLogger(__name__)

class Export(object):
    def __init__(self, library: str, output: str, fmt: str = "epub", debug: bool = False):
        self.db_con = None
        self.library = library
        self.output = output
        self.fmt = fmt
        self.debug = debug
        if self.debug:
            logger.setLevel(logging.DEBUG)

        self.db_con = sqlite3.connect(f'{self.library}/metadata.db')

    def authors(self):
        return self.__copy_table_books("authors", "sort")
    def tags(self):
        # no sort field in tags table
        return self.__copy_table_books("tags")
    def series(self):
        return self.__copy_table_books("series", "sort")
    def column(self, label: str, value = 1):
        return self.__copy_custom_column_books(label, value)


    def __copy_table_books(self, table: str, attribute = "name"):
        try:
            items = {}
            for item in self.__fetchall(f'select id, name, {attribute} from {table}'):
                # item[author_id] = item[author_sort]
                items[item[0]] = [item[1], item[2]]
            logger.debug(items)

            for book in self.__fetchall(f'select * from books_{table}_link'):
                item = items[book[2]]
                if len(item[1].split()) <= 5:
                    output_subdirectory = f'{self.output}/{item[1]}'
                    b = self.__fetchall(f'select title, sort, path from books where id == {book[1]}')[0]
                    copy_files(f'{self.library}/{b[2]}', output_subdirectory, self.fmt)
        except sqlite3.OperationalError as e:
            logger.error(f'{type(e)}: {e}')

    def __copy_custom_column_books(self, label: str, value: int):
        try:
            row = self.__fetchone(f'select id, datatype from custom_columns where label == \"{label}\"')
            if row is None:
                logger.error(f'no such column: {label}')
            elif row[1] == 'bool':
                for book in self.__fetchall(f'select book from custom_column_{row[0]} where value == {value}'):
                    self.__copy_book(book[0])
            else:
                values = self.__fetchall(f'select value, id from custom_column_{row[0]} order by value')
                for value in values:
                    self.__copy_shelf(value[0], value[1], row[0])
        except sqlite3.OperationalError as e:
            logger.error(f'{type(e)}: {e}')

    def __copy_book(self, book_id):
        book = self.__fetchone(f'select path from books where id == {book_id}')
        if book is None:
            logger.error(f'no book with id: {book_id}')
        else:
            copy_files(f'{self.library}/{book[0]}', self.output, self.fmt)

    def __copy_shelf(self, shelf, shelf_id, col):
        output_directory = f'{self.output}/{shelf}'
        logger.warning(f'Create directory {output_directory}')
        books = self.__fetchall(f'select book from books_custom_column_{col}_link where value == {shelf_id}')
        book_list = []
        for book in books:
            b = self.__fetchall(f'select title, sort, path from books where id == {book[0]}')
            book_list.append(b[0])
        logger.debug(f'books: {book_list}')
        for book in sorted(book_list, key=lambda bk: bk[1]):
            copy_files(f'{self.library}/{book[2]}', output_directory, self.fmt)

    def __fetchall(self, command: str):
        rows = self.db_con.cursor().execute(command).fetchall()
        logger.debug(f'{command}: {rows}')

        return rows

    def __fetchone(self, command: str):
        return self.db_con.cursor().execute(command).fetchone()


def copy_files(input_directory: str, output_directory: str, fmt: str):
    only_files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
    for f in [s for s in only_files if s.endswith(f'.{fmt}')]:
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



if __name__ == '__main__':
    set_logger()
    #fire.Fire(dict(authors=export_authors, series=export_series, tags=export_tags, column=export_custom_column))
    fire.Fire(Export)