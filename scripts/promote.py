#!/usr/bin/env python3
"""Gibt eine getestete Version frei: verschiebt sie in einem Plugin-Repository aus manifest-staging.json nach manifest.json.

Aufruf: python3 promote.py <Pfad zum Plugin-Repository> <Version>
Danach im Plugin-Repository committen und pushen und den Katalog aktualisieren (Workflow „Katalog aktualisieren“).
"""
import json, os, sys

repo, ver = sys.argv[1], sys.argv[2]
num = lambda v: tuple((list(map(int, v.split("."))) + [0, 0, 0, 0])[:4])
sp, mp = os.path.join(repo, "manifest-staging.json"), os.path.join(repo, "manifest.json")
staging, main = json.load(open(sp)), json.load(open(mp))
entry = next((v for v in staging[0]["versions"] if num(v["version"]) == num(ver)), None)
if entry is None:
    sys.exit("Version %s steht nicht im Staging-Katalog" % ver)
staging[0]["versions"] = [v for v in staging[0]["versions"] if num(v["version"]) != num(ver)]
main[0]["versions"] = sorted([entry] + [v for v in main[0]["versions"] if num(v["version"]) != num(ver)], key=lambda v: num(v["version"]), reverse=True)
for path, data in ((sp, staging), (mp, main)):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
print("freigegeben:", main[0]["name"], entry["version"])
