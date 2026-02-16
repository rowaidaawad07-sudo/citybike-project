# CityBike - Bike-Sharing Analytics Platform 🚲

## Projektbeschreibung
Dieses System ist eine Python-basierte Analyseplattform für ein städtisches Fahrradverleihsystem. Es verarbeitet Rohdaten über Fahrten, Stationen und Wartungsarbeiten, um geschäftliche Einblicke zu gewinnen, Daten zu bereinigen und Visualisierungen zu erstellen.

## Features
- **Datenbereinigung:** Automatisches Handling von fehlenden Werten (NaN) und Duplikaten.
- **Vektorisierte Berechnungen:** Effiziente Umsatz- und Distanzberechnungen mittels NumPy.
- **Business-Analysen:** Beantwortung wichtiger Fragen zu Spitzenzeiten, beliebten Routen und Wartungskosten.
- **Visualisierungen:** Automatische Erstellung von Histogrammen, Boxplots und Trend-Diagrammen.

## Verwendete Design Patterns & Prinzipien
- **Factory Pattern:** Zentralisierte Erstellung von Domänenobjekten (Bikes, User) aus Rohdaten.
- **Strategy Pattern:** Flexible Preisberechnungslogik für verschiedene Nutzertypen (Member, Casual).
- **Clean Code & Type Hints:** Konsequente Nutzung von Typisierungen und aussagekräftigen Docstrings für hohe Wartbarkeit.

## Projektstruktur
```text
citybike_project/
├── citybike/
│   ├── models.py        # Domänen-Modelle (Bike, User, Station, Trip)
│   ├── factory.py       # Factory-Logik zur Objekterstellung
│   ├── pricing.py       # Strategy Pattern für Preisberechnungen
│   ├── numerical.py     # NumPy-basierte Berechnungen & Z-Score
│   ├── visualizer.py    # Matplotlib-Logik für Diagramme
│   ├── utils.py         # Validierung, Parsing & Formatierung
│   ├── analyzer.py      # Kern-Logik (BikeShareSystem Klasse)
│   └── data/            # Rohdaten (trips.csv, stations.csv, etc.)
├── output/
│   └── figures/         # Generierte Grafiken (.png)
├── main.py              # Hauptprogramm (Entry Point)
├── .gitignore           # Ausschluss von venv, Cache und Output
├── requirements.txt     # Abhängigkeiten (pandas, numpy, matplotlib)
└── README.md            # Dokumentation & Analyseergebnisse