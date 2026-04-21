import json
import time
import threading
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

# This is data from my analysis in Google Colab.
UNITS_PER_SECOND = 20.83
TARGET_MOISTURE = 450
TOPIC_TELEMETRY = "id/soil_moisture_telemetry"
TOPIC_COMMAND = "id/relay_commands"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected successfully to the MQTT Broker")
        client.subscribe(TOPIC_TELEMETRY) 
    else:
        print(f"Connection failed with reason code: {reason_code}")

def control_relay(client, water_time):
    print(f"Unsubscribing... Watering for {water_time:.2f}s")
    client.unsubscribe(TOPIC_TELEMETRY)
    
    # Turn relay ON
    client.publish(TOPIC_COMMAND, json.dumps({'relay_on': True}))
    time.sleep(water_time)
    
    # Turn relay OFF
    client.publish(TOPIC_COMMAND, json.dumps({'relay_on': False}))
    time.sleep(5) # Stabilization wait
    
    print("Resubscribing to telemetry")
    client.subscribe(TOPIC_TELEMETRY)

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    moisture = payload['soil_moisture']
    print(f"Received Moisture: {moisture}")
    
    if moisture > TARGET_MOISTURE:
        req_seconds = (moisture - TARGET_MOISTURE) / UNITS_PER_SECOND
        threading.Thread(target=control_relay, args=(client, req_seconds)).start()

server_client = mqtt.Client(CallbackAPIVersion.VERSION2, "soilmoisturesensor_server")

server_client.on_connect = on_connect
server_client.on_message = handle_telemetry
server_client.connect("broker.hivemq.com", 1883)
server_client.loop_forever()