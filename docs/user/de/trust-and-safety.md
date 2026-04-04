# Trust & Safety

Forge setzt auf explizite Capability-Grenzen statt versteckter Automatisierung.

## Lese-Scope

- Repository-Dateien
- `.forge`-Artefakte (`index.json`, `graph.json`, runs/logs)
- optionale Framework-Refs/-Docs
- optionale Web-Retrieval-Pfade in Ask-Presets (wenn aktiviert)

## Write-Scope

- aktuelle Schreibvorgaenge sind auf Forge-Artefakte/Settings/Session-State begrenzt
- aktuelle Analysemodi aendern keinen Source-Code
- zukuenftige Code-Write-Modi muessen explizite Zielgrenzen definieren

## Auditierbarkeit

- maschinenlesbare Output-Contracts (`--output-format json`)
- explizite Unsicherheits-/Fallback-Sektionen
- Run-Historie und Logs sind einsehbar
