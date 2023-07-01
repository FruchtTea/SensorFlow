from flask import Flask, render_template
import folium, time, threading
import paho.mqtt.client as mqtt

################## HIER STARTET MQTT LOGIK ##################
gruppenname = "sensorik"
id = "IoTinformatikschulbuch"

# Eindeutiger Name mit dem sich beim MQTT Broker angemeldet wird
client_name = id + gruppenname + "server"

# Kanal auf der das Gerät Informationen empfangen wird
client_telemetry_topic = id + gruppenname + "/telemetry"

# Erzeugen des MQTT-Client Objekts und verbinden mit dem MQTT-Broker
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect("test.mosquitto.org")
mqtt_client.loop_start()
print("MQTT connected")


# Methode wird aufgerufen, sobald eine neue Nachricht empfangen wurde
def verarbeite_telemetry(client, nutzerdaten, nachricht):
    payload = nachricht.payload.decode()
    print("Nachricht empfangen: ", payload)

    global temperatur_value
    temperatur_value = payload


# Abonniert die oben gegebene Topic
mqtt_client.subscribe(client_telemetry_topic)

# Legt fest, dass die Methode verarbeite_telemetry aufgerufen werden soll, wenn eine Nachricht eintrifft
mqtt_client.on_message = verarbeite_telemetry


################## HIER STARTET DER FLASK SERVER ##################

app = Flask(__name__)

@app.route("/")
def render_main_page():
    return render_template("index.html")


@app.route("/geolocator")
def render_geolocator_page():
    return render_template("geolocator.html")


@app.route("/render-geolocation-page")
def render_karte():
    global lat
    global long 

    map = folium.Map(location=[lat, long], zoom_start=12, tiles="Stamen Terrain")

    folium.Marker(
        location=[lat, long],
        popup="<b>Du befindest dich hier!</b>",
        tooltip="Klicke, um mehr zu erfahren!",
        icon=folium.Icon(color="red"),
    ).add_to(map)

    return map._repr_html_()


@app.route("/raumklima")
def render_temperatur_page():
    global temperaur_value

    return render_template("raumklima.html", show_temperature=temperatur_value, show_humidity=1)


@app.route("/ueber-uns")
def render_about_us_page():
    return render_template("ueber-uns.html")


def startserver():
    app.run()


if __name__ == "__main__":
    t1 = threading.Thread(target=startserver)
    t1.start()

# while True:
#     try:
#         # Warte eine halbe Sekunde für die nächste Messung
#         time.sleep(0.1)
#     except IOError:
#         print("Error")