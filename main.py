import time
from time import localtime, strftime
from datetime import datetime
from decimal import Decimal
from sensors import Sensors
from display import Display
from database import db
import analytics
import json
from flask import Flask, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)
CORS(app)

SensorObject = Sensors()
DisplayObject = Display()
DB = db()
data_keys = ["id", "time", "water_temp", "air_temp", "humidity", "pressure"]

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
    sensorData = SensorObject.get_data()
    print(sensorData)
    if sensorData:
        record_backlog.append(sensorData)
        
        if record_backlog:
            for record in record_backlog[:]: 
                if DB.insert_record("hourly_logs", record): 
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
    DisplayObject.draw_data(sensorData, str(strftime("%d %b %Y %H:%M:%S", localtime())))

    
@app.route('/get_current_sensors', methods=['POST'])
def get_current_sensors():
    try:
        return json.dumps(SensorObject.get_data()), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({"sensorTest Fail": str(e)}), 200, {'Content-Type': 'application/json'}

@app.route('/get_sensor_logs', methods=['POST'])
def get_sensor_logs():
    try:
        _jsonData = request.get_json(force=True)
        print(_jsonData)

        if _jsonData['target'] == "Today":
            today = datetime.today()
            daystart = datetime(year=today.year, month=today.month, day=today.day, hour=0, second=0).strftime("%a, %d %b %Y %H:%M:%S")
            dt = datetime.now()
            dt = dt.strftime("%a, %d %b %Y %H:%M:%S")
            _data={"logs":DB.get_records_between("hourly_logs", data_keys, "time", daystart, dt)}
            _data['analytics'] = analytics.generate(_data["logs"])
            return json.dumps(_data, default = myconverter), 200, {'Content-Type': 'application/json'}
        elif _jsonData['target'] == "Specific":
            start_date = datetime.strptime(_jsonData['start_date'],"%Y-%m-%d %H:%M")
            end_date = datetime.strptime(_jsonData['end_date'],"%Y-%m-%d %H:%M")
            _data={"logs":DB.get_records_between("hourly_logs", data_keys, "time", start_date, end_date)}
            _data['analytics'] = analytics.generate(_data["logs"])
            return json.dumps(_data, default = myconverter), 200, {'Content-Type': 'application/json'}
        else:
            _data={"logs":DB.get_records_between("hourly_logs", data_keys)}
            _data['analytics'] = analytics.generate(_data["logs"])
            return json.dumps(_data, default = myconverter), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({"get_sensor_logs Fail": str(e)}), 200, {'Content-Type': 'application/json'}


scheduler = BackgroundScheduler(timezone="Europe/London")
scheduler.add_job(func=routine, trigger="cron", minute='0')
scheduler.add_job(func=routine, trigger="cron", minute='30')
scheduler.start()
now = datetime.now()
print("Monitor Active at " + str(now.strftime("%c")))

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)