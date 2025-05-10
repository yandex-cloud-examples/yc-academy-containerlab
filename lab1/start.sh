#!/bin/sh
clab deploy --topo frrlab.yml
./FRR-vty-files.sh
./PC-interfaces.sh
