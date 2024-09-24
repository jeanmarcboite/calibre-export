import logging
import subprocess
from os import listdir
import os.path

import fire
import sqlite3
from pathlib import Path

CALIBRE_DATABASE = "/home/box/Desktop/myCalibreLibrary"
db_con = sqlite3.connect("/home/box/Desktop/myCalibreLibrary/metadata.db")

def export_custom_column(column: str, output: str, debug: bool = False):
  logging.getLogger().setLevel(logging.DEBUG)
  cur = db_con.cursor()
  try:
    cur.execute(f'select id, label from custom_columns')
    rows = cur.fetchall()
    logging.debug(rows)
    for row in filter(lambda r: r[1] == column, rows):
        logging.debug(row)
        cur.execute(f'select id, value from custom_column_{row[0]} order by value')
        shelves = cur.fetchall()
        for shelf in shelves:
          display(shelf, output, row[0], debug)

  except Exception as e:
      logging.error(e)

  db_con.close()

def display(shelf, output, col, debug = False):
  if debug:
    print(shelf)
  print(shelf)
  Path(f'{output}/{shelf[1]}').mkdir(parents=True, exist_ok=True)
  cur = db_con.cursor()
  select = f'select book from books_custom_column_{col}_link where value == {shelf[0]}'
  cur.execute(select)
  books = cur.fetchall()
  book_list = []
  for book in books:
    select = f'select title, sort, path from books where id == {book[0]}'
    b = cur.execute(select).fetchall()[0]
    book_list.append(b)
  for book in sorted(book_list, key=lambda bk: bk[1]):
    if debug:
      print(book[0])
      print(book[2])
    ebook_dir = f'{CALIBRE_DATABASE}/{book[2]}'
    only_files = [f for f in listdir(ebook_dir) if os.path.isfile(os.path.join(ebook_dir, f))]
    for f in [s for s in only_files if s.endswith(".epub")]:
        print(f'epub: {CALIBRE_DATABASE}/{f}')
        # subprocess.call(["rsync", f'{ebook_dir}/{f}', f'{output}/{shelf[1]}'])
def main():
  fire.Fire({
    'export' : export_custom_column,
  })

if __name__ == '__main__':
  main()