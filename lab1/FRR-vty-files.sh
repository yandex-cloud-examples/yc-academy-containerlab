#!/bin/sh
sudo docker exec clab-frrlab-router1 /bin/sh -c "touch /etc/frr/vtysh.conf"
sudo docker exec clab-frrlab-router2 /bin/sh -c "touch /etc/frr/vtysh.conf"
sudo docker exec clab-frrlab-router3 /bin/sh -c "touch /etc/frr/vtysh.conf"