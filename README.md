# Network Scanner

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

Outil Python pour découvrir les appareils d’un réseau local.  
Détecte IP, MAC, hostname. Utilise ARP si possible (Npcap sur Windows), sinon fallback ICMP (ping). Export JSON/CSV et interface web simple.

---

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)
- [Ethics](#ethics)

---

## Installation

1. Clone le dépôt :
```bash
git clone https://github.com/BlueT0m/network-scanner.git
cd network-scanner
```
2. Installer les dépendances :
```bash
pip install -r requirements.txt
```
3. (Optionnel pour ARP sur Windows) Installer Npcap (WinPcap-compatible) : https://nmap.org/npcap/
---

## Usage :

Scanner (ARP si possible, sinon ping)
```bash
python scanner_enhanced.py 192.168.1.0/24 --json results.json --csv results.csv
```
Interface web pour visualiser les résultats
```bash
python web_ui.py
```
Ouvre `http://127.0.0.1:5000/` puis saisis `results.json` pour charger les résultats.

---

## Exemple

| IP              | MAC                  | Hostname      |
| :-------------- | :------------------- | :------------ |
| `192.168.1.239` | `80:30:49:e1:9b:59`  | `MonPC`       |
| `192.168.1.45`  | ` b8:27:eb:12:34:56` | `RaspberryPi` |

---

## Features

- ARP scan rapide (scapy + Npcap) ou fallback ping (cross-platform).

- Résolution reverse DNS pour hostname.

- Export JSON et CSV avec timestamp.

- Interface Flask simple pour visualiser les résultats.

- Compatible Windows, macOS, Linux.

---

## Files

- `scanner_enhanced.py` — script principal (ARP/ping, export CSV/JSON).

- `web_ui.py` — interface Flask pour affichage des résultats.

- `requirements.txt` — `scapy`, `Flask`.

- `results.json` / `results.csv` — fichiers générés par le scanner.

---

## Contributing

1. Fork le dépôt.

2. Crée une branche : `git checkout -b feature/ma-fonctionnalite`.

3. Commit tes changements : `git commit -m "Ajout: ..."`.

4. Push : `git push origin feature/ma-fonctionnalite`.

5. Ouvre une Pull Request.

---

## License

This project is licensed under the [MIT License](LICENSE).
