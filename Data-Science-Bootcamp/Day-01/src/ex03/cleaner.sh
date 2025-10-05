#!/bin/sh
hh_sorted="../ex02/hh_sorted.csv"
head -n 1 $hh_sorted > hh_positions.csv
tail -n +2 $hh_sorted |\
sed -E 's/^("([^"]*)","[^"]*","[^"]*),([^"]*")/\1;\3/' |\
awk -F, 'BEGIN {OFS=","} {
    
    name=$3
    newname="-"
    if(name ~ /Junior/&& name ~/Middle/){
        newname="Junior/Middle"
    }else if(name ~ /Middle/&& name ~/Senior/){
        newname="Middle/Senior"
    }else if(name ~ /Junior/&& name ~/Senior/){
        newname="Junior/Senior"
    }else if(name ~ /Junior/){
        newname="Junior"
    }else if(name ~ /Middle/){
        newname="Middle"
    }else if(name ~ /Senior/){
        newname="Senior"
    }
    $3="\""newname"\""
    print $0
}' >> hh_positions.csv