#!/bin/sh

# ./run.sh portnumber
# 9050 for Mac, Linux: 9150 or the tor port in use
port=$1

python riddle1.py $port