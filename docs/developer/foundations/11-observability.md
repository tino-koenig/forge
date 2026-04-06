# Foundation 11 – Observability (Developer)

## Zweck
Erzeugt strukturierte, nachvollziehbare Ereignisse (Events), damit ein Run vollständig analysierbar und debugbar ist.

## Wann nutze ich das?
- Wenn du verstehen willst, warum ein Mode ein bestimmtes Verhalten zeigt.
- Wenn du Debugging, Monitoring oder Analyse brauchst.
- Wenn du Entscheidungen, Budgets oder Policy-Verhalten nachvollziehen willst.

## 5-Minuten-Verständnis
- **Input:** Events aus Execution, Orchestration und anderen Foundations
- **Output:** strukturierte Event-Streams + Run Summary
- Observability beantwortet die Frage: **Was ist passiert und warum?**
- Die Foundation entscheidet also nicht fachlich, **was richtig war**, sondern macht sichtbar, **was tatsächlich passiert ist und wie es zusammenhängt**.

## Einfach erklärt (für Einsteiger)
Stell dir Foundation 11 wie das strukturierte Gedächtnis eines Runs vor.

Während Forge arbeitet, passieren viele Dinge:
- ein Run startet,
- eine Stage beginnt,
- eine Entscheidung wird getroffen,
- ein Budget wird erreicht,
- etwas wird blockiert,
- der Run endet.

Wenn man diese Dinge nur als lose Textlogs hinschreibt, kann man später vieles schwer nachvollziehen.
Foundation 11 sorgt deshalb dafür, dass solche Ereignisse als **strukturierte Events** festgehalten werden.

Ein einfaches Bild:

1. Im System passiert etwas.
2. Dazu wird ein Event erzeugt.
3. Dieses Event wird einem Run zugeordnet.
4. Später kann man alle Events eines Runs zusammen ansehen.
5. Daraus lässt sich verstehen, was passiert ist und warum.

```text
System läuft → Events entstehen → Events werden gesammelt → Run wird analysierbar
```

Ein alltagsnahes Beispiel:
- Eine Retrieval-Stage startet.
- Danach endet sie.
- Orchestration entscheidet auf `replan`.
- Später wird ein Budget-Limit erreicht.
- Am Ende endet der Run mit einem bestimmten `done_reason`.

Mit Foundation 11 kann man diese Kette später sauber nachvollziehen, statt nur einzelne lose Logzeilen zu haben.

Wichtig dabei:
- Events sind keine freien Texte, sondern strukturierte Datensätze.
- Alle wichtigen Ereignisse hängen an `run_id` und `trace_id`.
- Die Run Summary wird aus den vorhandenen Events abgeleitet.

Kurz gesagt:
- Foundation 11 merkt sich nicht einfach „irgendwelche Logs“.
- Foundation 11 baut eine nachvollziehbare Ereignisspur des gesamten Runs auf.

## Minimalbeispiel
```python
run_id = obs_start_run(context)

obs_log_event(obs_make_event(
    event_type="stage_started",
    payload={"stage": "retrieve"},
))

obs_end_run(run_id, summary={"done_reason": "sufficient_evidence"})
```

## Kern-API

### `obs_start_run(context)`
- startet einen neuen Run
- erzeugt `run_id` und `trace_id`

### `obs_log_event(event)`
- fügt ein Event zum Run hinzu
- hier landet jedes strukturierte Ereignis, das später für Debugging, Analyse oder Summary wichtig sein kann

### `obs_end_run(run_id, summary)`
- beendet den Run
- erzeugt Summary aus Events
- die Summary soll nicht frei erfunden werden, sondern aus den bis dahin vorhandenen Events ableitbar bleiben

### `obs_make_event(...)`
- erzeugt ein strukturiertes Event

## Wichtige Modelle

### `ObsEvent`
Ein einzelnes strukturiertes Ereignis innerhalb eines Runs.

Wichtige Felder:
- `event_type`
- `timestamp`
- `run_id`
- `payload`
- `redaction_status`

### `ObsContext`
Kontext eines Runs, also die grundlegenden Informationen, mit denen neue Events korrekt einem Run zugeordnet werden können.

### `ObsRunSummary`
Zusammengefasste Sicht eines Runs, die aus den vorhandenen Events abgeleitet wird.

## Event-Typen (Beispiele)
- `run_started`
- `stage_started`
- `stage_completed`
- `decision_made`
- `policy_blocked`
- `budget_exhausted`
- `action_started`

## Invarianten (sehr wichtig)
- Events sind strukturiert, nicht freie Texte.
- Pflichtfelder sind immer gesetzt (`run_id`, `event_type`, `timestamp`).
- `payload` ist ein Mapping.
- Redaction ist explizit (`not_needed|applied|blocked|failed`).
- Events müssen deterministisch auswertbar und korrelierbar sein.
- Run Summary wird aus Events berechnet, nicht separat frei gepflegt.
- Korrelation über `run_id` und `trace_id` darf nicht verloren gehen.

## Typischer Ablauf
```python
run_id = obs_start_run(context)

obs_log_event(...)
obs_log_event(...)

# Die Summary entsteht aus dem Event-Verlauf des Runs.
summary = obs_end_run(run_id)
```

## Integration

**Erwartet Input von:**
- Foundation 01 (Execution)
- Foundation 02 (Orchestration)

**Schafft die Grundlage für:**
- Debugging
- Monitoring
- Analyse
- spätere Visualisierung
- nachvollziehbare Auswertung von Entscheidungen, Budget- und Policy-Verhalten

## Typische Fehler
- Freitext-Logs statt strukturierter Events.
- Fehlende Pflichtfelder.
- Events ohne `run_id`.
- Redaction wird ignoriert.
- Summary wird manuell erzeugt statt aus Events.
- Events werden ohne saubere Korrelation erzeugt.
- Summary oder Abschlussgründe werden unabhängig von den tatsächlichen Events konstruiert.

## Review-Checkliste
- [ ] Events sind strukturiert und nicht bloß Freitext.
- [ ] Pflichtfelder sind vorhanden.
- [ ] Payload ist ein Mapping.
- [ ] Redaction ist korrekt gesetzt.
- [ ] Summary wird aus Events abgeleitet.
- [ ] Korrelation über `run_id` und `trace_id` funktioniert.
- [ ] Event-Typen und Payloads sind für spätere Analyse brauchbar.

## Referenz
Siehe vollständige Spezifikation:
`docs/foundations/11-observability-foundation.md`