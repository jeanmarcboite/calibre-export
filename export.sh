#!/bin/bash
library=/home/box/Desktop/myCalibreLibrary
output=/wtf/CalibreBooks
exe=/home/box/src/python/calibre/cdb/calibre-export.py
python $exe column --library $library --label bookshelf -o $output/epub
python $exe column --library $library --label bookshelf -o $output/pdf -f pdf
python $exe column --library $library --label read -o $output/read
python $exe column --library $library --label reading -o $output/reading
python $exe column --library $library --label read -o $output/read -f pdf
python $exe column --library $library --label reading -o $output/reading -f pdf
python $exe column --library $library --label read --value 0 -o $output/unread
python $exe authors --library $library  -o $output/authors
python $exe series --library $library  -o $output/series
python $exe tags --library $library  -o $output/tags
