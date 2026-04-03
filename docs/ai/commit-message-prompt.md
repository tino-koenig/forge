# Commit Message Generation Prompt (DE)

Erzeuge eine präzise Git-Commit-Message aus den aktuellen Änderungen.

Regeln:
- Antworte auf Deutsch.
- Nutze Conventional Commits im Format: type(scope): summary
- Erlaubte Typen: feat, fix, refactor, docs, test, chore, ci, perf.
- Summary im Imperativ, ohne Punkt am Ende, maximal 72 Zeichen.
- Kein Marketing, keine Füllwörter, keine Emojis.
- Keine erfundenen Inhalte; nur tatsächlich geänderte Punkte beschreiben.
- Falls mehrere sinnvolle Änderungen enthalten sind, füge unter der Titelzeile kurze Bullet-Points hinzu.
- Bullet-Points sollen konkret sein (Dateien/Bereiche/Wirkung), jeweils eine Zeile.
- Breche bei Unsicherheit nicht in Spekulation aus: lieber neutral und knapp formulieren.
- Verwende niemals Backtick-Zeichen oder Codeblöcke im Ergebnis.

Branch-/Ticket-Regel:
- Falls aus dem Branch-Namen eine Ticket-ID erkennbar ist (z. B. Issue #123), hänge sie am Ende der Summary in eckigen Klammern an.
- Beispiel: feat(cli): erweitere review ausgabe [#123]

Ausgabeformat:
1. Erste Zeile: Commit-Titel
2. Optional leerzeile
3. Optional Bullet-Points mit - 

Beispiele:
- feat(index): ergänze priorisierte dateiauswahl für query
- fix(cli): verhindere profil-override in read-only modi
- docs(features): präzisiere effektgrenzen für capability model

---

# Commit Message Generation Prompt (EN)

Generate a precise Git commit message from the current changes.

Rules:
- Reply in English.
- Use Conventional Commits in this format: type(scope): summary
- Allowed types: feat, fix, refactor, docs, test, chore, ci, perf.
- Write summary in imperative mood, no trailing period, max 72 characters.
- No marketing language, no filler words, no emojis.
- Do not invent facts; describe only actual changes.
- If multiple meaningful changes are included, add short bullet points below the title.
- Bullet points must be concrete (files/areas/effect), one line each.
- If uncertain, stay neutral and concise instead of speculating.
- Never use backtick characters or code fences in the output.

Branch/ticket rule:
- If a ticket ID is visible in the branch name (for example issue #123), append it to the summary in square brackets.
- Example: feat(cli): extend review output [#123]

Output format:
1. First line: commit title
2. Optional blank line
3. Optional bullet points with - 

Examples:
- feat(index): add prioritized file selection for query
- fix(cli): prevent profile override in read-only modes
- docs(features): clarify capability effect boundaries
