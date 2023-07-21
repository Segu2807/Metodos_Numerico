import random
import time
import json
import geocoder
import math
from paho.mqtt import client as mqtt_client

BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DATA = "arquitectura"
TOPIC_ALERT = "arquitecturav2"
CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
FLAG_CONNECTED = 0

def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_DATA)
        client.subscribe(TOPIC_ALERT)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc))


def on_message(client, userdata, msg):
    try:
        print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), topic=msg.topic))
    except Exception as e:
        print(e)

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client

def get_current_position():
    address = "Calle Falsa 123, Ciudad Ficticia"  # Reemplaza esto con la dirección de tu ubicación actual
    g = geocoder.osm(address)
    return (g.lat, g.lng)

def calculate_distance(lat1, lon1, lat2, lon2):
    # Fórmula de la distancia entre dos coordenadas en la esfera terrestre (aproximación con arcos)
    # R es el radio de la Tierra (aproximadamente 6371 km)
    R = 6371.0

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance * 1000  # Convertir a metros

def simulate_movement(lat, lon, displacement):
    # Simular el movimiento desplazándose en una dirección específica (aumentando la latitud y longitud)
    new_lat = lat + displacement
    new_lon = lon + displacement
    return new_lat, new_lon

def run():
    client = connect_mqtt()
    client.loop_start()

    while True:
        time.sleep(5)  # Esperar 5 segundos entre las simulaciones de movimiento
        if FLAG_CONNECTED:
            lat, lon = get_current_position()
            print(f"Posición actual: Latitud={lat}, Longitud={lon}")

            new_lat, new_lon = simulate_movement(lat, lon, 0.001)  # Simular el movimiento
            print(f"Nuevo punto: Latitud={new_lat}, Longitud={new_lon}")

            distance = calculate_distance(lat, lon, new_lat, new_lon)
            print(f"Distancia al nuevo punto: {distance:.2f} metros")

            if distance > 2:
                msg = {"alerta": "Distancia excedida de 2 metros"}
                publish(client, TOPIC_ALERT, msg)

def publish(client, topic, msg):
    msg = json.dumps(msg)
    result = client.publish(topic, msg)


if __name__ == '__main__':
    run()
