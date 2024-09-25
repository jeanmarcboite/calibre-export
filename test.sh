#!/bin/bash
library=/data/testCalibreLibrary
python calibre-export.py column --library $library --label bookshelf -o /data/export/column/bookshelf
python calibre-export.py column --library $library --label read -o /data/export/column/read
python calibre-export.py column --library $library --label read --value 0 -o /data/export/column/unread
python calibre-export.py authors --library $library  -o /data/export/authors
python calibre-export.py series --library $library  -o /data/export/series
python calibre-export.py tags --library $library  -o /data/export/tags
