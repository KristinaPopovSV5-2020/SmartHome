from datetime import datetime

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import threading
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO
import time

from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_query import simple_query, gyro_query


app = Flask(__name__)
scheduler = APScheduler()
socketio = SocketIO(app)

system_activated = False
alarm = False
sent_alarm = False



# InfluxDB Configuration
token = "Km0m8JvdlMfbQrc7LXd5fluhtufT0G8xZXj-5h28C64_vOcPo2Kg4NHNTuGc_7TTP_FfkPFI2xSb70GRaY7TTw=="
org = "ftn"
url = "http://localhost:8086"
bucket = "iot"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

# MQTT Configuration
mqtt_broker_host = "localhost"
mqtt_broker_port = 1883

people_inside = 0
people_inside_lock = threading.Lock()
last_dus1_value = None
new_dus1_value = None
last_dus2_value = None
new_dus2_value = None
previous_gyro_data = None


def on_connect(client, userdata, flags, rc):
    client.subscribe("home/coveredPorch/dl")
    client.subscribe("home/coveredPorch/d-us1")
    client.subscribe("home/coveredPorch/d-pir1")
    client.subscribe("home/foyer/db")
    client.subscribe("home/foyer/dms")
    client.subscribe("home/foyer/dms/single")
    client.subscribe("home/foyer/ds1")
    client.subscribe("home/foyer/r-pir1")
    client.subscribe("home/foyer/r-pir1/single")
    client.subscribe("home/familyFoyer/ds2")
    client.subscribe("home/garage/dus2")
    client.subscribe("home/garage/dpir2")
    client.subscribe("home/garage/dpir2/single")
    client.subscribe("home/garage/gdht/temperature")
    client.subscribe("home/garage/gdht/humidity")
    client.subscribe("home/WIC/gsg")
    client.subscribe("home/kitchen/rpir3")
    client.subscribe("home/kitchen/rpir3/single")
    client.subscribe("home/kitchen/rdht3/temperature")
    client.subscribe("home/kitchen/rdht3/humidity")
    client.subscribe("home/bedroom2/rdht1/humidity")
    client.subscribe("home/bedroom2/rdht1/temperature")
    client.subscribe("home/bedroom3/rdht2/humidity")
    client.subscribe("home/bedroom3/rdht2/temperature")
    client.subscribe("home/openRailing/r-pir2")
    client.subscribe("home/openRailing/r-pir2/single")
    client.subscribe("home/coveredPorch/d-pir1/single")
    client.subscribe("home/owners-suite/bir/rgb")
    client.subscribe("home/owners-suite/bir")
    client.subscribe("home/owners-suite/brgb")
    client.subscribe("home/owners-suite/brgb/single")
    client.subscribe("home/owners-suite/bb")
    client.subscribe("home/foyer/ds1-2")
    client.subscribe("home/foyer/ds1-2/duration")
    client.subscribe("home/dinette/rpir4")
    client.subscribe("home/dinette/rpir4/single")
    client.subscribe("home/owners-suite/rdht4/temperature")
    client.subscribe("home/owners-suite/rdht4/humidity")
    client.subscribe("home/owners-suite/b4sd")


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    topic = msg.topic

    topic_method_mapping = {
        "home/coveredPorch/dl": database_save,
        "home/coveredPorch/d-pir1": dpir1_save_to_db,
        "home/coveredPorch/d-pir1/single": dpir1_detect_movement,
        "home/foyer/r-pir1": database_save,
        "home/foyer/r-pir1/single": rpir_detect_movement,
        "home/familyFoyer/ds2": database_save,
        "home/garage/dus2": dus2_detect_movement,
        "home/garage/dpir2": database_save,
        "home/garage/dpir2/single": dpir2_detect_movement,
        "home/garage/gdht/temperature": handle_gdht_message,
        "home/garage/gdht/humidity": handle_gdht_message,
        "home/WIC/gsg": gyro_database_save,
        "home/kitchen/rpir3": database_save,
        "home/kitchen/rpir3/single": rpir_detect_movement,
        "home/kitchen/rdht3/temperature": database_save,
        "home/kitchen/rdht3/humidity": database_save,
        "home/openRailing/r-pir2": database_save,
        "home/openRailing/r-pir2/single": rpir_detect_movement,
        "home/bedroom2/rdht1/temperature": database_save,
        "home/bedroom2/rdht1/humidity": database_save,
        "home/bedroom3/rdht2/temperature": database_save,
        "home/bedroom3/rdht2/humidity": database_save,
        "home/foyer/dms": database_save,
        "home/foyer/dms/single": dms_detect_password,
        "home/coveredPorch/d-us1": dus1_detect_movement,
        "home/foyer/ds1": database_save,
        "home/foyer/db": database_save,
        "home/owners-suite/bir": database_save,
        "home/owners-suite/bir/rgb": turn_on_rgb,
        "home/owners-suite/brgb": database_save,
        "home/owners-suite/bb": database_save,
        "home/foyer/ds1-2": ds1_ds2_detect,
        "home/foyer/ds1-2/duration": ds1_ds2_duration,
        "home/dinette/rpir4": database_save,
        "home/dinette/rpir4/single": rpir_detect_movement,
        "home/owners-suite/rdht4/temperature": database_save,
        "home/owners-suite/rdht4/humidity": database_save,
        "home/owners-suite/brgb/single": detect_change_color_rgb,
        "home/owners-suite/b4sd": display_current_time,
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
    socketio.emit('data', payload)
    save_to_db(json.loads(msg.decode('utf-8')))

def display_current_time(payload, msg):
    socketio.emit('b4sd', payload)

def dpir1_save_to_db(payload, msg):
    save_to_db(json.loads(msg.decode('utf-8')))


def ds1_ds2_detect(payload, msg):
    global system_activated,alarm, sent_alarm
    value = payload['value']
    if value:
        if system_activated and alarm and not sent_alarm:
            sent_alarm = True
            print("BUZZZZ")
            send_mqtt_request({'value': True}, "server/pi3/owners-suite/bb")
            time.sleep(0.5)
            send_mqtt_request({'value': True}, "server/pi1/foyer/db")
    else:
        if alarm and sent_alarm:
            alarm = False
            sent_alarm = False
            print("Sound off")
            send_mqtt_request({'value': False}, "server/pi3/owners-suite/bb")
            time.sleep(0.5)
            send_mqtt_request({'value': False}, "server/pi1/foyer/db")


def detect_change_color_rgb(payload, msg):
    socketio.emit('brgb', payload)

def ds1_ds2_duration(payload, msg):
    global alarm, sent_alarm
    if not alarm and not sent_alarm:
        sent_alarm = True
        alarm = True
        print("BUZZZZ")
        send_mqtt_request({'value': True}, "server/pi3/owners-suite/bb")
        time.sleep(0.5)
        send_mqtt_request({'value': True}, "server/pi1/foyer/db")


def send_mqtt_request(payload, mqtt_topic):
    try:
        with app.app_context():
            publish.single(mqtt_topic, payload=json.dumps(payload), hostname=mqtt_broker_host, port=mqtt_broker_port)
            return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


def dms_detect_password(payload, msg):
    global alarm, system_activated, sent_alarm
    print(payload)
    if payload['value'].split("-")[1] == "True":
        alarm = False
        system_activated = False
        sent_alarm = False
        print("Sound off")
        print("System deactivated")
        send_mqtt_request({'value': False}, "server/pi3/owners-suite/bb")
        time.sleep(0.5)
        send_mqtt_request({'value': False}, "server/pi1/foyer/db")

    else:
        time.sleep(10)
        system_activated = True
        alarm = True
        print("System activated")
        print("Alarm activated")


def dpir1_detect_movement(payload, msg):
    print(payload)
    update_people_inside_dus1()
    if payload["value"]:
        send_mqtt_request({"value": True}, "server/pi1/coveredPorch/dl")
        threading.Timer(10, send_mqtt_request, args=({"value": False}, "server/pi1/coveredPorch/dl")).start()


def dpir2_detect_movement(payload, msg):
    print(payload)
    update_people_inside_dus2()


def rpir_detect_movement(payload, msg):
    global people_inside, alarm, sent_alarm
    if people_inside == 0:
        alarm = True
        if not sent_alarm:
            sent_alarm = True
            print("BUZZZZ")
            send_mqtt_request({'value': True}, "server/pi3/owners-suite/bb")
            time.sleep(0.5)
            send_mqtt_request({'value': True}, "server/pi1/foyer/db")


def update_people_inside_dus1():
    global people_inside, last_dus1_value, new_dus1_value, alarm, sent_alarm
    with people_inside_lock:
        if new_dus1_value < last_dus1_value:
            people_inside += 1
        elif new_dus1_value > last_dus1_value:
            people_inside -= 1
        if people_inside < 0:
            people_inside = 0
    print("PEOPLE INSIDE: ", people_inside)


def update_people_inside_dus2():
    global people_inside, last_dus2_value, new_dus2_value, alarm, sent_alarm
    with people_inside_lock:
        if new_dus2_value < last_dus2_value:
            people_inside += 1
        elif new_dus2_value > last_dus2_value:
            people_inside -= 1
        if people_inside < 0:
            people_inside = 0
    print("PEOPLE INSIDE: ", people_inside)


def dus1_detect_movement(payload, msg):
    global last_dus1_value, new_dus1_value
    print(payload)
    last_dus1_value = new_dus1_value
    new_dus1_value = payload["value"]
    database_save(payload, msg)


def dus2_detect_movement(payload, msg):
    global last_dus2_value, new_dus2_value
    print(payload)
    last_dus2_value = new_dus2_value
    new_dus2_value = payload["value"]
    database_save(payload, msg)


def handle_gdht_message(payload, msg):
    if payload["measurement"] == "Temperature":
        send_mqtt_request({"temperature": payload["value"]}, "server/pi2/garage/glcd")
    elif payload["measurement"] == "Humidity":
        send_mqtt_request({"humidity": payload["value"]}, "server/pi2/garage/glcd")
    database_save(payload, msg)


def turn_on_rgb(payload, msg):
    print(payload)
    code = payload['value']
    value = {"color": ' '}
    if code == "1":
        # turn on
        value = {"color": 'white'}
    elif code == "2":
        # turn off
        value = {"color": 'turnOff'}
    elif code == "3":
        # red
        value = {"color": 'red'}
    elif code == "4":
        # green
        value = {"color": 'green'}
    elif code == "5":
        # blue
        value = {"color": 'blue'}
    elif code == "6":
        # yellow
        value = {"color": 'yellow'}
    elif code == "7":
        # purple
        value = {"color": 'purple'}
    elif code == "8":
        # light blue
        value = {"color": 'light_blue'}

    send_mqtt_request(value, "server/pi3/owners-suite/brgb")


# ALARM
def activate_alarm():
    print("Alarm aktiviran")
    send_mqtt_request({'value': True}, "server/pi3/owners-suite/bb")
    time.sleep(2)
    data = {'intermittently': True,
            'turnOn': True}
    send_mqtt_request(data, "server/pi3/owners-suite/b4sd")


def set_alarm(alarm_time):
    alarm_time = datetime.now().replace(hour=alarm_time[0], minute=alarm_time[1], second=0, microsecond=0)
    scheduler.add_job(id='activate_alarm', func=activate_alarm, trigger='date', run_date=alarm_time)


def check_and_trigger_alarm_gyro(payload, previous_data, keys, threshold):
    global alarm, sent_alarm
    for key in keys:
        if abs(payload[key] - previous_data[key]) > threshold:
            alarm = True
            if not sent_alarm:
                sent_alarm = True
                print("BUZZZZ")
                send_mqtt_request({'value': True}, "server/pi3/owners-suite/bb")
                time.sleep(0.5)
                send_mqtt_request({'value': True}, "server/pi1/foyer/db")

def gyro_database_save(payload, msg):
    global previous_gyro_data
    print(payload)
    save_gyro_to_db(json.loads(msg.decode('utf-8')))

    # Compare with previous data
    if previous_gyro_data is not None:
        check_and_trigger_alarm_gyro(payload, previous_gyro_data, ['accel_x', 'accel_y', 'accel_z'], 0.2)
        check_and_trigger_alarm_gyro(payload, previous_gyro_data, ['gyro_x', 'gyro_y', 'gyro_z'], 20)

    # Update previous data
    previous_gyro_data = payload


def save_gyro_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("accel_x", data["accel_x"])
        .field("accel_y", data["accel_y"])
        .field("accel_z", data["accel_z"])
        .field("gyro_x", data["gyro_x"])
        .field("gyro_y", data["gyro_y"])
        .field("gyro_z", data["gyro_z"])
    )
    write_api.write(bucket=bucket, org=org, record=point)


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





# ENDPOINTS RELATED TO DEVICES

@app.route('/set_alarm', methods=['POST'])
def set_alarms():
    try:
        data = request.get_json()
        value_data = data['value']
        time_data = value_data.split(',')
        alarm_time = (int(time_data[0]), int(time_data[1]))
        set_alarm(alarm_time)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/cancel_alarm', methods=['POST'])
def cancel_alarm():
    try:
        data = request.get_json()
        print(data)
        # salje se vrednost false, da se ne bi vise cuo bb
        send_mqtt_request(data, "server/pi3/owners-suite/bb")
        print("POSLATO")
        time.sleep(2)
        data_b4sd = {'intermittently': False,
                     'turnOn': False}
        send_mqtt_request(data_b4sd, "server/pi3/owners-suite/b4sd")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/dl_change_state', methods=['POST'])
def dl_change_state():
    try:
        data = request.get_json()
        send_mqtt_request(data, "server/pi1/coveredPorch/dl")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/dms_change_state', methods=['POST'])
def dms_change_state():
    try:
        data = request.get_json()
        send_mqtt_request(data, "server/pi1/foyer/dms")
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


@app.route('/bb_change_state', methods=['POST'])
def bb_change_state():
    try:
        data = request.get_json()
        print(data)
        send_mqtt_request(data, "server/pi3/owners-suite/bb")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/lcd_change_state', methods=['POST'])
def lcd_change_state():
    try:
        data = request.get_json()
        print(data)
        send_mqtt_request(data, "server/pi2/garage/lcd")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/bir_change_state', methods=['POST'])
def bir_change_state():
    try:
        data = request.get_json()
        print(data)
        send_mqtt_request(data, "server/pi3/owners-suite/bir")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/b4sd_change_state', methods=['POST'])
def b4sd_change_state():
    try:
        data = request.get_json()
        send_mqtt_request(data, "server/pi3/owners-suite/b4sd")
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

def handle_influx_query(query):
    query_api = influxdb_client.query_api()
    tables = query_api.query(query, org=org)

    selected_columns = []
    for table in tables:
        for record in table.records:
            selected_columns = {
                "_measurement": record.get_measurement(),
                "_time": record.get_time(),
                "_value": record.get_value(),
                "name": record.values["name"],
                "runs_on": record.values["runs_on"],
                "simulated": record.values["simulated"]
            }

    return selected_columns


def export_container_gyro(container):
    unique_container = {"_measurement": "", "_time": "", "_value": [], "name": "", "runs_on": "", "simulated": ""}

    if container:
        first_record = container[0]
        unique_container['_measurement'] = first_record['_measurement']
        unique_container["_time"] = first_record["_time"]
        unique_container['_value'].append(first_record['_value'])
        unique_container['name'] = first_record['name']
        unique_container['runs_on'] = first_record['runs_on']
        unique_container['simulated'] = first_record['simulated']

        for c in container[1:]:
            unique_container['_value'].append(c['_value'])

    return unique_container

@app.route('/aggregate_query', methods=['GET'])
def retrieve_aggregate_data():
    data = []
    data_gyro = []
    try:
        measurement_name_pair = [("DS","DS1"),("DL","DL"),("DUS","DUS1"),("DB","DB"),("PIR","DPIR1"),("DMS","DMS"),
                             ("PIR","RPIR1"),("PIR","RPIR2"),("Humidity","RDHT1"),("Humidity","RDHT2"),("Temperature","RDHT1"),
                             ("Temperature", "RDHT2"), ("PIR","RPIR4"),("Humidity","RDHT4"),("Temperature","RDHT4"),("BB","BB"),("BIR","BIR"),("RGB","BRGB"),
                                 ("DS","DS2"),("DUS","DUS2"),("PIR","DPIR2"),("Humidity","GDHT"),("Temperature","GDHT"),("PIR","RPIR3"),("Humidity","RDHT3"),("Temperature","RDHT3")
                             ]
        for (m,n) in measurement_name_pair:
            query = simple_query(m,n)
            selected = handle_influx_query(query)
            data.append(selected)
        g_queries = gyro_query()
        for g_query in g_queries:
            gyro_selected = handle_influx_query(g_query)
            data_gyro.append(gyro_selected)
            print(gyro_selected)
        data.append(export_container_gyro(data_gyro))
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})




if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
