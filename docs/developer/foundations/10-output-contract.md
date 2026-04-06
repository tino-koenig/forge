# Foundation 10 – Output Contract (Developer)

## Zweck
Erzeugt eine strukturierte, stabile Ausgabe eines Runs, die sowohl maschinenlesbar als auch für Menschen verständlich ist.

## Wann nutze ich das?
- Wenn du Ergebnisse eines Modes strukturiert ausgeben willst.
- Wenn du eine klare Trennung zwischen Daten und Darstellung brauchst.
- Wenn du nachvollziehbare, standardisierte Outputs willst.

## 5-Minuten-Verständnis
- **Input:** strukturierte Daten (z. B. aus Execution, Orchestration, Retrieval, Ranking, Resolution)
- **Output:** `OutputContract`
- Der Output Contract ist die **einzige Quelle der Wahrheit für Ergebnisse**
- Die Foundation entscheidet also nicht, **was fachlich richtig ist**, sondern sorgt dafür, dass Ergebnisse vollständig, stabil und einheitlich ausgegeben werden.
- Views (Text/Anzeige) werden daraus abgeleitet

## Einfach erklärt (für Einsteiger)
Stell dir Foundation 10 wie die verbindliche Verpackung eines Ergebnisses vor.

Vorher haben andere Foundations schon gearbeitet:
- Foundation 01 hat ausgeführt.
- Foundation 02 hat gesteuert.
- Foundation 07 bis 09 haben fachliche Ergebnisse erzeugt.

Jetzt sorgt Foundation 10 dafür, dass daraus **eine saubere, einheitliche und verlässliche Ausgabe** wird.

Ein einfaches Bild:

1. Im System liegen interne Daten vor.
2. Diese Daten werden in feste Sections einsortiert.
3. Daraus entsteht ein strukturierter Contract.
4. Anzeigen oder Textansichten lesen nur noch aus diesem Contract.

```text
Interne Daten → strukturierter Contract → Anzeige
```

Wichtig dabei:
- Der Contract ist die eigentliche Wahrheit.
- Die Anzeige erfindet nichts dazu.
- Wenn etwas im Contract nicht steht, soll es auch nicht plötzlich in der View erscheinen.

Ein alltagsnahes Beispiel:
- Ein Mode hat Diagnostics, Runtime-Settings und vielleicht Ranking- oder Resolution-Ergebnisse erzeugt.
- Foundation 10 sortiert diese Informationen in feste Bereiche ein.
- Danach kann eine Standard-Ansicht, eine kompakte Ansicht oder eine API-Ausgabe darauf zugreifen.
- Alle lesen aus derselben Quelle.

Warum ist das wichtig?
Weil man sonst schnell diese Probleme bekommt:
- Die Textansicht zeigt etwas anderes als die JSON-Ausgabe.
- Eine View enthält eigene Fachlogik.
- Eine UI ergänzt still Informationen, die im eigentlichen Ergebnis gar nicht sauber vorhanden waren.

Kurz gesagt:
- Foundation 10 baut **nicht das Ergebnis selbst**.
- Foundation 10 sorgt dafür, dass das Ergebnis **sauber verpackt, geprüft und ausgegeben** wird.

## Minimalbeispiel
```python
contract = build_contract_core(
    sections={
        "diagnostics": diagnostics,
        "runtime_settings": settings,
    }
)

text = render_view(contract, view="standard")
```

## Kern-API

### `build_contract_core(...)`
- erstellt den Output Contract
- sammelt Section-Daten

Einfach gesagt: Hier werden die vorhandenen strukturierten Ergebnisse in einen gemeinsamen, stabilen Ausgabevertrag überführt.

### `validate_contract_schema(...)`
- prüft Struktur und Mindestsemantik

### `render_view(contract, view)`
- erzeugt Darstellung aus dem Contract

## Wichtige Modelle

### `OutputContract`
Die zentrale Ergebnisstruktur, aus der später alle Views und Ausgaben abgeleitet werden.

### `SectionBuilderResult`
Ergebnis eines Section-Builders, also eines Bausteins, der genau eine Section in den Contract einbringt.

### `ContractDiagnostic`
Diagnose für Probleme oder Auffälligkeiten im Output-Contract selbst.

## Invarianten (sehr wichtig)
- Der JSON-Contract ist die führende Wahrheit.
- Views dürfen keine neue Fachlogik enthalten.
- Sections haben feste, stabile Schlüssel.
- Section-Status ist explizit (`available|not_applicable|omitted|fallback`).
- Diagnostics, Policy-Verletzungen und Limits bleiben getrennt.
- Die gleiche Eingabe soll zum gleichen Output-Contract führen.

## Typischer Ablauf
```python
sections = collect_section_contributions(...)

contract = build_contract_core(sections)

validate_contract_schema(contract)

# Erst danach wird aus dem Contract eine konkrete Ansicht gebaut.
view = render_view(contract, "standard")
```

## Integration

**Erwartet Input von:**
- Foundation 01 (Execution)
- Foundation 02 (Orchestration)
- Foundation 07–09 (fachliche Ergebnisse)

**Schafft die Grundlage für:**
- Anzeige / API
- externe Systeme
- spätere Auswertung und Vergleichbarkeit von Ergebnissen
- konsistente Darstellung über mehrere Views hinweg

## Typische Fehler
- Logik wird in Views eingebaut
- Sections werden dynamisch statt stabil erzeugt
- Diagnostics werden mit Ergebnissen vermischt
- Output enthält versteckte Zusatzinformationen
- Eine View ergänzt fachliche Informationen, die im Contract selbst nicht sauber enthalten sind.
- Unterschiedliche Ausgabekanäle lesen nicht aus derselben Contract-Struktur.

## Review-Checkliste
- [ ] Der Contract enthält alle relevanten Daten.
- [ ] Sections sind stabil benannt.
- [ ] Views enthalten keine Fachlogik.
- [ ] Statuswerte und Section-Status sind korrekt.
- [ ] Diagnostics, Policy-Verletzungen und Limits sind getrennt.
- [ ] Mehrere Views greifen auf dieselbe Contract-Wahrheit zu.

## Referenz
Siehe vollständige Spezifikation:
`docs/foundations/10-output-contract-foundation.md`