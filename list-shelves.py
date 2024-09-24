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

def export_custom_column(column: str, output: str, debug: bool = False):
    if debug:
        logger.setLevel(logging.DEBUG)
    try:
        rows = fetchall(f'select id, label from custom_columns where label == \"{column}\"')
        for row in rows:
            values = fetchall(f'select value, id from custom_column_{row[0]} order by value')
            for value in values:
                export(value[0], value[1], output, row[0], debug)

    except sqlite3.OperationalError as e:
        logger.error(f'{type(e)}: {e}')

    db_con.close()


def export(shelf, shelf_id, output, col, debug=False):
    output_directory = f'{output}/{shelf}'
    logger.warning(f'Create directory {output_directory}')
    Path(output_directory).mkdir(parents=True, exist_ok=True)
    books = fetchall(f'select book from books_custom_column_{col}_link where value == {shelf_id}')
    book_list = []
    for book in books:
        b = fetchall(f'select title, sort, path from books where id == {book[0]}')
        book_list.append(b[0])
    logger.debug(f'books: {book_list}')
    for book in sorted(book_list, key=lambda bk: bk[1]):
        ebook_dir = f'{CALIBRE_DATABASE}/{book[2]}'
        only_files = [f for f in listdir(ebook_dir) if os.path.isfile(os.path.join(ebook_dir, f))]
        for f in [s for s in only_files if s.endswith(".epub")]:
            from_file = f'{ebook_dir}/{f}'
            to_file = f'{output}/{shelf}/{f}'
            # subprocess.call(["rsync", f'{ebook_dir}/{f}', f'{output}/{shelf}'])
            # distutils.file_util.copy_file(src, dst[, preserve_mode=1, preserve_times=1, update=0, link=None, verbose=0, dry_run=0])
            logger.debug(f"cmp {from_file} {to_file}: {filecmp.cmp(from_file, to_file, shallow=True)}")
            if not filecmp.cmp(from_file, to_file, shallow=True):
                logger.debug(f'cp {from_file} {to_file}')
                shutil.copy2(from_file, to_file)

def main():
    fire.Fire({
        'export': export_custom_column,
    })


if __name__ == '__main__':
    set_logger()
    main()
