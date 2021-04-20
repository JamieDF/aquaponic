import time
from time import localtime, strftime
from datetime import datetime, date
from decimal import Decimal
from sensors import Sensors
import csv   
import json
from flask import Flask, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import os.path

app = Flask(__name__)
CORS(app)

SensorObject = Sensors()
data_keys = ["time", "air_temp", "humidity", "pressure", "air_temp_DHT", "humidity_DHT", "outside_air_temp", "outside_humidity", "outside_pressure"]

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()
    elif isinstance(o, Decimal):
        return float(o)

try:
    record_backlog = []
    with open('record_backlog.json') as json_file:  
        _data = json.load(json_file)
        if _data:
            record_backlog = _data
except:
    record_backlog = []

def routine():
    todaysFile = date.today().strftime("%d%m%y")
    sensorData = SensorObject.get_data()
    print(sensorData)
    if sensorData:
        record_backlog.append(sensorData)
        if record_backlog:
            for record in record_backlog[:]: 
                if writeToCSV("data/"+ str(todaysFile) +".csv", record): 
                    record_backlog.remove(record) 
                else:
                    print("Keeping record in backlog")
                    break

            print("Storing record_backlog")
            try:
                with open('record_backlog.json', 'w') as outfile:
                    json.dump(record_backlog, outfile, indent=4)
            except Exception as e:
                print("Error: " + str(e))
    else:
        print("SENSORDATA == Null")

def writeToCSV(filename, item):
    file_exists = os.path.isfile(filename)
    try:
        with open(filename, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data_keys)
            if not file_exists:
                writer.writeheader()
            writer.writerow(item)
        return True
    except Exception as e: 
        print(e)
        return False


@app.route('/get_current_sensors', methods=['POST'])
def get_current_sensors():
    try:
        return json.dumps(SensorObject.get_data()), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({"sensorTest Fail": str(e)}), 200, {'Content-Type': 'application/json'}


scheduler = BackgroundScheduler(timezone="Europe/London")
scheduler.add_job(func=routine, trigger="cron", minute='0')
scheduler.add_job(func=routine, trigger="cron", minute='30')

scheduler.start()
now = datetime.now()
print("Monitor Active at " + str(now.strftime("%c")))

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)