import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Display(object):
    def __init__(self):
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address=0x3C)
        self.disp.begin()
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        
        
    def clear_display(self):
        self.disp.clear()
        self.draw.rectangle((0,0,self.disp.width, self.disp.height), outline=0, fill=0)

    def draw_data(self, data, time):
        self.clear_display()
        try:          
            self.draw.text((0, -2),  "Air Temp: " + str(data['air_temp']) + "*C",  font=self.font, fill=255)
            self.draw.text((0, 6),   "Humidity: " + str(data['humidity'])+ "%", font=self.font, fill=255)
            self.draw.text((0, 14),  "Pressure: " + str(data['pressure'])+ "hPa",  font=self.font, fill=255)
            self.draw.text((0, 23),  "Water Temp: " +  str(data['water_temp']) +"*C",  font=self.font, fill=255)
            # self.draw.text((0, 32),    "Average water:" + str(avrageWater) + "*C",  font=font, fill=255)
            # self.draw.text((0, 41),    "Average air:" + str(avrageAir) + "*C",  font=font, fill=255)
        except Exception as e:
            self.draw.text((0, -2),  "Error drawing data: ",  font=self.font, fill=255)
            self.draw.text((0, 6),  str(e),  font=self.font, fill=255)

        self.draw.text((0, 50),    str(time),  font=self.font, fill=255)
                                        #strftime("%d %b %Y %H:%M:%S", localtime()))
        self.disp.image(self.image)
        self.disp.display()
