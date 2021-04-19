from statistics import mean

def generate(data):
    returnData={"water_min":None, "water_max":None, "water_average":None, "air_min":None, "air_max":None, "air_average":None, "humidity_average":None, "pressure_average":None}
    list_form={"water_temp":[], "air_temp":[], "humidity":[], "pressure":[]}

    for item in data:
        list_form['water_temp'].append(item['water_temp'])
        list_form['air_temp'].append(item['air_temp'])
        list_form['humidity'].append(item['humidity'])
        list_form['pressure'].append(item['pressure'])

    returnData["water_average"] = round(mean(list_form['water_temp']), 2)
    returnData["air_average"] = round(mean(list_form['air_temp']), 2)
    returnData["humidity_average"] = round(mean(list_form['humidity']), 2)
    returnData["pressure_average"] = round(mean(list_form['pressure']), 2)

    returnData["water_max"] = max(list_form['water_temp'])
    returnData["air_max"] = max(list_form['air_temp'])

    returnData["water_min"] = min(list_form['water_temp'])
    returnData["air_min"] = min(list_form['air_temp'])

    return returnData




