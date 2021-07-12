from smbus2 import SMBus
#from smbus import SMBus
import bme280
from w1thermsensor import W1ThermSensor
from datetime import datetime

class Sensors(object):
    def __init__(self):
        self.sensor_bus = SMBus(1)
        self.sensor_address = 0x76
        self.water_sensor = W1ThermSensor()
        self.calibration_params = bme280.load_calibration_params(self.sensor_bus, self.sensor_address)
        self.air_sensor = bme280.sample(self.sensor_bus, self.sensor_address, self.calibration_params)
        self.sensor_data = {
                "water_temp": self.water_sensor.get_temperature(),
                "air_temp": self.air_sensor.temperature,
                "humidity": self.air_sensor.humidity,
                "pressure": self.air_sensor.pressure}

    def update_sensors(self):
        error = False
        try:
            self.air_sensor = bme280.sample(bus=self.sensor_bus)
        except Exception as e:
            error = True
            print("Error running air sensor : "+ str(e))

        self.sensor_data = {
            "water_temp": self.water_sensor.get_temperature(),
            "air_temp": self.air_sensor.temperature,
            "humidity": self.air_sensor.humidity,
            "pressure": self.air_sensor.pressure}
        return error
    
    def get_data(self):
        isError = self.update_sensors()
        dt = datetime.now()
        returnData = {"time": dt.strftime("%a, %d %b %Y %H:%M:%S")}
        data = {"water_temp":None, "air_temp":None,"humidity":None, "pressure":None}
        
        for data_item in data:
            try:
                data[data_item] = round(self.sensor_data[data_item], 2)
            except Exception as e:
                print("Sensor {_sensor} Error: {_error}".format(_sensor=data_item,_error=str(e)))
                isError = True
                
        if not isError:
            returnData.update(data)
            return returnData

# test = Sensors()
# print(test.get_data())