import random


def get_sensor_data():

    temperature = round(random.uniform(20, 40), 2)

    humidity = round(random.uniform(30, 90), 2)

    pressure = round(random.uniform(980, 1035), 2)

    return {
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure
    }