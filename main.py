import time
from time import localtime, strftime
import Adafruit_DHT
from w1thermsensor import W1ThermSensor
import json

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
      tmp_data = []
      with open('data_file.json') as json_file:
          tmp_data = json.load(json_file)
      tmp_data.extend(data_list)
      with open('data_file.json', 'w') as outfile:
          json.dump(tmp_data, outfile, indent=4)
      data_list = []
    time.sleep(15)
