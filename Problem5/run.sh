#!/bin/sh


# ./run.sh portnumber filename
# 9050 for Mac, 9150 for Linux
port=$1

# for the file ie cat. /secet/x h' /secet/y 
file=$2

python riddle1.py $port $file