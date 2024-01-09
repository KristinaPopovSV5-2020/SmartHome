import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import threading

from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

app = Flask(__name__)

# InfluxDB Configuration
token = "RAIp3pQkJ2XgrGiCBnm630gxcCtPvOUmjzoeZqC5lQSYJY8VYMUrFT9k3xkmB5QkvqYrrGUlE_DaEqqolA6Aew=="
org = "ftn"
url = "http://localhost:8086"
bucket = "iot"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

# MQTT Configuration
mqtt_broker_host = "localhost"
mqtt_broker_port = 1883


def on_connect(client, userdata, flags, rc):
    client.subscribe("home/coveredPorch/dl")
    client.subscribe("home/coveredPorch/d-us1")
    client.subscribe("home/coveredPorch/d-pir1")
    client.subscribe("home/foyer/db")
    client.subscribe("home/foyer/dms")
    client.subscribe("home/foyer/ds1")
    client.subscribe("home/foyer/r-pir1")
    client.subscribe("home/bedroom2/rdht1/humidity")
    client.subscribe("home/bedroom2/rdht1/temperature")
    client.subscribe("home/bedroom3/rdht2/humidity")
    client.subscribe("home/bedroom3/rdht2/temperature")
    client.subscribe("home/openRailing/r-pir2")
    client.subscribe("home/coveredPorch/d-pir1/single")


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    topic = msg.topic

    topic_method_mapping = {
        "home/coveredPorch/dl": database_save,
        "home/coveredPorch/d-pir1": dpir1_save_to_db,
        "home/coveredPorch/d-pir1/single": dpir1_detect_movement,
        "home/foyer/r-pir1": database_save,
        "home/openRailing/r-pir2": database_save,
        "home/bedroom2/rdht1/temperature": database_save,
        "home/bedroom2/rdht1/humidity": database_save,
        "home/bedroom2/rdht2/temperature": database_save,
        "home/bedroom2/rdht2/humidity": database_save,
        "home/foyer/dms": database_save,
        "home/coveredPorch/d-us1": database_save,
        "home/foyer/ds1": database_save,
        "home/foyer/db": database_save,
    }

    if topic in topic_method_mapping:
        topic_method_mapping[topic](payload, msg.payload)


# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
# mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


def database_save(payload, msg):
    print(payload)
    save_to_db(json.loads(msg.decode('utf-8')))


def dpir1_save_to_db(payload, msg):
    save_to_db(json.loads(msg.decode('utf-8')))


def send_mqtt_request(payload, mqtt_topic):
    try:
        with app.app_context():
            publish.single(mqtt_topic, payload=json.dumps(payload), hostname=mqtt_broker_host, port=mqtt_broker_port)
            return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


def dpir1_detect_movement(payload, msg):
    print(payload)
    if payload["value"]:
        send_mqtt_request({"value": True}, "server/pi1/coveredPorch/dl")
        threading.Timer(10, send_mqtt_request, args=({"value": False}, "server/pi1/coveredPorch/dl")).start()


def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
    )
    write_api.write(bucket=bucket, org=org, record=point)


def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# ENDPOINTS RELATED TO DEVICES
@app.route('/dl_change_state', methods=['POST'])
def dl_change_state():
    try:
        data = request.get_json()
        print(data)
        send_mqtt_request(data, "server/pi1/coveredPorch/dl")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/db_change_state', methods=['POST'])
def db_change_state():
    try:
        data = request.get_json()
        print(data)
        send_mqtt_request(data, "server/pi1/foyer/db")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        store_data(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/simple_query', methods=['GET'])
def retrieve_simple_data():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Temperature")"""
    return handle_influx_query(query)


@app.route('/aggregate_query', methods=['GET'])
def retrieve_aggregate_data():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Temperature")
    |> mean()"""
    return handle_influx_query(query)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
