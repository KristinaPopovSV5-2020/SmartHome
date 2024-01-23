
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
    queries = []
    fields = ["accel_x","accel_y","accel_z","gyro_x","gyro_y","gyro_z"]
    for field in fields:
        query = f"""
            from(bucket: "iot")
          |> range(start: -5d)
          |> filter(fn: (r) => r["_measurement"] == "Gyro")
          |> filter(fn: (r) => r["_field"] == "{field}")
          |> filter(fn: (r) => r["name"] == "GSG")
          |> filter(fn: (r) => r.simulated == "True" or r.simulated == "False")
          |> last()
        """
        queries.append(query)
    return queries
