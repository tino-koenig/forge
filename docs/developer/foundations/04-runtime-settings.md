# Foundation 04 – Runtime Settings (Developer)

## Zweck
Löst Runtime-Einstellungen zentral, typisiert und deterministisch auf.

## Wann nutze ich das?
- Wenn ein Mode oder eine Foundation konfigurierbare Laufzeitwerte braucht.
- Wenn Einstellungen aus mehreren Quellen kommen können.
- Wenn Defaults, Grenzen und erlaubte Werte zentral gelten sollen.

## 5-Minuten-Verständnis
- **Input:** ein Setting-Key plus Quellen wie `cli`, `local`, `repo` und `default`
- **Output:** ein aufgelöster, validierter Wert plus Diagnostics
- Foundation 04 beantwortet die Frage: **Welcher Runtime-Wert gilt hier wirklich?**
- Die Registry ist die zentrale Wahrheit für Typ, Default, Bounds und erlaubte Werte.
- Die Foundation entscheidet also nicht nur, **welcher Wert oben liegt**, sondern **welcher Wert wirklich gültig ist**.

## Einfach erklärt (für Einsteiger)
Stell dir Foundation 04 wie einen kleinen, strengen Einstellungs-Prüfer vor.

Es reicht nicht, dass irgendwo ein Wert steht. Forge muss auch prüfen:
- Ist das überhaupt der richtige Typ?
- Liegt der Wert in erlaubten Grenzen?
- Ist der Wert für dieses Setting überhaupt erlaubt?

Ein einfaches Bild:

1. Forge schaut zuerst auf den wichtigsten Zettel.
2. Wenn dort ein Wert steht, wird er geprüft.
3. Wenn er gültig ist, wird er verwendet.
4. Wenn er ungültig ist, geht Forge zur nächsten Quelle.
5. Wenn am Ende nichts Gültiges übrig bleibt, gilt der Default aus der Registry.

```text
cli → local → repo → default
```

Beispiel:
- `analysis.max_files=200` auf CLI → wird verwendet.
- `analysis.max_files="abc"` auf CLI → ungültig, also nächste Quelle prüfen.
- `analysis.max_files=20000` auf CLI, aber das Maximum ist 5000 → ebenfalls ungültig.
- nichts Gültiges gefunden → Default aus der Registry.

Wichtig dabei:
- Nicht jede Quelle gewinnt automatisch.
- Erst muss der Wert auch **zum Setting passen**.
- Die Registry entscheidet, was erlaubt ist.
- Dadurch verhalten sich alle Foundations gleich und bauen nicht ihre eigenen kleinen Sonderregeln.

Kurz gesagt:
- Foundation 04 sagt, **welcher Runtime-Wert wirklich gilt**.
- Nicht der lauteste Wert gewinnt, sondern der **erste gültige** Wert.

## Minimalbeispiel
```python
result = resolve_setting(
    key="analysis.max_files",
    sources={
        "cli": {"analysis.max_files": "200"},
        "repo": {"analysis.max_files": 100},
    },
    registry=RUNTIME_SETTINGS_FOUNDATION_REGISTRY,
)

print(result.value)   # 200
print(result.source)  # cli
```

## Kern-API

### `resolve_setting(key, sources, registry)`
Löst genau ein Setting auf.

Einfach gesagt: Die Funktion sucht den ersten gültigen Wert in der Quellenreihenfolge und erklärt über Diagnostics, warum andere Werte nicht verwendet wurden.

- prüft Quellen in Prioritätsreihenfolge
- validiert Typ und Grenzen
- fällt kontrolliert zurück
- liefert Diagnostics

### `resolve_settings(keys, sources, registry)`
Löst mehrere Settings deterministisch auf.

### `SettingSpec`
Definiert den Vertrag eines Settings in der Registry.

## Wichtige Modelle

### `SettingSpec`
Definiert ein Setting zentral und beschreibt, welcher Typ, welcher Default und welche Regeln dafür gelten.

Wichtige Felder:
- `key`
- `kind`
- `default`
- `min` / `max`
- `allowed_values`
- `normalize`
- `allow_default_fallback`

### `ResolvedSetting`
Ergebnis der Auflösung, also der am Ende wirklich geltende Wert inklusive Quelle und Diagnostics.

Wichtige Felder:
- `key`
- `value`
- `source`
- `diagnostics`

### `SettingDiagnostic`
Beschreibt, warum ein Wert verworfen, ersetzt oder auf einen Fallback reduziert wurde.

## Invarianten (sehr wichtig)
- Die Registry ist die zentrale Wahrheit für Runtime-Settings.
- Quellenpriorität ist fest: `cli > local > repo > default`.
- Ungültige Werte werden nicht still übernommen.
- Unknown Keys werden diagnostiziert.
- Defaults müssen selbst gültig sein.
- Modes und Foundations sollen keine eigene `_resolve_runtime_*`-Logik bauen.

## Typischer Ablauf
```python
registry = RUNTIME_SETTINGS_FOUNDATION_REGISTRY

resolved = resolve_settings(
    keys=("analysis.max_files", "analysis.mode"),
    sources=sources,
    registry=registry,
)

# Danach werden nur noch die bereits aufgelösten Werte verwendet.
max_files = resolved["analysis.max_files"].value
mode = resolved["analysis.mode"].value
```

## Integration

**Wird verwendet von:**
- allen Foundations oder Modes, die konfigurierbare Runtime-Werte brauchen
- besonders Retrieval-, Ranking-, Orchestration- und Output-nahe Schichten

**Schafft die Grundlage für:**
- konsistente Runtime-Konfiguration im ganzen System
- nachvollziehbare Fallback-Entscheidungen
- zentrale, testbare Settings statt verteilter Sonderlogik

## Typische Fehler
- Modes lösen Settings selbst auf statt Foundation 04 zu nutzen.
- Werte werden aus der höchsten Quelle übernommen, obwohl sie ungültig sind.
- Unknown Keys werden still ignoriert.
- Defaults in der Registry sind selbst ungültig.
- `bool` wird versehentlich wie `int` behandelt.
- `enum`-Werte werden nicht gegen `allowed_values` geprüft.
- Verschiedene Foundations definieren für dieselben Settings unterschiedliche Fallback-Logik.

## Review-Checkliste
- [ ] Neue Runtime-Settings stehen in der zentralen Registry.
- [ ] Typ, Bounds und erlaubte Werte sind sauber definiert.
- [ ] Resolver-Logik bleibt zentral und wird nicht in Modes dupliziert.
- [ ] Diagnostics sind bei Invalid/Fallback-Fällen sichtbar.
- [ ] Quellenpriorität wird korrekt eingehalten.
- [ ] Defaults sind gültig und testbar.

## Referenz
Siehe vollständige Spezifikation:
`docs/foundations/04-runtime-settings-foundation.md`