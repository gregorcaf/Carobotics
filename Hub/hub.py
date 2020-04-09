import airsim
import cv2
import numpy as np
import os
import time
from flask import jsonify, Flask
from functools import reduce

CarStateSensor = "CarState"
getGpsData = "GpsData"
getMagnetometerData = "MagnetometerData"


client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()


app = Flask(__name__)
#  region getInfo
#  region CarState
@app.route("/hub/{}".format(CarStateSensor))
def sensor_all():
    return str(client.getCarState())

@app.route("/hub/{}/<attr1>".format(CarStateSensor))
def sensor_attr1(attr1):
    car = client.getCarState()
    try:
        return str(getattr(car, attr1))
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>".format(CarStateSensor))
def sensor_attr2(attr1, attr2):
    car = client.getCarState()
    try:
        return str(reduce(getattr,(attr1, attr2), car))
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>/<attr3>".format(CarStateSensor))
def sensor_attr3(attr1, attr2, attr3):
    car = client.getCarState()
    try:
        return str(reduce(getattr,(attr1, attr2, attr3), car))
    except AttributeError:
        return ('', 204)
#  endregion
#  region getGpsData
@app.route("/hub/{}".format(getGpsData))
def gps_all():
    return str(client.getGpsData())

@app.route("/hub/{}/<attr1>".format(getGpsData))
def gps_attr1(attr1):
    car = client.getGpsData()
    try:
        return str(getattr(car, attr1))
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>".format(getGpsData))
def gps_attr2(attr1, attr2):
    car = client.getGpsData()
    try:
        return str(reduce(getattr,(attr1, attr2), car))
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>/<attr3>".format(getGpsData))
def gps_attr3(attr1, attr2, attr3):
    car = client.getGpsData()
    try:
        return str(reduce(getattr,(attr1, attr2, attr3), car))
    except AttributeError:
        return ('', 204)
#  endregion
#  region getMagnetometerData
@app.route("/")
def magnetometer_all():
    car = client.getBarometerData(barometer_name="Barometer", vehicle_name="PhysXCar")
    return str(car)


@app.route("/hub/{}/<attr1>".format(getMagnetometerData))
def magnetometer_attr1(attr1):
    car = client.getGpsData()
    try:
        return str(getattr(car, attr1))
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>".format(getMagnetometerData))
def magnetometer_attr2(attr1, attr2):
    car = client.getGpsData()
    try:
        return str(reduce(getattr,(attr1, attr2), car))
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>/<attr3>".format(getMagnetometerData))
def magnetometer_attr3(attr1, attr2, attr3):
    car = client.getGpsData()
    try:
        return str(reduce(getattr,(attr1, attr2, attr3), car))
    except AttributeError:
        return ('', 204)
#  endregion
#  endregion


if __name__ == "__main__":

    app.run()
    