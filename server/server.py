import paho.mqtt.client as mqtt
import json

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

def on_connect(client, userdata, flags, rc):
    client.subscribe("home/coveredPorch/dl")
    client.subscribe("home/foyer/db")
    client.subscribe("home/foyer/dms/temperature")
    client.subscribe("home/foyer/dms/humidity")
    client.subscribe("home/beedroom2/rdht1")
    client.subscribe("home/beedroom3/rdht2")


def on_message(client, userdata, msg):
    print("USAO")
    payload_data = json.loads(msg.payload.decode('utf-8'))
    save_to_db(payload_data)

# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
    )
    print(point)
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
