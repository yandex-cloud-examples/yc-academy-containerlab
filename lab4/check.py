import os

def cmd_out(cmd):
    stream = os.popen(cmd)
    output = stream.read().strip()
    return output

def gre_check(iface, r_scope):
    for item in r_scope:
        r_out = cmd_out(f"docker exec {item} sh -c 'ifconfig {iface}'")
        if 'RUNNING' in r_out:
            print(f"Iface {iface} was found in runtime configuration on {item}")
            pass
        else:
            raise Exception (f"Iface {iface} was NOT found in runtime configuration on {item}")
    return True

def icmp_check():
    for ip in ["192.168.2.1", "192.168.3.1"]:
        host_output = cmd_out(f"docker exec clab-vpn-srv1 sh -c 'ping -qc4 {ip} | grep loss | cut -d, -f3'")
        loss = int(host_output.split('%')[0])
        if loss <= 25:
            print(f"{ip} succesfully response with %{loss} losses")
            pass
        elif loss == 100:
            raise Exception (f"Host {ip} doesn't reacheable by icmp")
        else:
            raise Exception (f"Too many losses,%{loss} something goes wrong")
    return True

def ipsec_check():
    try:
        swanctl_output = cmd_out("docker exec clab-vpn-router1 sh -c 'swanctl --stats | grep IKE_SAs'")
    except:
        raise Exception ("Failed get data. Probably strongswan daemon not running")
    if "1 total" in swanctl_output:
        print(f"IPSec IKE and SA successfully formed\n{swanctl_output}\n")
        pass
    else:
        raise Exception (f"\nIPSec connection or SA association not formed properly")
    return True

print("\nGRE interface check\n===================")
gre_check("gre1",["clab-vpn-router1", "clab-vpn-router2"])
gre_check("gre2",["clab-vpn-router1", "clab-vpn-router3"])
print("\nICMP check\n===================")
icmp_check()
print("\nIPSec check\n===================")
ipsec_check()
