

from smbus2 import SMBus
#from smbus import SMBus
import bme280
import Adafruit_DHT
from datetime import datetime
import time
import requests
import json



class Sensors(object):
    def __init__(self):
        self.sensor_bus = SMBus(1)
        self.sensor_address = 0x76
        self.calibration_params = bme280.load_calibration_params(self.sensor_bus, self.sensor_address)
        self.air_sensor = bme280.sample(self.sensor_bus, self.sensor_address, self.calibration_params)
        self.DHT_SENSOR = Adafruit_DHT.DHT22
        self.DHT_PIN = 4
        self.sensor_data = {
                "air_temp": self.air_sensor.temperature,
                "humidity": self.air_sensor.humidity,
                "pressure": self.air_sensor.pressure,
                "air_temp_DHT": Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)[1],
                "humidity_DHT": Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)[0]}

    def update_sensors(self):
        error = False
        humidity = None
        temperature = None
        attempts = 0
        try:
            self.air_sensor = bme280.sample(bus=self.sensor_bus)
        except Exception as e:
            error = True
            print("Error running air sensor : "+ str(e))
        
        try:
            while (not humidity and not temperature):
                humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
                time.sleep(2)
        except Exception as e:
            error = True
            print("Error running DHT air sensor : "+ str(e))

        
        self.sensor_data = {
            "air_temp": self.air_sensor.temperature,
            "humidity": self.air_sensor.humidity,
            "pressure": self.air_sensor.pressure,
            "air_temp_DHT": temperature,
            "humidity_DHT": humidity}
        return error
    
    def getWeather(self):
        output = {"outside_air_temp": None, "outside_humidity":None, "outside_pressure": None}
        try:
            targetURL = "http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&APPID=4048c2bfc3219e25cc2b99ab0d371978".format(lat=float(56.10963), lon=float(-3.1633400000000003))
            response = requests.get(targetURL, timeout=30)
            if response.ok:
                formated_response = json.loads(response.content)  
                weather = formated_response['weather'][0]['main']
                output["outside_air_temp"] = weather['temp']
                output["outside_humidity"] = weather['humidity']
                output["outside_pressure"] = weather['pressure']
                return output
            else:
                print("getWeather Response Error: " +str(response))
        except Exception as errtxt:
            print ("getWeather Exception: " + str(errtxt))
        return output

    def get_data(self):
        isError = self.update_sensors()
        dt = datetime.now()
        returnData = {"time": dt.strftime("%a, %d %b %Y %H:%M:%S")}
        data = {"air_temp":None,"humidity":None, "pressure":None, "air_temp_DHT":None, "humidity_DHT":None }
        
        for data_item in data:
            try:
                data[data_item] = round(self.sensor_data[data_item], 2)
            except Exception as e:
                print("Sensor {_sensor} Error: {_error}".format(_sensor=data_item,_error=str(e)))
                isError = True
                
        if not isError:
            returnData.update(data)
            returnData.update
            return returnData(self.getWeather())

