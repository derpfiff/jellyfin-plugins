#!/usr/bin/env python3
"""Setzt die gemeinsamen Plugin-Kataloge aus den Katalogen der einzelnen Plugin-Repositories zusammen.

manifest.json  – Produktion: nur freigegebene Versionen (manifest.json der Repositories).
staging.json   – Test: alles aus der Produktion plus die Versionen, die noch geprüft werden
                 (manifest-staging.json der Repositories). Nur Server, die diesen Katalog eingetragen haben, sehen sie.
"""
import json, os, sys, urllib.error, urllib.request

REPOS = ["derpfiff/cinema-glass", "derpfiff/jellyfin-mediathek", "derpfiff/jellyscribe-fork"]


def load(repo, name, required=True):
    # über die GitHub-API statt raw.githubusercontent.com: die API liefert den aktuellen Stand, raw ist bis zu 5 Minuten alt
    url = "https://api.github.com/repos/%s/contents/%s?ref=main" % (repo, name)
    headers = {"Accept": "application/vnd.github.raw", "User-Agent": "catalog-merge"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404 and not required:
            return []
        raise
    if not isinstance(data, list) or (required and not data):
        sys.exit("Ungültiger Katalog: " + url)
    return data


def num(v):
    return tuple((list(map(int, v.split("."))) + [0, 0, 0, 0])[:4])


prod, staging = [], []
for repo in REPOS:
    main = load(repo, "manifest.json")
    test = {p["guid"]: p for p in load(repo, "manifest-staging.json", required=False)}
    prod.extend(main)
    for p in main:
        q = dict(p)
        extra = test.get(p["guid"], {}).get("versions", [])
        seen, versions = set(), []
        for v in extra + p["versions"]:
            if v["version"] not in seen:
                seen.add(v["version"])
                versions.append(v)
        q["versions"] = sorted(versions, key=lambda v: num(v["version"]), reverse=True)
        staging.append(q)

for name, packages in (("manifest.json", prod), ("staging.json", staging)):
    guids = [p["guid"] for p in packages]
    if len(set(guids)) != len(guids):
        sys.exit("Doppelte Plugin-GUID im Katalog")
    packages.sort(key=lambda p: p["name"].lower())
    with open(name, "w", encoding="utf-8") as f:
        json.dump(packages, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(name + ": " + ", ".join("%s %s" % (p["name"], p["versions"][0]["version"]) for p in packages))
