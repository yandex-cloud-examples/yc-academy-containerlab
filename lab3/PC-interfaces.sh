#!/bin/sh
sudo docker exec clab-switching-pc1 ip addr add 192.168.1.254/24 dev eth1
sudo docker exec clab-switching-pc2 ip addr add 192.168.2.254/24 dev eth1
sudo docker exec clab-switching-pc3 ip addr add 192.168.1.253/24 dev eth1
sudo docker exec clab-switching-pc4 ip addr add 192.168.2.253/24 dev eth1
