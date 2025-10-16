#!/usr/bin/env python3
from scapy.all import ARP, Ether, srp, conf
import sys

def arp_scan(network_cidr: str, iface=None, timeout=2):
    conf.verb = 0
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network_cidr)
    ans, _ = srp(pkt, timeout=timeout, iface=iface)
    results = []
    for sent, received in ans:
        ip = received.psrc
        mac = received.hwsrc
        results.append((ip, mac))
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: sudo python scanner_arp.py 192.168.1.0/24 [iface]")
        return
    network = sys.argv[1]
    iface = sys.argv[2] if len(sys.argv) >= 3 else None
    print(f"ARP scan {network} (iface={iface}) ...")
    res = arp_scan(network, iface=iface)
    if not res:
        print("Aucun hôte trouvé.")
        return
    print("IP\t\tMAC")
    for ip, mac in sorted(res):
        print(f"{ip}\t{mac}")

if __name__ == "__main__":
    main()
