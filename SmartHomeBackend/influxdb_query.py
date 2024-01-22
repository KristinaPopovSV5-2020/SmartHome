
def simple_query(measurement ,name):
    query = f"""
        from(bucket: "iot")
          |> range(start: -5d)
          |> filter(fn: (r) => r._measurement == "{measurement}")
          |> filter(fn: (r) => r._field == "measurement")
          |> filter(fn: (r) => r.name == "{name}")
          |> filter(fn: (r) => r.simulated == "True" or r.simulated == "False")
          |> last()
        """
    return query

def gyro_query():
    query = f"""
        from(bucket: "iot")
      |> range(start: -5d)
      |> filter(fn: (r) => r["_measurement"] == "Gyro")
      |> filter(fn: (r) => r["_field"] == "accel_x" or r["_field"] == "accel_y" or r["_field"] == "accel_z" or r["_field"] == "gyro_x" or r["_field"] == "gyro_y" or r["_field"] == "gyro_z")
      |> filter(fn: (r) => r["name"] == "GSG")
      |> filter(fn: (r) => r.simulated == "True" or r.simulated == "False")
      |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    """
    return query
