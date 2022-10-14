#!/bin/bash

# to get up to 31 in hex with xxd
# then with dd remove the wrong bytes
dd if=sss491020.tar.gz of=sss.tar.gz ibs=31 skip=1