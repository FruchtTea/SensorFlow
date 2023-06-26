# SensorFlow

![Logo](static/visual/banner.png)

## Über das Projekt

SensorFlow ist ein Schulprojekt im Bereich des Internet of Things und soll über Sensoren empfangene Dateien visualisieren.

## Getting Started

Um loslegen zu können, muss zuerst [python3](https://www.python.org/) installiert sein. Zusätzlich werden im Projekt die folgenden pip-Abhändigkeiten genutzt:

- flask
- folium
- paho-mqtt

Diese können folgendermaßen installiert werden:

```cmd
pip3 install flask folium phao-mqqt
```

Um die Anwendung richtig benutzen zu können wir ein Datenübertragendes Gerät (siehe [sender](#)) benötigt.

Wenn diese installiert sind, kann das Projekt mit 

```cmd
python main.py
``` 

gestartet werden. Im Anschluss kann die Anwendung im Browser unter [localhost:5000](http://localhost:5000) erreicht werden.