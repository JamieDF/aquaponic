import time
from time import localtime, strftime
from datetime import datetime
from sensors import Sensors
from display import Display
from database import db
import json
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

SensorObject = Sensors()
DisplayObject = Display()
DB = db()

try:
    record_backlog = []
    with open('record_backlog.json') as json_file:  
        _data = json.load(json_file)
        if _data:
            record_backlog = _data
except:
    record_backlog = []

# if record_backlog:
#     for record in record_backlog[:]: 
#         if DB.insert_record("hourly_logs", record): 
#             record_backlog.remove(record) 
#         else:
#             print("Keeping record in backlog")
#             break

#     print("Storing record_backlog")
#     try:
#         with open('record_backlog.json', 'w') as outfile:
#             json.dump(record_backlog, outfile, indent=4)
#     except Exception as e:
#         print("Error: " + str(e))