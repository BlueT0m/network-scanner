#!/usr/bin/env python3
from flask import Flask, render_template_string, request
import json, os

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Network Scanner - UI</title>
<h2>Résultats du dernier scan</h2>
<form method=post>
  Fichier JSON: <input name=file type=text placeholder="results.json" value="results.json">
  <input type=submit value=Charger>
</form>
{% if rows %}
<table border=1 cellpadding=6>
<tr><th>timestamp</th><th>ip</th><th>mac</th><th>hostname</th></tr>
{% for r in rows %}
<tr><td>{{r.timestamp}}</td><td>{{r.ip}}</td><td>{{r.mac}}</td><td>{{r.hostname}}</td></tr>
{% endfor %}
</table>
{% endif %}
"""

def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

@app.route("/", methods=["GET","POST"])
def index():
    rows = []
    if request.method == "POST":
        path = request.form.get("file","results.json").strip()
        if os.path.exists(path):
            rows = load_json(path)
    return render_template_string(HTML, rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
