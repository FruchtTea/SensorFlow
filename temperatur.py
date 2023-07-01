import time
import json
import paho.mqtt.client as mqtt

gruppenname = "sensorik"
id = "IoTinformatikschulbuch"

client_name = id + gruppenname + "server"
client_telemetry_topic = id + gruppenname + "temp"

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect("test.mosquitto.org")
mqtt_client.loop_start()
print("MQTT connected - TEMPERATUR.py")

def verarbeite_telemetry(client, nutzerdaten, nachricht):
    payload = nachricht.payload.decode()
    print("Nachricht empfangen: ", payload)

    global temperatur_value
    global data
    temperatur_value = payload

    data = {
        "temperatur": temperatur_value
    }


    json_data = json.dumps(data)

    with open("data.json", "w") as json_file:
        json_file.write(json_data)

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = verarbeite_telemetry

while True:
    try:
        time.sleep(0.1)
    except IOError:
        print("Error")    
