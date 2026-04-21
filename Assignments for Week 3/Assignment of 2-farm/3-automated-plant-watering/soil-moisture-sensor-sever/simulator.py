import json
import time
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

TOPIC_TELEMETRY = "id/soil_moisture_telemetry"
TOPIC_COMMAND = "id/relay_commands"
BROKER_HOST = "broker.hivemq.com"
BROKER_PORT = 1883
RETRY_SECONDS = 5


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected successfully to the MQTT Broker")
        # Listen for relay commands from the server.
        client.subscribe(TOPIC_COMMAND)
    else:
        print(f"Connection failed with reason code: {reason_code}")


def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8", errors="replace")
    print(f"Received command on {msg.topic}: {payload}")


def connect_with_retry(client):
    while True:
        try:
            print(f"Connecting to MQTT broker {BROKER_HOST}:{BROKER_PORT}...")
            client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
            return
        except (TimeoutError, OSError) as exc:
            print(f"MQTT connection failed: {exc}. Retrying in {RETRY_SECONDS}s...")
            time.sleep(RETRY_SECONDS)

device_client = mqtt.Client(CallbackAPIVersion.VERSION2, "soilmoisturesensor_client")

device_client.on_connect = on_connect
device_client.on_message = on_message
connect_with_retry(device_client)
device_client.loop_start()

# This is just a test case to show the server is working. You can replace this with your actual sensor code.
while True:
    data = {'soil_moisture': 649} 
    print(f"Sending telemetry: {data}")
    device_client.publish(TOPIC_TELEMETRY, json.dumps(data))
    time.sleep(10)