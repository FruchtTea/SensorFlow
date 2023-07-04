from flask import Flask, render_template
import paho.mqtt.client as mqtt
import folium, time, threading, json

gruppenname = "sensorik"
id = "IoTinformatikschulbuch"

client_name = id + gruppenname + "server"
client_telemetry_topic = id + gruppenname + "/telemetry"

# MQTT Verbindung aufbauen
def subscribe_to_mqtt():
    global mqtt_client

    mqtt_client = mqtt.Client(client_name)
    mqtt_client.connect("test.mosquitto.org")
    mqtt_client.loop_start()
    print("MQTT connected")

    mqtt_client.subscribe(client_telemetry_topic)
    mqtt_client.on_message = verarbeite_telemetry


# Wird aufgerufen sobald eine neue Nachricht empfangen wurde
def verarbeite_telemetry(client, nutzerdaten, nachricht):
    payload = nachricht.payload.decode()
    print(payload)

    payload_message = payload.split("=")

    # Dictionary für die möglichen MQTT Inputs
    mapping = {
        "lat": "Breitengrad",
        "long": "Laegengrad",
        "temp": "Temperatur",
        "humid": "Luftfeuchtigkeit"
}

    # Überprüfen, ob der Schlüssel in der Zuordnung vorhanden ist
    if payload_message[0] in mapping:
        key = mapping[payload_message[0]]
        value = float(payload_message[1])
        data = {key: value}
        json_data = json.dumps(data)
        with open("data.json", "w") as json_file:
            json_file.write(json_data)


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def render_main_page():
    return render_template("index.html")


@app.route("/geolocator")
def render_geolocator_page():
    return render_template("geolocator.html")


@app.route("/render-geolocation-page")
def render_karte():
    
    # JSON-Datei öffnen und Daten laden
    with open("data.json", "r") as json_file:
        json_data = json.load(json_file)

    # Den Wert aus der JSON-Datei auslesen
    lat = json_data["Laengengrad"]
    long = json_data["Breitengrad"]

    map = folium.Map(
        location=[lat, long], 
        zoom_start=12, 
        tiles="Stamen Terrain")

    folium.Marker(
        location=[lat, long],
        popup="<b>Du befindest dich hier!</b>",
        tooltip="Klicke, um mehr zu erfahren!",
        icon=folium.Icon(color="red"),
    ).add_to(map)

    return map._repr_html_()


@app.route("/raumklima")
def render_klima_page():

    # JSON-Datei öffnen und Daten laden
    with open("data.json", "r") as json_file:
        json_data = json.load(json_file)

    # Den Wert aus der JSON-Datei auslesen
    temp = json_data["Temperatur"]
    humid = json_data["Luftfeuchtigkeit"]

    return render_template("raumklima.html", show_temperature=temp, show_humidity=humid)


@app.route("/ueber-uns")
def render_about_us_page():
    return render_template("ueber-uns.html")


if __name__ == "__main__":
    t1 = threading.Thread(target=subscribe_to_mqtt)
    t1.start()

    app.run(debug=True)

while True:
    try:
        time.sleep(0.1)
    except IOError:
        print("Error")