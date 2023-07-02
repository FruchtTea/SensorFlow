from flask import Flask, render_template
import folium, time, threading, json, subprocess
import paho.mqtt.client as mqtt

long = 0
lat = 0
temp = 0
humid = 0

################## HIER STARTET MQTT LOGIK ##################
gruppenname = "sensorik"
id = "IoTinformatikschulbuch"

# Eindeutiger Name mit dem sich beim MQTT Broker angemeldet wird
client_name = id + gruppenname + "server"

# Kanal auf der das Gerät Informationen empfangen wird
client_telemetry_topic = id + gruppenname + "/telemetry"

# Erzeugen des MQTT-Client Objekts und verbinden mit dem MQTT-Broker
def subscribe_to_mqtt():
    global mqtt_client

    mqtt_client = mqtt.Client(client_name)
    mqtt_client.connect("test.mosquitto.org")
    mqtt_client.loop_start()
    print("MQTT connected")

    # Abonniert die oben gegebene Topic
    mqtt_client.subscribe(client_telemetry_topic)

    # Legt fest, dass die Methode verarbeite_telemetry aufgerufen werden soll, wenn eine Nachricht eintrifft
    mqtt_client.on_message = verarbeite_telemetry


# Methode wird aufgerufen, sobald eine neue Nachricht empfangen wurde
def verarbeite_telemetry(client, nutzerdaten, nachricht):
    payload = nachricht.payload.decode()
    print(payload)

    data = payload.split("=")

    if data[0] == "lat":
        global lat
        lat = float(data[1])

    if data[0] == "long":
        global long
        long = float(data[1])

    if data[0] == "humid":
        global humid
        humid = float(data[1])

    if data[0] == "temp":
        global temp
        temp = float(data[1])


################## HIER STARTET DER FLASK SERVER ##################

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
    global temp
    global humid

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