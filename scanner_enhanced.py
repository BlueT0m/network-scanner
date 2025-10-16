#!/usr/bin/env python3
"""
scanner_enhanced.py
Usage:
  python scanner_enhanced.py <network_cidr> [--csv file] [--json file] [--iface IFACE]
Example:
  python scanner_enhanced.py 192.168.1.0/24 --json results.json --csv results.csv
"""
import sys
import ipaddress
import platform
import subprocess
import concurrent.futures
import socket
import time
import json
import csv

# Try import scapy, mark availability
USE_SCAPY = False
try:
    from scapy.all import ARP, Ether, srp, conf
    USE_SCAPY = True
except Exception:
    USE_SCAPY = False

def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

def resolve_name(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ""

def ping(ip, timeout=1000):
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout), ip]
    else:
        sec = str(int(max(1, round(timeout/1000.0))))
        cmd = ["ping", "-c", "1", "-W", sec, ip]
    try:
        return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    except Exception:
        return False

def scan_ping(network_cidr, workers=200):
    net = ipaddress.ip_network(network_cidr, strict=False)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(ping, str(ip)): ip for ip in net.hosts()}
        for fut in concurrent.futures.as_completed(futs):
            ip = str(futs[fut])
            try:
                alive = fut.result()
            except Exception:
                alive = False
            if alive:
                results.append({"ip": ip, "mac": "", "hostname": resolve_name(ip)})
    return results

def scan_arp(network_cidr, iface=None, timeout=2):
    conf.verb = 0
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network_cidr)
    ans, _ = srp(pkt, timeout=timeout, iface=iface)
    results = []
    for sent, received in ans:
        ip = received.psrc
        mac = received.hwsrc
        results.append({"ip": ip, "mac": mac, "hostname": resolve_name(ip)})
    return results

def save_csv(results, path):
    keys = ["timestamp", "ip", "mac", "hostname"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in results:
            row = {"timestamp": r.get("timestamp",""), "ip": r.get("ip",""), "mac": r.get("mac",""), "hostname": r.get("hostname","")}
            w.writerow(row)

def save_json(results, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print("Usage: python scanner_enhanced.py <network_cidr> [--csv file] [--json file] [--iface IFACE]")
        return
    network = sys.argv[1]
    csv_path = None
    json_path = None
    iface = None
    args = sys.argv[2:]
    for i, a in enumerate(args):
        if a == "--csv" and i+1 < len(args):
            csv_path = args[i+1]
        if a == "--json" and i+1 < len(args):
            json_path = args[i+1]
        if a == "--iface" and i+1 < len(args):
            iface = args[i+1]

    print(f"[{now_iso()}] Scan {network} ... (scapy available: {USE_SCAPY})")
    if USE_SCAPY:
        try:
            results = scan_arp(network, iface=iface)
        except Exception as e:
            print("ARP scan failed:", e)
            print("Falling back to ping scan.")
            results = scan_ping(network)
    else:
        results = scan_ping(network)

    timestamp = now_iso()
    for r in results:
        r["timestamp"] = timestamp

    if not results:
        print("Aucun hôte trouvé.")
    else:
        print("Résultats:")
        for r in sorted(results, key=lambda x: x["ip"]):
            print(f'{r["ip"]}\t{r.get("mac","")}\t{r.get("hostname","")}')

    if csv_path:
        save_csv(results, csv_path)
        print("CSV sauvegardé:", csv_path)
    if json_path:
        save_json(results, json_path)
        print("JSON sauvegardé:", json_path)

if __name__ == "__main__":
    main()
