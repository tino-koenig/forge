
# Foundation 01 – Mode Execution (Developer)

## Zweck
Führt einen Mode deterministisch über eine fest definierte Reihenfolge von Stages aus.

## Wann nutze ich das?
- Wenn du einen neuen Mode bauen willst.
- Wenn du mehrere Verarbeitungsschritte sauber hintereinander ausführen willst.
- Wenn du keine versteckte Logik, sondern einen klar nachvollziehbaren Ablauf brauchst.

## 5-Minuten-Verständnis
- **Input:** Ein Plan (`ModeExecutionPlan`) plus Kontext.
- **Output:** Ein Ergebnis (`ExecutionOutcome`).
- Der Plan definiert, **welche Stages in welcher Reihenfolge laufen**.
- Jede Stage liefert ein `StageResult`.
- Der State wird Schritt für Schritt weiterentwickelt.
- Eine Stage beschreibt also nicht den ganzen Ablauf, sondern nur ihren eigenen kleinen Beitrag.

**Wichtig:**
- Diese Foundation **führt nur aus**.
- Sie entscheidet **nicht**, was als Nächstes passieren soll. Das macht Foundation 02.

## Einfach erklärt (für Einsteiger)
Stell dir einen Mode wie eine kleine Arbeitskette vor.

Ein Beispiel aus dem Alltag:
- Zuerst wird etwas vorbereitet.
- Dann werden Informationen eingesammelt.
- Danach werden sie ausgewertet.
- Am Ende wird ein sauberes Ergebnis gebaut.

Genau so arbeitet Foundation 01 auch. Sie nimmt eine feste Liste von Schritten und führt sie nacheinander aus.

1. Du hast eine Liste von Schritten (Stages).
2. Jeder Schritt bekommt den aktuellen Zustand.
3. Der Schritt liefert zurück, was sich geändert hat.
4. Diese Änderung wird in den Zustand übernommen.
5. Dann läuft der nächste Schritt.
6. Am Ende kommt `finalize`.

```text
init → retrieve → rank → finalize
```

Wichtig dabei:
- Eine Stage macht **nicht alles**, sondern nur ihren eigenen Teil.
- Der Zustand wandert von Stage zu Stage weiter.
- Es gibt keine versteckten Zwischenschritte.
- Dadurch bleibt der Ablauf nachvollziehbar und testbar.

Ein einfaches Bild:
- `init` bereitet den Lauf vor.
- `retrieve` sammelt Daten.
- `rank` verarbeitet oder bewertet diese Daten weiter.
- `finalize` baut daraus das abschließende Ergebnis.

Warum ist das nützlich?
Weil man später sehr klar sagen kann:
- In welchem Schritt ist etwas passiert?
- Welche Stage hat den Zustand verändert?
- Warum sieht das Endergebnis so aus?

Was Foundation 01 **nicht** macht:
- Sie entscheidet nicht, **ob** weitergemacht wird. Das macht Foundation 02.
- Sie bewertet nicht selbst Dateien oder Evidenz. Das machen spätere fachliche Foundations.
- Sie ersetzt keine Business-Logik der Stages.

Kurz gesagt:
- Foundation 01 ist das **Ablaufgerüst**.
- Die eigentliche Fachlogik steckt in den einzelnen Stages.

## Minimalbeispiel
```python
plan = ModeExecutionPlan(
    mode_name="query_v2",
    stages=(
        StageDefinition("init", init_stage),
        StageDefinition("retrieve", retrieve_stage),
        StageDefinition("rank", rank_stage),
        StageDefinition("finalize", finalize_stage),
    ),
)

result = run_mode(plan, context)
```

## Kern-API

### `run_mode(plan, context) -> ExecutionOutcome`
Führt den kompletten Mode aus.

- verarbeitet alle Stages der Reihe nach
- sammelt Ergebnisse
- erzeugt einen Trace

### `StageResult`
Das wichtigste Objekt.

Ein `StageResult` sagt vereinfacht: "Diese Stage ist fertig, so ist sie ausgegangen, und das hat sie am Zustand geändert."

```python
StageResult(
    stage_name="retrieve",
    stage_id="retrieve_1",
    status="ok",
    state_delta={...},
)
```

## Wichtige Modelle

### `ModeExecutionPlan`
Enthält die Reihenfolge der Stages und ist damit der feste Ablaufplan eines Modes.

### `ExecutionState`
Aktueller Zustand während der Ausführung. Dieser Zustand wird Schritt für Schritt weitergereicht und verändert.

### `StageResult`
Ergebnis einer einzelnen Stage, inklusive Status und `state_delta`.

### `ExecutionOutcome`
Gesamtergebnis des Modes nach allen Stages, inklusive finalem Zustand und Trace.

## Invarianten (sehr wichtig)
- `init` läuft genau einmal am Anfang.
- `finalize` läuft immer am Ende, auch bei Fehlern.
- Es gibt keine versteckten Stages.
- `status` ist immer einer von:
  - `ok`
  - `noop`
  - `blocked`
  - `error`
- `state_delta` ist eine **teilweise Änderung**, kein kompletter State.
- Stages dürfen keine finalen Ergebnisse bauen, sondern nur Beiträge liefern.

## Typischer Ablauf
```python
state = initial_state

for stage in plan.stages:
    result = stage.handler(state)
    state = apply_stage_result(state, result)

# Nach allen Stages liegt der finale Zustand vor.
return ExecutionOutcome(state=state)
```

## Integration

**Wird verwendet von:**
- Foundation 02 (Orchestration)
- zukünftigen Modes wie `query_v2` oder `propose_v2`

**Erwartet Input von:**
- Foundation 04 (Settings)
- Foundation 12 (Workspace)

**Schafft die Grundlage für:**
- Foundation 10 (Output Contract): übernimmt später strukturierte Ausführungsergebnisse und Beiträge.
- Foundation 11 (Observability): kann Trace- und Execution-Daten beobachten und auswerten.

## Typische Fehler
- Stage verändert den kompletten State statt nur `state_delta`.
- Stage erzeugt finale Ergebnisse statt nur Beiträge.
- Zusätzliche Schritte laufen außerhalb des Plans.
- Es werden freie Statuswerte statt des geschlossenen Statusraums verwendet.
- `finalize` wird übersprungen.
- Eine Stage trifft Orchestration-Entscheidungen, die eigentlich in Foundation 02 gehören.

## Review-Checkliste
- [ ] Stages sind klar definiert.
- [ ] Die Reihenfolge ist deterministisch.
- [ ] Es gibt keine versteckten Schritte.
- [ ] `state_delta` wird korrekt verwendet.
- [ ] Statuswerte stammen aus dem geschlossenen Statusraum.
- [ ] `finalize` enthält keine neue Fachlogik.

## Referenz
Siehe vollständige Spezifikation:
`docs/foundations/01-mode-execution-foundation.md`