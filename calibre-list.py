import filecmp
import logging
import shutil
import subprocess
from os import listdir
import os.path

import fire
import sqlite3
from pathlib import Path

CALIBRE_DATABASE = "/home/box/Desktop/myCalibreLibrary"
db_con = sqlite3.connect("/home/box/Desktop/myCalibreLibrary/metadata.db")
logger = logging.getLogger(__name__)

def set_logger():
    logger.setLevel(logging.ERROR)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)
    # 'application' code
    logger.debug('debug message')

def fetchall(command):
    cursor = db_con.cursor()
    rows = cursor.execute(command).fetchall()
    logger.debug(f'{command}: {rows}')

    return rows

def export_authors(output: str, debug: bool = False):
    if debug:
        logger.setLevel(logging.DEBUG)
    try:
        authors = {}
        authors_list = fetchall(f'select id, name, sort from authors')
        for author in authors_list:
            authors[author[0]] = [author[1], author[2]]
        logger.debug(authors)
        books = fetchall(f'select book, author from books_authors_link')
        for book in books:
            author = authors[book[1]]
            output_directory = f'{output}/{author[1]}'
            b = fetchall(f'select title, sort, path from books where id == {book[0]}')[0]

            copy_files(f'{CALIBRE_DATABASE}/{b[2]}', output_directory)
    except sqlite3.OperationalError as e:
        logger.error(f'{type(e)}: {e}')

    db_con.close()

def export_custom_column(column: str, output: str, debug: bool = False):
    if debug:
        logger.setLevel(logging.DEBUG)
    try:
        rows = fetchall(f'select id from custom_columns where label == \"{column}\"')
        for row in rows:
            values = fetchall(f'select value, id from custom_column_{row[0]} order by value')
            for value in values:
                export_shelf(value[0], value[1], output, row[0], debug)

    except sqlite3.OperationalError as e:
        logger.error(f'{type(e)}: {e}')

def copy_files(input_directory, output_directory):
    only_files = [f for f in listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
    for f in [s for s in only_files if s.endswith(".epub")]:
        copy_file(f, input_directory, output_directory)

def copy_file(filename, input_directory, output_directory):
    Path(output_directory).mkdir(parents=True, exist_ok=True)
    from_file = f'{input_directory}/{filename}'
    to_file = f'{output_directory}/{filename}'
    # subprocess.call(["rsync", f'{ebook_dir}/{f}', f'{output}/{shelf}'])
    # distutils.file_util.copy_file(src, dst[, preserve_mode=1, preserve_times=1, update=0, link=None, verbose=0, dry_run=0])
    # logger.debug(f"cmp {from_file} {to_file}: {filecmp.cmp(from_file, to_file, shallow=True)}")
    try:
        if not filecmp.cmp(from_file, to_file, shallow=True):
            logger.info(f'[update] cp {from_file} {to_file}')
            shutil.copy2(from_file, to_file)
    except FileNotFoundError:
        logger.debug(f'cp {from_file} {to_file}')
        shutil.copy2(from_file, to_file)


def export_shelf(shelf, shelf_id, output, col, debug=False):
    output_directory = f'{output}/{shelf}'
    logger.warning(f'Create directory {output_directory}')
    books = fetchall(f'select book from books_custom_column_{col}_link where value == {shelf_id}')
    book_list = []
    for book in books:
        b = fetchall(f'select title, sort, path from books where id == {book[0]}')
        book_list.append(b[0])
    logger.debug(f'books: {book_list}')
    for book in sorted(book_list, key=lambda bk: bk[1]):
        copy_files(f'{CALIBRE_DATABASE}/{book[2]}', output_directory)

def main():
    fire.Fire({
        'export': export_custom_column,
        'authors': export_authors,
    })

    db_con.close()


if __name__ == '__main__':
    set_logger()
    main()
