#!/bin/sh
sudo docker exec clab-static-routing-router1 /bin/sh -c "touch /etc/frr/vtysh.conf"
sudo docker exec clab-static-routing-router2 /bin/sh -c "touch /etc/frr/vtysh.conf"
sudo docker exec clab-static-routing-router3 /bin/sh -c "touch /etc/frr/vtysh.conf"
sudo docker exec clab-static-routing-router4 /bin/sh -c "touch /etc/frr/vtysh.conf"
sudo docker exec clab-static-routing-router-core /bin/sh -c "touch /etc/frr/vtysh.conf"