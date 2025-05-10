#!/bin/sh
clab deploy --topo static-routing.yml
./FRR-vty-files.sh
./PC-interfaces.sh
