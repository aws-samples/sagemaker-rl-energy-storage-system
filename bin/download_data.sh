#!/usr/bin/env bash

DIR=${1:-data/price_demand_data}
mkdir -p ${DIR}

YEAR="2020"
for i in {01..13};do
    link="https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_${YEAR}${i}_NSW1.csv"
    wget ${link} -P ${DIR}
done
