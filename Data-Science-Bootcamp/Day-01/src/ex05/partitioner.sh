#!/bin/sh
INPUT="../ex03/hh_positions.csv"
HEADER=$(head -n 1 $INPUT)

tail -n +2 $INPUT | while IFS=, read -r id created_at name has_test url
do
    DATE=$(echo $created_at | cut -d'T' -f1)
    FILE="${DATE}.csv"

    if [ ! -f "$FILE" ]; then
        echo "$HEADER" > "$FILE"
    fi

    echo "$id,$created_at,$name,$has_test,$url" >> "$FILE"
done