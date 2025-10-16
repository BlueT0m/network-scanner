#!/usr/bin/env python3
import subprocess
import platform
import ipaddress
import concurrent.futures
import sys
from socket import gethostbyaddr, herror

def ping(ip: str, timeout=1000) -> bool:
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout), ip]
    else:
        # macOS/linux: timeout in seconds -> use -c 1 and -W (Linux) or -t (macOS unsupported)
        cmd = ["ping", "-c", "1", "-W", str(int(timeout/1000)), ip]
    try:
        return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    except Exception:
        return False

def scan_network(network_cidr: str, workers=100):
    net = ipaddress.ip_network(network_cidr, strict=False)
    alive = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(ping, str(ip)): ip for ip in net.hosts()}
        for fut in concurrent.futures.as_completed(futures):
            ip = futures[fut]
            try:
                if fut.result():
                    name = ""
                    try:
                        name = gethostbyaddr(str(ip))[0]
                    except herror:
                        name = ""
                    alive.append((str(ip), name))
            except Exception:
                pass
    return alive

def main():
    if len(sys.argv) != 2:
        print("Usage: python scanner_ping.py 192.168.1.0/24")
        return
    network = sys.argv[1]
    print(f"Scan de {network} ...")
    results = scan_network(network)
    if not results:
        print("Aucun hôte trouvé.")
        return
    print("IP\t\tHostname")
    for ip, name in sorted(results):
        print(f"{ip}\t{name}")

if __name__ == "__main__":
    main()
