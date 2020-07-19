import time
from time import localtime, strftime
import Adafruit_DHT
from w1thermsensor import W1ThermSensor
import json
import csvStore
import graph

sensor = W1ThermSensor()
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17

print("Running")
data_list = []

while True:
    humidity, airTemperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    waterTemperature = sensor.get_temperature()

    if humidity is not None and airTemperature is not None:
        print("Air Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(airTemperature, humidity))
    else:
        print("Failed to retrieve data from air sensor")

    if waterTemperature is not None:
        print("The water temperature is %s celsius" % waterTemperature)
    else:
        print("Failed to retrieve data from water sensor")
    data_list.append({"time": str(strftime("%d %b %Y %H:%M:%S", localtime())), "humidity":humidity, "airTemperature":airTemperature,"waterTemperature":waterTemperature})
    if len(data_list) > 50:
        print("Writing To file")
        csvStore.writeFile(data_list)
        data_list = []
        try:
            print("Creating Graph")
            graph.createGraph()
        except Exception as e:
            print(e)
    time.sleep(15)
