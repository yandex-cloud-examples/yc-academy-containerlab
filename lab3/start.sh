sudo apt-get install openvswitch-switch
sudo ovs-vsctl add-br ovs-bridge1
sudo ovs-vsctl add-br ovs-bridge2
sudo ovs-vsctl add-br ovs-bridge3
sudo ovs-vsctl add-br ovs-bridge4
sudo ovs-vsctl set bridge ovs-bridge1 rstp_enable=true
sudo ovs-vsctl set bridge ovs-bridge2 rstp_enable=true
sudo ovs-vsctl set bridge ovs-bridge3 rstp_enable=true
sudo ovs-vsctl set bridge ovs-bridge4 rstp_enable=true
sudo clab deploy --topo switching.yml
sudo ./PC-interfaces.sh
