#!/usr/bin/env bash

mkdir -p data

YEAR="2020"
for i in {01..13};do
    link="https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_${YEAR}${i}_NSW1.csv"
    wget ${link} -P ./data
done


