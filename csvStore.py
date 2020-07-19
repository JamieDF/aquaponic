import csv
import os

file = "Newdata.csv"

def writeFile(data):
    fieldnames = []
    if isinstance(data, list):
        fieldnames = data[0].keys()
    else:
            fieldnames = data.keys()
    try:
        fd = os.open(file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except OSError as e:
        if e.errno == 17:
            #For existing files
            with open(file, 'a') as f:
                w = csv.DictWriter(f, fieldnames)
                if isinstance(data, list):
                    for i in data:
                            w.writerow(i)
                else:
                    w.writerow(data)
            return True
    
    with open(file, 'w') as f:
        w = csv.DictWriter(f, fieldnames)
        w.writeheader()
        if isinstance(data, list):
            for i in data:
                w.writerow(i)
        else:
            w.writerow(data)
    return True