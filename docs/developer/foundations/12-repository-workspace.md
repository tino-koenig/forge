# Foundation 12 – Repository / Workspace (Developer)

## Zweck
Definiert den Arbeitsraum (Workspace) und stellt sicher, dass alle Pfade, Dateien und Zugriffe konsistent und kontrolliert behandelt werden.

## Wann nutze ich das?
- Wenn du mit Dateien, Verzeichnissen oder Repositories arbeitest.
- Wenn du sicherstellen willst, dass Zugriff (lesen/schreiben) korrekt geregelt ist.
- Wenn du Pfade und Lokatoren einheitlich behandeln musst.

## 5-Minuten-Verständnis
- **Input:** Pfade, Lokatoren und Konfiguration.
- **Output:** strukturierter `WorkspaceContext` plus geprüfte Zugriffsentscheidungen.
- Diese Foundation beantwortet nicht nur: **Darf ich auf diese Datei zugreifen und wie?**
- Sie legt auch fest: **Was gehört überhaupt zum gültigen Arbeitsraum, was ist nur Artefakt, und was darf später gelesen oder geschrieben werden?**
- Foundation 12 entscheidet also nicht nur über einzelne Pfade, sondern definiert den gemeinsamen Arbeitsraum für alle nachgelagerten Foundations.

## Einfach erklärt (für Einsteiger)
Stell dir Foundation 12 wie einen Pförtner und einen Lageplan gleichzeitig vor.

Ein Pförtner entscheidet:
- Wer oder was darf überhaupt hinein?
- Was ist erlaubt?
- Was ist gesperrt?

Ein Lageplan erklärt zusätzlich:
- Was ist Produktcode?
- Was ist Doku?
- Was ist Build-Ausgabe?
- Was ist nur Artefakt oder extern?

Genau das macht Foundation 12 für Forge.

Sie beantwortet drei einfache Fragen:

1. **Wo darf Forge überhaupt hinschauen?**
2. **Was ist das fachlich für eine Datei oder Referenz?**
3. **Darf Forge sie nur lesen oder auch später ändern?**

Ein einfaches Bild:

```text
Datei/Pfad → zuerst einordnen → dann Regeln prüfen → dann Entscheidung treffen
```

Ein alltagsnahes Beispiel:
- `src/app.py` liegt im Workspace und ist meist Produktcode → lesen oft erlaubt, schreiben nur wenn der Write-Scope es erlaubt.
- `docs/guide.md` liegt im Workspace, ist aber Doku → kann je nach Aufgabe anders behandelt werden als Produktcode.
- `vendor/` oder `node_modules/` gehören technisch oft zum Repo, sind aber normalerweise keine Primärquellen für code-zentrierte Analyse.
- `dist/` oder `build/` sind meist Build-Ausgabe oder Artefakte → sichtbar, aber nicht wie normaler Quellcode behandeln.
- eine Datei außerhalb des Workspace wird nicht einfach still mitgenommen, sondern bewusst blockiert oder diagnostiziert.

Warum ist das wichtig?
Weil Forge sonst in verschiedenen Teilen des Systems dieselbe Datei unterschiedlich behandeln würde.
Dann könnte zum Beispiel:
- Retrieval etwas als normalen Treffer ansehen,
- Resolution denselben Pfad anders lesen,
- und ein späterer Write-Pfad plötzlich an einer Stelle arbeiten, die eigentlich gar nicht erlaubt war.

Foundation 12 verhindert genau das, indem sie für alle dieselbe Grundlage liefert.

Wichtig dabei:
- Foundation 12 ist **nicht nur ein Pfad-Helper**.
- Sie definiert den **gültigen Arbeitsraum** für alle späteren Foundations.
- Sie sorgt dafür, dass Retrieval, Ranking, Resolution und spätere Write-Pfade **dieselben Regeln** verwenden.
- Sie trennt sichtbar zwischen lesen, schreiben, Rollenklassifikation und Workspace-Grenzen.

Kurz gesagt:
- Foundation 12 sagt, **was zum Arbeitsraum gehört**.
- Foundation 12 sagt, **wie ein Pfad einheitlich dargestellt wird**.
- Foundation 12 sagt, **ob gelesen oder geschrieben werden darf**.
- Foundation 12 sagt, **welche Rolle eine Datei fachlich hat**.

## Minimalbeispiel
```python
workspace = resolve_workspace_context(args, repo_root)

locator = normalize_locator("src/app.py", workspace)

read_decision = is_in_read_scope(locator, workspace)
write_decision = is_in_write_scope(locator, workspace)
```

## Kern-API

### `resolve_workspace_context(...)`
- erstellt den Workspace-Kontext

Einfach gesagt: Hier wird festgelegt, wie Forge den aktuellen Arbeitsraum überhaupt sieht.

### `normalize_locator(...)`
- wandelt Pfade in kanonische Lokatoren um

Das ist wichtig, damit später nicht verschiedene Foundations denselben Pfad in leicht unterschiedlicher Form behandeln.

### `is_in_read_scope(...)`
- prüft, ob gelesen werden darf

### `is_in_write_scope(...)`
- prüft, ob geschrieben werden darf

### `classify_file_role(...)`
- bestimmt Rolle einer Datei (source, config, test, ...)

## Wichtige Modelle

### `WorkspaceContext`
Die zentrale Beschreibung des gültigen Arbeitsraums, inklusive Roots, Scopes, Regeln und Workspace-Status.

### `CanonicalLocator`
Die normalisierte und stabile Darstellung eines Pfads oder Verweises innerhalb des Systems.

### `ScopeDecision`
Ergebnis einer Zugriffprüfung, also ob etwas gelesen oder geschrieben werden darf und auf welcher Regelgrundlage diese Entscheidung entstanden ist.

### `FileRoleAssignment`
Die fachliche Rolle einer Datei, zum Beispiel `source`, `config`, `test`, `docs`, `generated`, `artifact` oder `external`.

## Invarianten (sehr wichtig)
- Jeder Zugriff erfolgt über einen kanonischen Locator.
- Pfade sind immer normalisiert und deterministisch darstellbar.
- Read und Write sind getrennte Entscheidungen.
- Write ist standardmäßig verboten (deny-by-default).
- Include-/Ignore- und Scope-Regeln sind explizit und diagnostizierbar.
- Dateien erhalten genau eine primäre Rolle; Mehrfachklassifikation muss diagnostiziert werden.
- Der Workspace ist eine zentrale Wahrheit für nachgelagerte Foundations.

## Typischer Ablauf
```python
workspace = resolve_workspace_context(...)

locator = normalize_locator(path, workspace)

read_decision = is_in_read_scope(locator, workspace)
if not read_decision.allowed:
    raise Error("not allowed")

# Erst nach diesen Schritten dürfen weitere Foundations sinnvoll arbeiten.
```

## Integration

**Wird verwendet von:**
- fast allen späteren Foundations, besonders 07 (Retrieval), 09 (Target Resolution), 14 (Policy) und spätere Write-/Mutation-Pfade

**Schafft die Grundlage für:**
- sichere Dateioperationen
- konsistente Pfadverarbeitung
- ein gemeinsames Workspace-Modell für alle Foundations
- reproduzierbare Scope- und Lokator-Entscheidungen

## Typische Fehler
- Direkter Zugriff auf rohe Pfade ohne Locator.
- Write-Zugriff ohne separate Scope-Prüfung.
- Unterschiedliche Pfadrepräsentationen in verschiedenen Foundations.
- Ignorieren von Workspace-Grenzen oder Include-/Ignore-Regeln.
- Vendor-, Build- oder Artefaktbereiche wie normalen Produktcode behandeln.
- Rollenklassifikation still mehrfach oder uneinheitlich werden lassen.
- Retrieval, Resolution oder spätere Write-Pfade verwenden nicht dieselbe Workspace-Wahrheit.

## Review-Checkliste
- [ ] Alle relevanten Zugriffe nutzen kanonische Locator.
- [ ] Read und Write werden getrennt geprüft.
- [ ] Pfade und Regeln sind normalisiert und deterministisch.
- [ ] Include-/Ignore- und Scope-Entscheidungen sind nachvollziehbar.
- [ ] Write bleibt deny-by-default.
- [ ] Rollenklassifikation ist konsistent.
- [ ] Es gibt keine impliziten Zugriffe außerhalb des Workspace.

## Referenz
Siehe vollständige Spezifikation:
`docs/foundations/12-repository-workspace-foundation.md`
