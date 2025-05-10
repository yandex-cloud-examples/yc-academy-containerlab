#!/bin/sh
sudo docker exec clab-static-routing-PC1 ip link set eth1 up
sudo docker exec clab-static-routing-PC1 ip addr add 192.168.0.2/24 dev eth1
sudo docker exec clab-static-routing-PC1 ip route add 0.0.0.0/0 via 192.168.0.1 dev eth1

sudo docker exec clab-static-routing-PC2 ip link set eth1 up
sudo docker exec clab-static-routing-PC2 ip addr add 10.0.2.2/24 dev eth1
sudo docker exec clab-static-routing-PC2 ip route add 0.0.0.0/0 via 10.0.2.1 dev eth1


sudo docker exec clab-static-routing-PC3 ip link set eth1 up
sudo docker exec clab-static-routing-PC3 ip addr add 10.0.3.2/24 dev eth1
sudo docker exec clab-static-routing-PC3 ip route add 0.0.0.0/0 via 10.0.3.1 dev eth1

sudo docker exec clab-static-routing-PC4 ip link set eth1 up
sudo docker exec clab-static-routing-PC4 ip addr add 10.0.4.2/24 dev eth1
sudo docker exec clab-static-routing-PC4 ip route add 0.0.0.0/0 via 10.0.4.1 dev eth1