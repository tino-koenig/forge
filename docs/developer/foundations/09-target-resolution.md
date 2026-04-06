# Foundation 09 – Target Resolution (Developer)

## Zweck
Löst ein konkretes Ziel (Datei, Symbol, Verzeichnis) aus einer Menge von Kandidaten deterministisch und nachvollziehbar auf.

## Wann nutze ich das?
- Wenn du aus mehreren Kandidaten ein konkretes Ziel bestimmen willst.
- Wenn du Ambiguität sichtbar behandeln musst.
- Wenn du strukturierte Zielauflösung ohne versteckte Heuristik brauchst.

## 5-Minuten-Verständnis
- **Input:** Kandidaten (z. B. aus Ranking) + `TargetRequest`
- **Output:** `TargetResolutionResult`
- Resolution beantwortet die Frage: **Welches Ziel ist gemeint?**
- Die Foundation entscheidet also nicht mehr nur, **was gut aussieht**, sondern welches konkrete Ziel am Ende aus der Kandidatenmenge gewählt oder als mehrdeutig ausgewiesen wird.
- Sie nutzt priorisierte Regeln und transparente Fallbacks.

**Wichtig:**
- Diese Foundation trifft die finale Zielentscheidung.
- Sie erzeugt **keine neuen Kandidaten**.
- Sie nutzt keine versteckte Suche.

## Einfach erklärt (für Einsteiger)
Stell dir Foundation 09 wie den letzten klaren Auswahlschritt vor.

Vorher ist bereits einiges passiert:
- Foundation 07 hat mögliche Treffer gesammelt.
- Foundation 08 hat diese Treffer bewertet und sortiert.

Jetzt kommt Foundation 09 und beantwortet die Frage:
- „Welches konkrete Ziel ist hier wirklich gemeint?“

Ein einfaches Bild:

1. Es gibt mehrere Kandidaten.
2. Diese Kandidaten werden in eine stabile Reihenfolge gebracht.
3. Dann wird geprüft, ob ein Kandidat klar genug ist.
4. Wenn ja, wird das Ziel aufgelöst.
5. Wenn nein, wird Ambiguität sichtbar gemacht.
6. Wenn nur ein Fallback greift, bleibt auch das sichtbar.

```text
Kandidaten → prüfen → Ziel auswählen oder Ambiguität ausgeben
```

Ein alltagsnahes Beispiel:
- Ranking hat mehrere Treffer zu `workspace` geliefert.
- Zwei davon sehen ähnlich gut aus.
- Resolution prüft jetzt nicht noch einmal „frei“, sondern arbeitet mit klaren Regeln.
- Wenn einer klar führt, wird er als Ziel zurückgegeben.
- Wenn mehrere Kandidaten gleich relevant bleiben, wird das als Ambiguität ausgegeben statt still zu raten.

Wichtig dabei:
- Foundation 09 erzeugt **keine neuen Kandidaten**.
- Foundation 09 macht **kein neues Ranking**.
- Foundation 09 trifft die Zielentscheidung transparent und diagnostizierbar.

Kurz gesagt:
- Foundation 07 findet mögliche Treffer.
- Foundation 08 bewertet diese Treffer.
- Foundation 09 entscheidet, welches konkrete Ziel daraus wird.

## Minimalbeispiel
```python
result = resolve_target(
    request=target_request,
    context=resolution_context,
)

if result.resolution_status == "ambiguous":
    print(result.ambiguity_top_k)
```

## Kern-API

### `resolve_target(request, context) -> TargetResolutionResult`
Führt die Zielauflösung durch.

Einfach gesagt: Die Funktion nimmt die vorhandenen Kandidaten, wendet die Resolution-Regeln an und liefert entweder ein klares Ziel oder eine sichtbare Ambiguität zurück.

### `resolve_from_run_reference(...)`
Löst Ziele aus vorherigen Runs auf (Handoff).

### `validate_transition(...)`
Prüft, ob ein Übergang zwischen Modes erlaubt ist.

## Wichtige Modelle

### `TargetRequest`
Beschreibt, was aufgelöst werden soll und mit welchen Hinweisen oder Einschränkungen die Auflösung arbeiten darf.

### `TargetCandidate`
Ein möglicher Zielkandidat, der aus vorherigen Schritten stammt und jetzt für die Auflösung geprüft wird.

### `TargetResolutionResult`
Ergebnis der Auflösung.

Wichtige Felder:
- `resolved_target`
- `resolved_kind`
- `resolution_status`
- `resolution_source`
- `resolution_strategy`
- `ambiguity_top_k`
- `diagnostics`

### `TransitionDecision`
Beschreibt, ob ein Übergang zwischen Modes erlaubt ist oder blockiert werden muss.

## Invarianten (sehr wichtig)
- Resolution ist deterministisch.
- Ambiguität darf nicht versteckt werden.
- Fallback muss sichtbar sein.
- Zielart (`resolved_kind`) ist klar von Herkunft (`resolution_source`) getrennt.

## Typischer Ablauf
```python
ordered = order_target_candidates_for_resolution(candidates, policy)

result = resolve_target(request, context)

# Danach liegt entweder ein konkretes Ziel oder eine sichtbare Ambiguität vor.
```

## Integration

**Erwartet Input von:**
- Foundation 07 (Retrieval)
- Foundation 08 (Ranking)

**Schafft die Grundlage für:**
- Foundation 10 (Output Contract)
- Foundation 11 (Observability)

## Typische Fehler
- Ambiguität wird still aufgelöst.
- Resolution mischt sich mit Retrieval oder Ranking.
- Fallback passiert ohne Diagnostics.
- Herkunft (`resolution_source`) wird mit Zielart verwechselt.
- Resolution trifft Best-Guess-Entscheidungen, obwohl Ambiguität sichtbar gemacht werden müsste.
- `resolved_target`, `resolved_kind` und `resolution_source` werden nicht sauber auseinandergehalten.

## Review-Checkliste
- [ ] Resolution ist deterministisch.
- [ ] Ambiguität wird sichtbar gemacht.
- [ ] Fallback ist diagnostizierbar.
- [ ] Zielart und Herkunft sind sauber getrennt.
- [ ] `resolved_target`, `resolved_kind` und `resolution_source` sind sauber und konsistent belegt.

## Referenz
Siehe vollständige Spezifikation:
`docs/foundations/09-target-resolution-foundation.md`