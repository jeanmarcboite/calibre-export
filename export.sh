#!/bin/bash
library=/home/box/Desktop/myCalibreLibrary
output=/wtf/CalibreBooks
python calibre-export.py column --library $library --label bookshelf -o $output/epub
python calibre-export.py column --library $library --label bookshelf -o $output/pdf -f pdf
python calibre-export.py column --library $library --label read -o $output/read
python calibre-export.py column --library $library --label reading -o $output/reading
python calibre-export.py column --library $library --label read -o $output/read -f pdf
python calibre-export.py column --library $library --label reading -o $output/reading -f pdf
python calibre-export.py column --library $library --label read --value 0 -o $output/unread
python calibre-export.py authors --library $library  -o $output/authors
python calibre-export.py series --library $library  -o $output/series
python calibre-export.py tags --library $library  -o $output/tags
