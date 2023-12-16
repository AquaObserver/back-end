import paho.mqtt.client as mqtt
from aqua_observer.apps.device_readings.models import DeviceReadings
# MQTT broker details
broker_address = "172.17.0.4"  # Replace with your server IP address
broker_port = 1883  # Default port for MQTT protocol

# Callback functions
def on_connect(client, userdata, flags, rc, properties=None, return_code=1):
    if rc == 0:
        print("Connected with result code: " + str(rc))
        # Subscribe to topics after successful connection
        client.subscribe("aqua1/online")
        client.subscribe("aqua1/critLvl")
        client.subscribe("aqua1/wtrLvl")
        client.subscribe("aqua1/calibrate")

    else:
        print("Failed to connect, return code: " + str(rc))

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode('utf-8')} on topic {message.topic}")
    mesaage = message.payload.decode('utf-8')
    try:
        mesaage = float(mesaage)
    except:
        mesaage = 7
    DeviceReadings.objects.create(deviceId=1, waterLevel=mesaage)


# Create an MQTT client instance using MQTTv5 protocol
client = mqtt.Client("mqtt5_client", protocol=mqtt.MQTTv5)

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect_async(broker_address, broker_port, 60)


