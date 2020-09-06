
import time
from time import localtime, strftime
#import Adafruit_DHT
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from w1thermsensor import W1ThermSensor
import json
import csvStore
import graph
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
RST = None
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
sensor = W1ThermSensor()
#DHT_SENSOR = Adafruit_DHT.DHT22
#DHT_PIN = 17
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
disp.begin()

# Clear display.
disp.clear()
disp.display()

print("Running")
data_list = []

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
avrageWater = 0
avrageAir = 0

while True:
    #humidity, airTemperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    temperature = round(bme280.get_temperature(), 3)
    pressure = round(bme280.get_pressure(),3)
    humidity = round(bme280.get_humidity(), 3)
    waterTemperature = round(sensor.get_temperature(), 3)

    if humidity is not None and temperature is not None and pressure is not None:
        print("Air Temp={0:0.1f}*C  Humidity={1:0.1f}%  Pressure={0:05.2f}hPa".format(temperature, humidity, pressure))
    else:
        print("Failed to retrieve data from air sensor")

    if waterTemperature is not None:
        print("The water temperature is %s celsius" % waterTemperature)
    else:
        print("Failed to retrieve data from water sensor")

    data_list.append({"time": str(strftime("%d %b %Y %H:%M:%S", localtime())), "humidity":humidity, "temperature":temperature,"pressure":pressure, "waterTemperature":waterTemperature})
    if len(data_list) > 50:
        print("Writing To file")
        csvStore.writeFile(data_list)
        data_list = []
        #try:
        #    print("Creating Graph")
        #    avrageWater, avrageAir = graph.createGraph()
        #except Exception as e:
        #    print(e)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    # Display image.
    draw.text((x, top),       "Air Temp: " + str(temperature) + "*C",  font=font, fill=255)
    draw.text((x, top+8),     "Humidity: " + str(humidity)+ "%", font=font, fill=255)
    draw.text((x, top+16),    "Pressure: " + str(pressure)+ "hPa",  font=font, fill=255)
    draw.text((x, top+25),    "Water Temp: " +  str(waterTemperature) +"*C",  font=font, fill=255)
    draw.text((x, top+34),    "Average water:" + str(avrageWater) + "*C",  font=font, fill=255)
    draw.text((x, top+43),    "Average air:" + str(avrageAir) + "*C",  font=font, fill=255)
    draw.text((x, top+52),    str(strftime("%d %b %Y %H:%M:%S", localtime())),  font=font, fill=255)

    disp.image(image)
    disp.display()
    time.sleep(15)
