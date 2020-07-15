import time
import Adafruit_DHT
from w1thermsensor import W1ThermSensor


sensor = W1ThermSensor()

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

while True:
    humidity, airTemperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    waterTemperature = sensor.get_temperature()

    if humidity is not None and airTemperature is not None:
        print("Air Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(airTemperature, humidity))
    else:
        print("Failed to retrieve data from air sensor")

    if waterTemperature is not None:
        print("The water temperature is %s celsius" % waterTemperature)
        print("Failed to retrieve data from water sensor")
    time.sleep(2)