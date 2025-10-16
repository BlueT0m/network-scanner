# 🌐 Network Scanner

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 🧩 Description

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
