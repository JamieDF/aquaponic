

from smbus2 import SMBus
#from smbus import SMBus
import bme280
import Adafruit_DHT
from datetime import datetime



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
        try:
            self.air_sensor = bme280.sample(bus=self.sensor_bus)
        except Exception as e:
            error = True
            print("Error running air sensor : "+ str(e))
        
        try:
            humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
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
            return returnData

test = Sensors()
print(test.get_data())
