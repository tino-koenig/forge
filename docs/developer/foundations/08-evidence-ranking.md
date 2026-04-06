# Foundation 08 – Evidence Ranking (Developer)

## Zweck
Bewertet Retrieval-Kandidaten und Evidenz nachvollziehbar und deterministisch, ohne bereits Zielauflösung durchzuführen.

## Wann nutze ich das?
- Wenn du mehrere Retrieval-Kandidaten vergleichbar machen willst.
- Wenn du nachvollziehbar entscheiden willst, **welche Kandidaten stärker sind als andere**.
- Wenn du Explainability und reproduzierbares Ranking brauchst.

## 5-Minuten-Verständnis
- **Input:** `RetrievalOutcome` + `RankingRequest` + `RankingContext`
- **Output:** `RankingOutcome`
- Ranking beantwortet die Frage: **Wie gut ist jeder Kandidat im Vergleich zu den anderen?**
- Die Foundation entscheidet also nicht direkt, **welches Ziel am Ende genommen wird**, sondern baut zuerst eine nachvollziehbare Bewertungsreihenfolge auf.
- Ranking nutzt **explizite Score-Komponenten**, keine versteckten Heuristiken.
- Welche Kriterien überhaupt zählen, wird über die `RankingPolicy` festgelegt.
- Ranking löst noch kein finales Ziel auf (das macht Foundation 09).

**Wichtig:**
- Ranking bewertet nur, es entscheidet nicht final.
- Ranking ist deterministisch: gleicher Input → gleiche Reihenfolge.

## Einfach erklärt (für Einsteiger)
Stell dir Ranking wie eine faire und nachvollziehbare Bewertungsliste vor.

Retrieval hat vorher schon mehrere mögliche Treffer gefunden. Jetzt kommt Foundation 08 und beantwortet nicht mehr die Frage:
- „Was könnte passen?“

sondern die Frage:
- „Was passt **wahrscheinlich besser** als etwas anderes?“

Ein einfaches Bild:

1. Es gibt mehrere Kandidaten.
2. Jeder Kandidat bekommt Punkte aus klaren Kriterien.
3. Diese Punkte werden zusammengeführt.
4. Danach werden die Kandidaten sortiert.

```text
Kandidaten → Punkte berechnen → vergleichen → sortieren
```

Wichtig dabei:
- Ranking ist **keine magische Entscheidung**.
- Jeder Kandidat bekommt seine Bewertung aus sichtbaren Bausteinen.
- Man kann später nachvollziehen, warum Kandidat A vor Kandidat B steht.

Ein alltagsnahes Beispiel:
- Retrieval hat drei Dateien gefunden.
- Eine Datei hat viele passende Evidenzstellen.
- Eine andere Datei hat weniger Evidenz, aber einen besseren direkten Retrieval-Score.
- Ranking führt diese Informationen zusammen und baut daraus eine sortierte Reihenfolge.

Ganz wichtig:
- Foundation 08 sagt noch nicht endgültig: „Das ist das Ziel.“
- Sie sagt: „Von diesen Kandidaten sieht dieser hier aktuell am stärksten aus.“
- Die eigentliche Zielauflösung macht danach Foundation 09.

Kurz gesagt:
- Foundation 07 findet mögliche Treffer.
- Foundation 08 bewertet diese Treffer.
- Foundation 09 entscheidet, welches konkrete Ziel daraus wird.

## Minimalbeispiel
```python
outcome = rank_evidence(
    request=RankingRequest(enable_rerank=False),
    retrieval_outcome=retrieval_outcome,
    context=ranking_context,
)

for candidate in outcome.candidates:
    print(candidate.locator, candidate.score_total)
```

## Kern-API

### `rank_evidence(request, retrieval_outcome, context) -> RankingOutcome`
Führt den kompletten Ranking-Schritt aus.

Einfach gesagt: Die Funktion nimmt die Kandidaten aus dem Retrieval, berechnet für jeden nachvollziehbare Score-Bausteine und liefert eine sortierte, erklärbare Reihenfolge zurück.

- berechnet Score-Komponenten
- aggregiert Scores
- sortiert deterministisch
- wendet Tie-break-Regeln an
- optional: deklarierter Rerank

## Wichtige Modelle

### `RankingRequest`
Steuert den Ranking-Lauf, zum Beispiel ob ein optionaler Rerank-Schritt aktiviert sein soll.

### `RankingPolicy`
Definiert die Komponenten und Gewichte des Rankings.
- legt fest, **welche Kriterien überhaupt in das Ranking eingehen**
- hat `policy_id` und `policy_version`
- wird **nicht von der Foundation selbst gewählt**, sondern vom aufrufenden Code bereitgestellt

### `ScoreComponent`
Ein einzelner Beitrag zum Gesamtscore eines Kandidaten.

Beispiele:
- Retrieval-Score
- Anzahl oder Qualität von Evidenz
- Term-Abdeckung
- Determinismus der Quelle

### `RankedCandidate`
Ein bewerteter Kandidat inklusive Gesamtscore, Score-Bestandteilen und Status.

Wichtige Felder:
- `locator`
- `score_total`
- `score_components`
- `status`
- `policy_id`

### `RankingOutcome`
Gesamtergebnis des Rankings, also die geordnete Kandidatenliste plus Policy- und Diagnostic-Informationen.

Wichtige Felder:
- `candidates`
- `policy_id`
- `policy_version`
- `diagnostics`

## Invarianten (sehr wichtig)
- Ranking nutzt nur explizite Score-Komponenten.
- `score_total` ist ein **aggregierter Wert**, kein Wahrheitswert.
- Ranking ist deterministisch.
- Tie-break ist stabil.
- Rerank ist optional und sichtbar.
- Ranking ersetzt nicht Retrieval und nicht Resolution.

## Typischer Ablauf
```python
components = _compute_score_components(...)

score = _aggregate_score(components)

ordered = _apply_tie_break(candidates)

# Danach liegt eine nachvollziehbar sortierte Kandidatenliste vor.
outcome = RankingOutcome(...)
```

## Integration

**Erwartet Input von:**
- Foundation 07 (Retrieval): Kandidaten und Evidenz

**Schafft die Grundlage für:**
- Foundation 09 (Target Resolution): wählt aus den bestbewerteten Kandidaten
- Foundation 10 (Output Contract): kann Ranking-Ergebnisse darstellen
- Foundation 11 (Observability): kann Ranking-Entscheidungen und Scores analysieren

## Typische Fehler
- Ranking vermischt mit Retrieval-Logik
- Ranking trifft finale Entscheidungen statt nur Bewertung
- Score-Komponenten sind implizit oder nicht nachvollziehbar
- Tie-break ist nicht stabil
- Rerank überschreibt still das ursprüngliche Ranking
- Ranking wird so gebaut, dass der eigentliche Auflösungsschritt aus Foundation 09 still vorweggenommen wird.

## Review-Checkliste
- [ ] Ranking nutzt explizite Score-Komponenten
- [ ] Aggregation ist nachvollziehbar
- [ ] Tie-break ist deterministisch
- [ ] `policy_id` und `policy_version` sind sichtbar
- [ ] Rerank ist optional und transparent
- [ ] keine versteckte Logik außerhalb der Komponenten

## Referenz
Siehe vollständige Spezifikation:
`docs/foundations/08-evidence-ranking-foundation.md`