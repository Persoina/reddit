### Rolle
Du bist ein erfahrener Python-Entwickler und OSINT-Analyst. Dein Ziel ist es, einen robusten, gut dokumentierten und sofort lauffähigen Code zu liefern.

### Aufgabe
Schreibe ein vollständiges Python-Programm, das dauerhaft (quasi in Echtzeit) neue Reddit-Posts **und** -Kommentare überwacht, die mit rechtsextremen oder rechtspopulistischen Gruppen in Deutschland zusammenhängen.  
Die Anwendung soll eine Live-Übersicht (“Monitoring-Dashboard”) erzeugen, in der folgende Informationen fortlaufend aktualisiert werden:

1. **Titel / Kommentarausschnitt**  
2. **Subreddit**  
3. **Autor**  
4. **Zeitstempel (UTC & lokale Zeit)**  
5. **Score**  
6. **Erkannte Schlagworte / Gruppennamen**  
7. **Direktlink zum Beitrag / Kommentar**

### Technische Anforderungen
1. **Reddit-API**  
   * Nutze `asyncpraw` (asynchron, Python ≥ 3.9).  
   * Lies `client_id`, `client_secret`, `user_agent` sicher aus einer `.env`-Datei (nutze `python-dotenv`).  
   * Verarbeite sowohl _submissions_ als auch _comments_.  
   * Poll-Intervall max. 30 Sek.; gehe schonend mit Rate-Limits um.

2. **Zielquelle definieren**  
   * Verwende eine **Liste von Subreddits** (`RIGHT_WING_SUBS`) **und/oder** eine **Keyword-Liste** (`RIGHT_WING_TERMS`) – beide in einer externen JSON-Datei (`config.json`); lade sie beim Start.  
   * Beispiel-Subreddits (unvollständig, nur als Platzhalter – bitte nach eigener Recherche ergänzen oder anpassen):  
     * `r/Deutschland`  
     * `r/de_AltRight`  
   * Beispiel-Keywords: `"AfD"`, `"Identitäre Bewegung"`, `"Pegida"`, `"Querdenker"` …

3. **Datenhaltung**  
   * Speichere jede erkannte Nachricht zeilenweise in eine **SQLite-DB** (`sqlite3`) mit passenden Indizes für schnelles Filtern.  
   * Lege außerdem eine **CSV-Sicherung** pro Tag an (Dateiname `YYYY-MM-DD_monitoring.csv`).

4. **Live-Dashboard**  
   * Implementiere ein kleines **Streamlit**-Dashboard (`streamlit run app.py`):  
     * Auto-Refresh alle 10 Sek.  
     * Tabellenansicht mit den Feldern (1) – (7).  
     * Text-Input-Feld zum dynamischen Filtern (Suche).  
     * Badge/Counter für neue Treffer seit letztem Refresh.  
     * Optional: kleine Zeit-Serie “Treffer pro Stunde” mit `matplotlib`.

5. **Code-Qualität**  
   * Nutze `asyncio` & `asyncio.create_task` für gleichzeitige Streams (Submissions vs. Comments).  
   * Führe eine zentrale Fehler-/Retry-Logik ein, um Netzwerk-Glitches abzufangen.  
   * Strikte Typisierung (`from __future__ import annotations`, plus `mypy`-kompatible `typing`).  
   * Struktur: `src/`-Modul, eigenständige `main.py`, `dashboard.py`, `db.py`, `config.py`.  
   * Kommentiere klar (Docstrings, Typ-Hints) und halte dich an PEP 8.

6. **Nutzungshinweise (README-Abschnitt)**  
   * Installations-Schritte (`pip install -r requirements.txt`).  
   * Wie man eigene Subreddit- oder Keyword-Listen erweitert.  
   * Hinweise auf Reddit-Nutzungsbedingungen & deutsches Recht (vgl. DSGVO, §86a StGB).  
   * Sicherheit: niemals Inhalte automatisch weiterverbreiten.

### Erwartetes Ergebnis
* Ein **vollständiges Projektverzeichnis** mit:
  * `requirements.txt`  
  * `config.json` (Beispiel)  
  * `.env.example`  
  * `src/…` (alle Module)  
  * `app.py` (Streamlit-Dashboard)  
  * `README.md`
* Code, der nach Ausfüllen der `.env` und `config.json` sofort startet und das Dashboard unter `localhost:8501` verfügbar macht.

### Lieferformat
Antworte ausschließlich mit Codeblöcken (kein zusätzlicher Fließtext), beginnend bei Projekt-Root.  
Füge am Anfang eine kurze ASCII-Baumübersicht der Struktur ein, danach folgen die Dateien:

