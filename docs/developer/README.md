# Forge Developer Docs

Dieses Verzeichnis enthält die **entwicklerorientierte Arbeitsdokumentation** für Forge.

Im Unterschied zu den vollständigen Spezifikationen in `docs/foundations/` sind die Inhalte hier bewusst kürzer, direkter und näher an der täglichen Umsetzung im Code.

## Zweck

Diese Dokumentation soll neuen und bestehenden Entwicklern helfen,
- schneller in Forge einzusteigen,
- die wichtigsten Foundations in praktischer Form zu verstehen,
- Änderungen sauber, klein und vertragskonform umzusetzen,
- Reviews gezielter und konsistenter durchzuführen.

## Was du hier findest

### Foundations
Developer-Versionen der zentralen Foundations.

Sie beantworten vor allem:
- Wofür ist diese Foundation da?
- Wann nutze ich sie?
- Welche Invarianten gelten?
- Welche typischen Fehler sollte ich vermeiden?

### Implementation Guides
Konkrete Umsetzungsmuster für häufige Änderungen.

### Review Guides
Praktische Prüfkriterien für Code-Reviews, Regressionen und Vertragskonformität.

## Wie diese Doku zu lesen ist

Diese Dokumentation ist **nicht** die Quelle der Wahrheit für den Systemvertrag.

Die Quelle der Wahrheit bleibt immer:
- `docs/foundations/`

Die Developer-Dokumente in diesem Verzeichnis sind die **Arbeitsfassung für Entwickler**:
- verständlicher,
- kompakter,
- näher an typischen Implementierungsfragen.

## Empfohlener Einstieg

1. Zuerst die Developer-Foundations lesen.
2. Danach bei Bedarf die vollständige Spezifikation in `docs/foundations/` nachschlagen.
3. Zugehörige Features, Issues oder Änderungsziele prüfen.
4. Änderungen mit kleinstmöglichem, korrektem Diff umsetzen.

## Empfohlene Lesereihenfolge der Foundations

### Ablauf und Steuerung
- [Foundation 01 – Mode Execution](foundations/01-mode-execution.md)
- [Foundation 02 – Orchestration](foundations/02-orchestration.md)
- [Foundation 04 – Runtime Settings](foundations/04-runtime-settings.md)

### Such- und Entscheidungsfluss
- [Foundation 07 – Retrieval](foundations/07-retrieval.md)
- [Foundation 08 – Evidence Ranking](foundations/08-evidence-ranking.md)
- [Foundation 09 – Target Resolution](foundations/09-target-resolution.md)

### Ausgabe, Nachvollziehbarkeit und Workspace
- [Foundation 10 – Output Contract](foundations/10-output-contract.md)
- [Foundation 11 – Observability](foundations/11-observability.md)
- [Foundation 12 – Repository / Workspace](foundations/12-repository-workspace.md)

## Praktische Arbeitsregel

Wenn du an Forge arbeitest, stelle dir bei jeder Änderung zuerst diese Fragen:
- Welche Foundation ist betroffen?
- Welche Invarianten dieser Foundation darf ich nicht verletzen?
- Verändere ich gerade nur Implementierungsdetails oder still den Vertrag?
- Gehört diese Logik wirklich in diese Schicht?

## Zielbild

Diese Developer Docs sollen dazu führen, dass Änderungen an Forge:
- besser verständlich,
- konsistenter,
- leichter reviewbar,
- und sicherer weiterentwickelbar werden.
