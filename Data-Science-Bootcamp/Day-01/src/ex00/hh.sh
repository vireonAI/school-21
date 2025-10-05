#!/bin/sh

VACANCY=$1

QUERY=$(echo "$VACANCY" | sed 's/ /+/g')

curl "https://api.hh.ru/vacancies?text=$QUERY&per_page=20" | jq . > hh.json
