#!/bin/sh
filename="../ex03/hh_positions.csv" 
echo '"name","count"' > hh_uniq_positions.csv

tail -n +2 $filename | \
cut -d, -f3 | \
grep -v '"-"' | \
sort | \
uniq -c | \
sort -nr | \
awk '{print $2 "," $1}'  >> hh_uniq_positions.csv