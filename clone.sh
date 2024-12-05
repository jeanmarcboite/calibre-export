#!/bin/bash
for t in epub pdf
do
 rclone copy /wtf/CalibreBooks/$t doogee:storage/documents/CalibreBooks/$t
done