import airsim
import cv2
import numpy as np
import os
import time
from flask import jsonify, Flask
from functools import reduce
CarStateSensor = "sensor"



client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()


app = Flask(__name__)

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



if __name__ == "__main__":
    app.run()
    