# Foundation 02 – Orchestration (Developer)

## Zweck
Steuert den Ablauf eines Modes und entscheidet, wann weitergemacht wird und wann der Lauf beendet werden soll.

## Wann nutze ich das?
- Wenn du entscheiden musst, ob ein Mode weiterlaufen soll.
- Wenn du Replan, Recovery, Handoff oder Blockierung sauber modellieren willst.
- Wenn du kontrollierte, nachvollziehbare Steuerlogik statt versteckter Schleifen brauchst.

## 5-Minuten-Verständnis
- **Input:** aktueller `OrchestrationState`, aktuelles Iterationsergebnis und Fortschrittsbewertung.
- **Output:** `OrchestrationDecision`.
- Die Foundation entscheidet:
  - ob weitergelaufen wird (`continue`) oder gestoppt wird (`stop`)
  - **wie** weitergelaufen wird (`control_signal`)
- Sie liefert außerdem:
  - `done_reason`
  - `next_action`
  - diagnostische Informationen
  - Trace-Daten für die nächste Schicht

**Wichtig:**
- Diese Foundation **entscheidet**, sie **führt nicht aus**.
- Die eigentliche Ausführung von Stages passiert in Foundation 01.
- Die eigentliche Ausgabeaufbereitung passiert später in Foundation 10.

## Einfach erklärt (für Einsteiger)
Stell dir Foundation 02 wie einen Verkehrsleiter zwischen den Arbeitsschritten vor.

Foundation 01 kann zwar Stages ausführen, aber Foundation 02 entscheidet, wie der Lauf insgesamt weitergeht.

Ein sehr einfaches Bild:

1. Ein Schritt ist fertig.
2. Jetzt wird angeschaut, was dabei herauskam.
3. Dann wird entschieden:
   - **weiterlaufen**,
   - **neu planen**,
   - **vorübergehend blockieren**,
   - **wieder freigeben**,
   - **an einen anderen Mode übergeben**,
   - oder **ganz stoppen**.

```text
Iterationsergebnis + Fortschritt + Regeln → Entscheidung → nächster Schritt
```

Beispiele:
- Es gibt neue gute Ergebnisse → weitermachen.
- Es gibt mehrfach keinen Fortschritt → neu planen.
- Ein Problem ist vorübergehend blockierend → vorerst blockieren.
- Das Problem ist weg → wieder freigeben und weiterlaufen.
- Budget ist endgültig verbraucht → stoppen.

Wichtig dabei:
- Foundation 02 trifft **keine Fachbewertung von Dateien oder Evidenz**.
- Sie entscheidet **nicht anhand von Bauchgefühl**, sondern über feste Regeln.
- Dadurch wird der Ablauf später gut analysierbar und debugbar.

Kurz gesagt:
- Foundation 01 führt Schritte aus.
- Foundation 02 entscheidet, **wie der Lauf zwischen diesen Schritten gesteuert wird**.

## Minimalbeispiel
```python
decision = decide_orchestration(
    state=current_state,
    iteration=current_iteration,
    progress=progress_evaluation,
)

if decision.decision == "stop":
    return decision.done_reason

if decision.control_signal == "replan":
    ...
```

## Kern-API

### `decide_orchestration(...) -> OrchestrationDecision`
Trifft die zentrale Steuerentscheidung für die aktuelle Iteration.

### `apply_orchestration_step(...)`
- aktualisiert den Orchestration-State
- erzeugt einen deterministischen Orchestration-Trace
- setzt den nächsten Lifecycle-State

### `choose_done_reason(...)`
- bestimmt den finalen Abbruchgrund
- nutzt die fest definierte Priorität der terminalen Gründe

### `evaluate_progress_signal(...)`
- bewertet Fortschritt deterministisch aus expliziten Signalen
- schätzt Fortschritt **nicht frei**, sondern leitet ihn aus Eingaben ab

## Wichtige Modelle

### `OrchestrationDecision`
- `decision`: `continue | stop`
- `control_signal`: `none | replan | recover | handoff | block`
- `done_reason`
- `next_action`
- `diagnostics`

**Einfach gemerkt:**
- `decision` sagt, **ob** es weitergeht.
- `control_signal` sagt, **wie** es weitergeht.

### `OrchestrationState`
- aktueller Lifecycle-Zustand
- Iterationszähler
- No-Progress-Streak
- Handoff-/Loop-Zähler
- Budget-/Policy-bezogene Zustände

### `ProgressEvaluation`
- Fortschrittsbewertung
- deterministisch aus Signalen abgeleitet
- Grundlage für Replan-/Stop-Entscheidungen

### `OrchestrationTraceEntry`
- strukturierter Nachweis eines Schritts
- zeigt, warum ein bestimmter Übergang passiert ist

## Invarianten (sehr wichtig)
- `decision` ist immer entweder `continue` oder `stop`.
- `control_signal` beschreibt die Art der Fortsetzung, nicht die Terminalentscheidung.
- `done_reason` wird nicht frei gesetzt, sondern über feste Priorität bestimmt.
- `blocked` ist ein **recoverable** Zustand und kein stilles Endstadium.
- Es darf keinen Endlos-Replan geben.
- Es darf keinen stillen Endlos-Loop geben.
- Orchestration bleibt deterministisch: gleicher Input soll zum gleichen Entscheidungsverhalten führen.

## Typischer Ablauf
```python
progress = evaluate_progress_signal(...)

decision = decide_orchestration(
    state=state,
    iteration=iteration,
    progress=progress,
)

state, trace_entry = apply_orchestration_step(
    state=state,
    decision=decision,
    iteration=iteration,
)
```

## Integration

**Verwendet:**
- Foundation 01 (Mode Execution)

**Erwartet Input von:**
- Foundation 07 (Retrieval)
- Foundation 08 (Evidence Ranking)
- Foundation 09 (Target Resolution)

**Schafft die Grundlage für:**
- Foundation 10 (Output Contract): übernimmt später strukturierte Entscheidungen, `done_reason` und Trace-nahe Ergebnisse.
- Foundation 11 (Observability): kann Decision-, Block-, Replan- und Trace-Daten beobachten und auswerten.

## Typische Fehler
- `decision` und `control_signal` werden verwechselt.
- Replan wird ohne Limit oder Anti-Loop-Schutz ausgelöst.
- `blocked` wird nie verwendet oder nie wieder verlassen.
- `done_reason` wird frei gesetzt statt über Priorität bestimmt.
- Fortschritt wird frei geschätzt statt aus Signalen abgeleitet.
- Handoff wird wie normales `continue` behandelt, ohne die Übergabesemantik mitzudenken.

## Review-Checkliste
- [ ] Die Entscheidung ist deterministisch.
- [ ] Die Done-Reason-Priorität wird eingehalten.
- [ ] Replan hat einen Anti-Loop-Mechanismus.
- [ ] `blocked` ist erreichbar und wieder verlassbar.
- [ ] Der Trace ist vollständig und nachvollziehbar.
- [ ] Es gibt keine versteckte Steuerlogik außerhalb von `decide_orchestration(...)`.
- [ ] `decision` und `control_signal` sind fachlich sauber getrennt.

## Referenz
Siehe vollständige Spezifikation:
`docs/foundations/02-orchestration-foundation.md`