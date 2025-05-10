sudo docker exec clab-bgp-PC1 ip addr add 31.31.20.1/24 dev eth1
sudo docker exec clab-bgp-PC1 ip route del default
sudo docker exec clab-bgp-PC1 ip route add default via 31.31.20.254
