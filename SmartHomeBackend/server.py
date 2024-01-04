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


# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))
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
