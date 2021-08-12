#!/bin/bash

if [[ $# -ne 2 ]]; then
   START="import"
   STOP="export"
else
   START=$1
   STOP=$2
fi

sc examples/gcd/gcd.v \
   -target "skywater130_asicflow" \
   -constraint "examples/gcd/gcd.sdc" \
   -asic_floorplan "examples/gcd/floorplan.py" \
   -loglevel "INFO" \
   -quiet \
   -relax \
   -start $START \
   -stop $STOP \
   -design gcd  
