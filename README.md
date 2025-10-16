# Network Scanner
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## Description
Outil Python pour scanner un réseau local.  
Il détecte les appareils connectés, leurs adresses IP, MAC et noms d’hôtes.  
- Utilise ARP si possible (Windows avec Npcap)  
- Sinon fallback ping  
- Export CSV et JSON avec horodatage  
- Interface web Flask simple pour visualiser les résultats

---

## ⚙️ Installation

```bash
git clone https://github.com/BlueT0m/network-scanner.git
cd network-scanner
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows PowerShell
venv\Scripts\activate.ps1

pip install -r requirements.txt
```

---
## 🚀Utilisation

Scanner
```bash
python scanner_enhanced.py 192.168.1.0/24 --json results.json --csv results.csv
````

Interface web
```bash
python web_ui.py
# ouvrir http://127.0.0.1:5000/
# entrer "results.json" pour charger les résultats
```

---

## 💾 Fichiers générés

- results.json → données des appareils détectés
- results.csv → tableur CSV des appareils avec timestamp

---

## 🔧 Prérequis pour ARP (Windows)

- Installer Npcap en mode WinPcap compatible : https://nmap.org/npcap/
- Lancer PowerShell en administrateur
- Sinon, le scanner utilise le mode ping

---

## 📌 Exemples de sortie

| IP              | MAC                  | Hostname      |
| :-------------- | :------------------- | :------------ |
| `192.168.1.239` | `80:30:49:e1:9b:59`  | `MonPC`       |
| `192.168.1.45`  | ` b8:27:eb:12:34:56` | `RaspberryPi` |
