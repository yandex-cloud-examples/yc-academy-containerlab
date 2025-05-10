#!/bin/sh
clab deploy --topo vpn.yml
docker exec clab-vpn-router1 sh -c "swanctl --load-all"
docker exec clab-vpn-router3 sh -c "swanctl --load-all"
