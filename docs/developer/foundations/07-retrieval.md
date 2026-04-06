# Foundation 07 – Retrieval (Developer)

## Zweck
Findet strukturierte Kandidaten und Evidenz für eine Anfrage, ohne bereits Ranking oder Zielauflösung zu machen.

## Wann nutze ich das?
- Wenn du für einen Mode relevante Dateien, Symbole oder Dokumente finden willst.
- Wenn du Rohkandidaten und Evidenz mit sauberer Provenienz brauchst.
- Wenn du Suche, Ranking und Resolution sauber getrennt halten willst.

## 5-Minuten-Verständnis
- **Input:** `RetrievalRequest` plus `RetrievalContext`.
- **Output:** `RetrievalOutcome`.
- Retrieval beantwortet die Frage: **Welche Quellen oder Kandidaten sind grundsätzlich relevant?**
- Die Foundation entscheidet also noch nicht, **welcher Treffer gewinnt**, sondern baut zuerst eine saubere Ausgangsmenge auf.
- Retrieval macht **noch kein Ranking** im Sinne von Foundation 08.
- Retrieval macht **noch keine Zielauflösung** im Sinne von Foundation 09.

**Wichtig:**
- Diese Foundation sammelt Kandidaten und Evidenz.
- Sie entscheidet nicht, welcher Kandidat „der beste“ ist.
- Sie entscheidet nicht, welches Ziel final aufgelöst wird.

## Einfach erklärt (für Einsteiger)
Stell dir Retrieval wie das erste Einsammeln von Material für eine spätere Entscheidung vor.

Wenn ein Entwickler fragt:
- „Welche Dateien könnten hier wichtig sein?“
- „Welche Dokumente oder Symbole passen überhaupt zu meiner Anfrage?“

… dann ist Foundation 07 der Schritt, der zuerst einmal brauchbares Material zusammenträgt.

Ein einfaches Bild:

1. Eine Anfrage kommt rein.
2. Retrieval schaut in passende Quellen.
3. Es sammelt mögliche Treffer.
4. Es sammelt Belege, warum diese Treffer relevant sein könnten.
5. Es räumt Duplikate auf.
6. Es beachtet Budget- und Policy-Grenzen.
7. Das Ergebnis ist eine saubere Rohmenge für die nächsten Schritte.

```text
Anfrage → Quellen prüfen → Kandidaten + Evidenz sammeln → bereinigtes Ergebnis
```

Wichtig dabei:
- Es wird noch nicht „der Gewinner“ bestimmt.
- Es wird noch kein finales Ziel festgelegt.
- Es wird nichts still aussortiert, ohne dass Herkunft oder Diagnostics sichtbar bleiben.

Ein alltagsnahes Beispiel:
- Die Anfrage erwähnt `workspace` und `scope`.
- Retrieval schaut z. B. in Repo-Dateien oder andere erlaubte Quellen.
- Es findet mehrere passende Stellen.
- Zu jeder Stelle kann es Belege sammeln, etwa Textausschnitte oder Treffer auf Suchsignale.
- Danach können spätere Foundations entscheiden, **welcher Treffer besser ist** oder **welches Ziel wirklich gemeint war**.

Kurz gesagt:
- Foundation 07 findet **mögliche Treffer**.
- Foundation 08 bewertet diese Treffer.
- Foundation 09 löst daraus das konkrete Ziel auf.

## Minimalbeispiel
```python
request = RetrievalRequest(
    query_terms=(
        QueryTermSignal(term="workspace", signal_type="keyword", weight=1.0),
        QueryTermSignal(term="scope", signal_type="concept", weight=0.7),
    ),
    target_scope="repo",
    source_scope=("repo",),
    budget_view=BudgetView(max_candidates=20, max_evidence_items=40),
    policy_context=PolicyContext(allow_external=False),
)

outcome = run_retrieval(request, context)
```

## Kern-API

### `run_retrieval(request, context) -> RetrievalOutcome`
Führt den kompletten Retrieval-Schritt aus.

Einfach gesagt: Die Funktion sammelt erst Treffer und Belege, bereinigt sie anschließend und liefert dann ein nachvollziehbares Retrieval-Ergebnis zurück.

- wählt passende Quellen aus
- erzeugt Kandidaten und Evidenz
- dedupliziert stabil
- begrenzt über Budgetregeln
- liefert Status, Provenienz und Diagnosen

## Wichtige Modelle

### `RetrievalRequest`
Definiert, wonach gesucht werden soll.

Wichtige Felder:
- `query_terms`
- `target_scope`
- `source_scope`
- `budget_view`
- `policy_context`

### `QueryTermSignal`
Ein strukturierter Suchhinweis.

Wichtige Felder:
- `term`
- `signal_type`
- `weight`

**Einfach gemerkt:**
- nicht nur Freitext, sondern bewusst modellierte Retrieval-Signale

### `RetrievalCandidate`
Ein möglicher Treffer aus einer Quelle, also etwas, das später weiter bewertet oder aufgelöst werden kann.

Wichtige Felder:
- `path_or_url`
- `locator`
- `locator_kind`
- `source_type`
- `source_origin`
- `retrieval_source`
- `retrieval_signals`
- `raw_retrieval_score`

### `RetrievalEvidence`
Ein Beleg, warum etwas relevant sein könnte, zum Beispiel ein passender Textausschnitt oder ein Treffer auf ein Suchsignal.

Wichtige Felder:
- Quelle / Locator
- Textausschnitt oder Snippet
- Signalbezug
- Provenienz

### `RetrievalOutcome`
Gesamtergebnis des Retrievals, also die bereinigte Kandidaten- und Evidenzmenge inklusive Status und Diagnostics.

Wichtige Felder:
- `candidates`
- `evidence_items`
- `retrieval_diagnostics`
- `source_usage`
- `status`

### `RetrievalSourceUsage`
Zeigt, wie eine Quelle im Entscheidungsraum behandelt wurde und ob sie wirklich verwendet wurde.

Wichtige Felder:
- `selection_status`
- `attempted`
- `used`

**Einfach gemerkt:**
- `attempted` = Quelle wurde wirklich ausgeführt
- `used` = Quelle hat Kandidaten oder Evidenz geliefert

## Invarianten (sehr wichtig)
- Retrieval liefert strukturierte Kandidaten und Evidenz, kein finales Ziel.
- Provenienz darf nicht verloren gehen.
- Deduplizierung darf Herkunft nicht verstecken.
- Budget-/Policy-Grenzen dürfen nicht zu stillem Abbruch führen.
- `status` ist immer einer von:
  - `ok`
  - `partial`
  - `blocked`
  - `error`
- Nichtdeterministische Quellen müssen sichtbar markiert werden.
- Retrieval bleibt deterministisch: gleicher Input soll zum gleichen Ergebnis führen.

## Typischer Ablauf
```python
selected_sources = _select_sources(request, context)

candidates, evidence = _generate_candidates_and_evidence(
    request=request,
    context=context,
    selected_sources=selected_sources,
)

candidates = _dedupe_candidates(candidates)
evidence = _dedupe_evidence(evidence)

candidates, evidence, diagnostics = _apply_budget_limits(
    request=request,
    candidates=candidates,
    evidence=evidence,
)

# Erst danach liegt die bereinigte Rohmenge für Ranking/Resolution vor.
outcome = RetrievalOutcome(...)
```

## Integration

**Erwartet Input von:**
- Foundation 12 (Repository / Workspace): Workspace- und Locator-Grenzen
- Foundation 04 (Runtime Settings): Retrieval-relevante Limits und Parameter
- Foundation 02 (Orchestration): Kontext für kontrollierten Ablauf

**Schafft die Grundlage für:**
- Foundation 08 (Evidence Ranking): bewertet Kandidaten und Evidenz weiter.
- Foundation 09 (Target Resolution): löst Ziele auf Basis der Kandidaten weiter auf.
- Foundation 10 (Output Contract): kann Diagnosen, Source-Usage und Retrieval-Ergebnisse strukturiert aufnehmen.
- Foundation 11 (Observability): kann Retrieval-Status, Quellenverwendung und Budgeteffekte beobachten.

## Typische Fehler
- Retrieval wird schon wie Ranking behandelt.
- Retrieval versucht bereits finale Zielauflösung zu machen.
- Provenienz geht bei Deduplizierung verloren.
- `source_usage` zeigt nur verwendete Quellen statt des ganzen Entscheidungsraums.
- Budget-Truncation wird still gemacht, ohne Diagnostics.
- Evidence enthält Volltext statt brauchbarer Ausschnitte.
- Retrieval versucht schon zu entscheiden, welches Ziel endgültig gemeint ist.

## Review-Checkliste
- [ ] Retrieval bleibt von Ranking und Resolution getrennt.
- [ ] Provenienz ist für Kandidaten und Evidenz sichtbar.
- [ ] Deduplizierung ist stabil und diagnostizierbar.
- [ ] Budget- und Policy-Effekte sind im Outcome sichtbar.
- [ ] `source_usage` ist nachvollziehbar und semantisch sauber.
- [ ] Nichtdeterministische Quellen werden markiert.
- [ ] Gleiches Input führt zu gleichem Retrieval-Verhalten.

## Referenz
Siehe vollständige Spezifikation:
`docs/foundations/07-retrieval-foundation.md`
