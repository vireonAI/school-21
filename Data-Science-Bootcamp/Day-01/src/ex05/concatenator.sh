#!/bin/sh
OUTPUT=hh_concat.csv
FIRST_FILE=$(ls *.csv | head -n 1)
head  -n 1 $FIRST_FILE > $OUTPUT
for FILE in *.csv
do
    tail -n +2 $FILE >> $OUTPUT
done