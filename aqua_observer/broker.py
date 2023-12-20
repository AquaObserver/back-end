import paho.mqtt.client as mqtt

from aqua_observer.apps.device_readings.models import DeviceReadings

# MQTT broker details
broker_address = "4.tcp.eu.ngrok.io"
broker_port = 11825
#username = "mosquitto-test-user1"
#password = "$7$101$rOJe8HwYjM4qXvt5$aqmGjFQhX+2v+W4bjLJPvGq0T32Hg4CTVGo4zbuIkW4CDXRXx59Ne1GSeamzGTr80PEJPAsIOmyf9fFAiK8ekA=="


# Callback functions
def on_connect(client, userdata, flags, rc, properties=None, return_code=1):
    if rc == 0:
        print("Connected with result code: " + str(rc))
        client.subscribe("aqua1/online")
        client.subscribe("aqua1/critLvl")
        client.subscribe("aqua1/wtrLvl")
        client.subscribe("aqua1/calibrate")

    else:
        print("Failed to connect, return code: " + str(rc))


def on_message(client, userdata, message):
    mesaage = message.payload.decode('utf-8')
    print("Got message: " + mesaage + " on topic " + message.topic)
    if message.topic == "aqua1/wtrLvl":
        DeviceReadings.objects.create(deviceId=1, waterLevel=int(mesaage))


# Create an MQTT client instance using MQTTv5 protocol
client = mqtt.Client("mqtt5_client_back", protocol=mqtt.MQTTv5)

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect_async(broker_address, broker_port, 60)
