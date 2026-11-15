#!/usr/bin/env python3
"""Setzt den gemeinsamen Plugin-Katalog aus den Katalogen der einzelnen Plugin-Repositories zusammen."""
import json, sys, urllib.request

SOURCES = [
    "https://raw.githubusercontent.com/derpfiff/cinema-glass/main/manifest.json",
    "https://raw.githubusercontent.com/derpfiff/jellyfin-mediathek/main/manifest.json",
    "https://raw.githubusercontent.com/derpfiff/jellyscribe-fork/main/manifest.json",
]

packages = []
for url in SOURCES:
    with urllib.request.urlopen(urllib.request.Request(url, headers={"Cache-Control": "no-cache"}), timeout=30) as r:
        data = json.load(r)
    if not isinstance(data, list) or not data:
        sys.exit("Ungültiger Katalog: " + url)
    packages.extend(data)

guids = [p["guid"] for p in packages]
if len(set(guids)) != len(guids):
    sys.exit("Doppelte Plugin-GUID im Katalog")
packages.sort(key=lambda p: p["name"].lower())
with open("manifest.json", "w", encoding="utf-8") as f:
    json.dump(packages, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(", ".join("%s %s" % (p["name"], p["versions"][0]["version"]) for p in packages))
