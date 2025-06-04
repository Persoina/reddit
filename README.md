# Reddit Right-Wing Monitor

Dieses Projekt überwacht Reddit-Beiträge und Kommentare auf Erwähnungen rechtsextremer oder rechtspopulistischer Gruppen in Deutschland. Gefundene Treffer werden in einer SQLite-Datenbank gespeichert und können über ein Streamlit-Dashboard eingesehen werden.

## Installation

1. Repository klonen und ins Verzeichnis wechseln.
2. Python >= 3.9 installieren.
3. Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

4. `.env` auf Basis von `.env.example` anlegen und Reddit-API-Zugangsdaten eintragen.
5. `config.json` anpassen und gewünschte Subreddits bzw. Schlagworte hinterlegen.

## Nutzung

### Monitoring starten

```bash
python -m src.main
```

### Dashboard aufrufen

```bash
streamlit run app.py
```

Das Dashboard aktualisiert sich alle 10 Sekunden und zeigt neue Treffer seit dem letzten Refresh an. Ein Suchfeld erlaubt das Filtern der Ergebnisse.

## Eigene Listen erweitern

In `config.json` können beliebige Subreddits und Suchbegriffe ergänzt werden. Beispiel:

```json
{
  "RIGHT_WING_SUBS": ["Deutschland", "de_AltRight"],
  "RIGHT_WING_TERMS": ["AfD", "Identitäre Bewegung", "Pegida", "Querdenker"]
}
```

## Rechtliche Hinweise

* Die Nutzung der Reddit-API unterliegt den [Reddit Terms of Service](https://www.redditinc.com/policies/data-api-terms). Beachten Sie insbesondere Rate-Limits und Datenschutz.
* In Deutschland sind Inhalte mit verfassungsfeindlichen Symbolen oder Propaganda (§86a StGB) strafbar. Dieses Projekt dient ausschließlich der Beobachtung und Dokumentation.
* Inhalte sollten niemals automatisiert weiterverbreitet oder veröffentlicht werden.

## Projektstruktur

- `app.py` – Streamlit-Dashboard
- `src/main.py` – Startpunkt für das Monitoring
- `src/db.py` – SQLite- und CSV-Sicherung
- `src/config.py` – Laden von `.env` und `config.json`

Viel Erfolg beim Monitoring!
