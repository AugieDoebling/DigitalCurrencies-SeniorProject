#!/bin/bash

cd ~/DigitalCurrencies-SeniorProject/LiveApplication/

d=$(date +%Y-%m-%d)

python application.py &> "runlogs/$d.log"
