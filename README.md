# Plugin-Katalog von derpfiff

Ein Katalog für alle meine Jellyfin-Plugins. In Jellyfin unter **Dashboard → Plugins → Repositories** diese Adresse eintragen:

```
https://raw.githubusercontent.com/derpfiff/jellyfin-plugins/main/manifest.json
```

| Plugin | Was es tut | Repository |
|---|---|---|
| **Cinema Glass** | Glas-Oberfläche im Stil von Apple TV, „Entdecken“ mit persönlichen Empfehlungen, Anfragen über Seerr, Bewerten nach dem Schauen | [cinema-glass](https://github.com/derpfiff/cinema-glass) |
| **Mediathek** | Sendungen der öffentlich-rechtlichen Mediatheken als Bibliothek in Jellyfin | [jellyfin-mediathek](https://github.com/derpfiff/jellyfin-mediathek) |
| **Jellyscribe** (Fork) | Letterboxd-Tagebuch auf Wunsch: trägt nur ein, was im Bewerten-Dialog von Cinema Glass bestätigt wird | [jellyscribe-fork](https://github.com/derpfiff/jellyscribe-fork) |

Alle Plugins sind für **Jellyfin 12.4**. Die Datei `manifest.json` setzt GitHub stündlich aus den Katalogen der einzelnen Repositories zusammen (`scripts/merge.py`); die bisherigen Einzel-Kataloge funktionieren weiter.
