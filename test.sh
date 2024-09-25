#!/bin/bash

python calibre-export.py column --library /data/testCalibreLibrary --label bookshelf -o /data/export/column/bookshelf     
python calibre-export.py column --library /data/testCalibreLibrary --label read -o /data/export/column/read               
python calibre-export.py column --library /data/testCalibreLibrary --label read --value 0 -o /data/export/column/unread   
python calibre-export.py authors --library /data/testCalibreLibrary  -o /data/export/authors                       
python calibre-export.py series --library /data/testCalibreLibrary  -o /data/export/series                         
python calibre-export.py tags --library /data/testCalibreLibrary  -o /data/export/tags
