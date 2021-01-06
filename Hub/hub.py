import airsim
import cv2
import numpy as np
import os
import base64
import json
import time
from flask import jsonify, Flask, request, send_from_directory
from functools import reduce
from decimal import Decimal

#  region Global var
CarStateSensor = "CarState"
getGpsData = "GpsData"
getImuData = "IMU"
getBarometerData = "Barometer"
getMagnetometerData = "Magnetometer"
getDistanceSensorData = "Distance"
getCollisionInfo = "Collision"

client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()
collision_info = client.simGetCollisionInfo()

app = Flask(__name__)
#  endregion
#  region AirSim Api
@app.route("/hub/disable")
def disable():
    client.enableApiControl(False)
    return("Disable")

@app.route("/hub/enable")
def enable():
    client.enableApiControl(True)
    return("Enable")
#   endregion
#  region getInfo
#  region CarState
@app.route("/hub/{}".format(CarStateSensor))
def sensor_all():
    return json.dumps(client.getCarState(), default=vars)

@app.route("/hub/{}/<attr1>".format(CarStateSensor))
def sensor_attr1(attr1):
    car = client.getCarState()
    try:
        return json.dumps(getattr(car, attr1), default=vars)
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>".format(CarStateSensor))
def sensor_attr2(attr1, attr2):
    car = client.getCarState()
    try:
        return json.dumps(reduce(getattr,(attr1, attr2), car), default=vars)
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>/<attr3>".format(CarStateSensor))
def sensor_attr3(attr1, attr2, attr3):
    car = client.getCarState()
    try:
        return json.dumps(reduce(getattr,(attr1, attr2, attr3), car), default=vars)
    except AttributeError:
        return ('', 204)
#  endregion
#  region getGpsData
@app.route("/hub/{}".format(getGpsData))
def gps_all():
    return json.dumps(client.getGpsData(), default=vars)

@app.route("/hub/{}/<attr1>".format(getGpsData))
def gps_attr1(attr1):
    car = client.getGpsData()
    try:
        return json.dumps(getattr(car, attr1), default=vars)
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>".format(getGpsData))
def gps_attr2(attr1, attr2):
    car = client.getGpsData()
    try:
        return json.dumps(reduce(getattr,(attr1, attr2), car), default=vars)
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>/<attr3>".format(getGpsData))
def gps_attr3(attr1, attr2, attr3):
    car = client.getGpsData()
    try:
        return json.dumps(reduce(getattr,(attr1, attr2, attr3), car), default=vars)
    except AttributeError:
        return ('', 204)
#  endregion
#  region getImuData
@app.route("/hub/{}".format(getImuData))
def imu_all():
    car = client.getImuData(imu_name="Imu", vehicle_name="PhysXCar")
    return json.dumps(car, default=vars)


@app.route("/hub/{}/<attr1>".format(getImuData))
def imu_attr1(attr1):
    car = client.getImuData(imu_name="Imu", vehicle_name="PhysXCar")
    try:
        return json.dumps(getattr(car, attr1), default=vars)
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>".format(getImuData))
def imu_attr2(attr1, attr2):
    car = client.getImuData(imu_name="Imu", vehicle_name="PhysXCar")
    try:
        return json.dumps(reduce(getattr,(attr1, attr2), car), default=vars)
    except AttributeError:
        return ('', 204)
#  endregion
#  region getBarometerData
@app.route("/hub/{}".format(getBarometerData))
def barometer_all():
    car = client.getBarometerData(barometer_name="Barometer", vehicle_name="PhysXCar")
    return json.dumps(car, default=vars)


@app.route("/hub/{}/<attr1>".format(getBarometerData))
def barometer_attr1(attr1):
    car = client.getBarometerData(barometer_name="Barometer", vehicle_name="PhysXCar")
    try:
        return json.dumps(getattr(car, attr1), default=vars)
    except AttributeError:
        return ('', 204)

#  endregion
#  region getMagnetometerData
@app.route("/hub/{}".format(getMagnetometerData))
def magnetometer_all():
    car = client.getMagnetometerData(magnetometer_name="Magnetometer", vehicle_name="PhysXCar")
    return json.dumps(car, default=vars)


@app.route("/hub/{}/<attr1>".format(getMagnetometerData))
def magnetometer_attr1(attr1):
    car = client.getMagnetometerData(magnetometer_name="Magnetometer", vehicle_name="PhysXCar")
    try:
        return json.dumps(getattr(car, attr1), default=vars)
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>".format(getMagnetometerData))
def magnetometer_attr2(attr1,attr2):
    car = client.getMagnetometerData(magnetometer_name="Magnetometer", vehicle_name="PhysXCar")
    try:
        return json.dumps(reduce(getattr,(attr1, attr2), car), default=vars)
    except AttributeError:
        return ('', 204)

#  endregion
#  region getDistanceSensorData
@app.route("/hub/{}".format(getDistanceSensorData))
def distance_all():
    car = client.getDistanceSensorData()
    return json.dumps(car, default=vars)


@app.route("/hub/{}/<attr1>".format(getDistanceSensorData))
def distance_attr1(attr1):
    car = client.getDistanceSensorData()
    try:
        return json.dumps(getattr(car, attr1), default=vars)
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>".format(getDistanceSensorData))
def distance_attr2(attr1,attr2):
    car = client.getDistanceSensorData()
    try:
        return json.dumps(reduce(getattr,(attr1, attr2), car), default=vars)
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>/<attr3>".format(getDistanceSensorData))
def distance_attr3(attr1,attr2,attr3):
    car = client.getDistanceSensorData()
    try:
        return json.dumps(reduce(getattr,(attr1, attr2, attr3), car), default=vars)
    except AttributeError:
        return ('', 204)
#  endregion
#  region getCollisionInfo
@app.route("/hub/{}".format(getCollisionInfo))
def collision_all():
    return json.dumps(collision_info, default=vars)


@app.route("/hub/{}/<attr1>".format(getCollisionInfo))
def collision_attr1(attr1):
    try:
        return json.dumps(getattr(collision_info, attr1), default=vars)
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>".format(getCollisionInfo))
def collision_attr2(attr1, attr2):
    try:
        return json.dumps(reduce(getattr,(attr1, attr2), collision_info), default=vars)
    except AttributeError:
        return ('', 204)
#  endregion
#  region Canera
@app.route("/hub/Camera/<attr1>/scene")
def get_image_scene(attr1):
    responses = client.simGetImages([airsim.ImageRequest(attr1, airsim.ImageType.Scene, False, True)])
    return json.dumps(base64.b64encode(responses[0].image_data_uint8).decode('ascii'), default=vars)
@app.route("/hub/Camera/<attr1>/depthvis")
def get_image_depth_vis(attr1):
    responses = client.simGetImages([airsim.ImageRequest(attr1, airsim.ImageType.DepthVis, False, True)])
    return json.dumps(base64.b64encode(responses[0].image_data_uint8).decode('ascii'), default=vars)
@app.route("/hub/Camera/<attr1>/depthperspective")
def get_image_depth_perspective(attr1):
    responses = client.simGetImages([airsim.ImageRequest(attr1, airsim.ImageType.DepthPerspective, False, True)])
    return json.dumps(base64.b64encode(responses[0].image_data_uint8).decode('ascii'), default=vars)
@app.route("/hub/Camera/<attr1>/segmentation")
def get_image_depth_segmentation(attr1):
    responses = client.simGetImages([airsim.ImageRequest(attr1, airsim.ImageType.Segmentation, False, True)])
    return json.dumps(base64.b64encode(responses[0].image_data_uint8).decode('ascii'), default=vars)
 #airsim.write_file(os.path.normpath('path/11.png'), responses[0].image_data_uint8)
#  endregion
#  endregion
#  region Wether
@app.route("/hub/weather/disable")
def disable_weather():
    client.simEnableWeather(False)
    return("Disable weather")

@app.route("/hub/weather/enable")
def enable_weather():
    client.simEnableWeather(True)
    return("Enable weather")

@app.route("/hub/weather")
def wether():
    rain = request.args.get("Rain")
    if(rain!=None):
        client.simSetWeatherParameter(airsim.WeatherParameter.Rain, float(rain))
        print("works")
    roadwetness = request.args.get("Roadwetness")
    if(roadwetness!=None):
        client.simSetWeatherParameter(airsim.WeatherParameter.Roadwetness, float(roadwetness))
    snow = request.args.get("Snow")
    if(snow!=None):
        client.simSetWeatherParameter(airsim.WeatherParameter.Snow, float(snow))
    road_snow = request.args.get("RoadSnow")
    if(road_snow!=None):
        client.simSetWeatherParameter(airsim.WeatherParameter.RoadSnow, float(road_snow))
    maple_leaf = request.args.get("MapleLeaf")
    if(maple_leaf!=None):
        client.simSetWeatherParameter(airsim.WeatherParameter.MapleLeaf, float(maple_leaf))
    road_leaf = request.args.get("RoadLeaf")
    if(road_leaf!=None):
        client.simSetWeatherParameter(airsim.WeatherParameter.RoadLeaf, float(road_leaf))
    dust = request.args.get("Dust")
    if(dust!=None):
        dust.simSetWeatherParameter(airsim.WeatherParameter.Dust, float(dust))
    fog = request.args.get("Fog")
    if(fog!=None):
        client.simSetWeatherParameter(airsim.WeatherParameter.Fog, float(fog))
    return("Done")


#  endregion
#  region Control
@app.route("/hub/control", methods = ['POST'])
def control():
    throttle = request.args.get("throttle")
    if(throttle!=None):
        if float(throttle) >= 0:
            car_controls.throttle = float(throttle) 
            car_controls.is_manual_gear = False
            car_controls.manual_gear = 0
            car_controls.brake = 0
        else:
            car_controls.is_manual_gear = True
            car_controls.manual_gear = -1
            car_controls.throttle = car_controls.brake = float(throttle)  # AirSim bug
    steering = request.args.get("steering")
    if(steering!=None):
        car_controls.steering = float(steering)
    brake = request.args.get("brake")
    if(brake!=None and car_controls.throttle >= 0 ):
        car_controls.brake = float(brake)
    handbrake = request.args.get("handbrake")
    if(handbrake!=None):
        car_controls.handbrake = eval(handbrake)
    is_manual_gear = request.args.get("is_manual_gear")
    if(is_manual_gear!=None):
        car_controls.is_manual_gear = eval(is_manual_gear)
    manual_gear = request.args.get("manual_gear")
    if(manual_gear!=None):
        car_controls.manual_gear = int(manual_gear)
    gear_immediate = request.args.get("gear_immediate")
    if(gear_immediate!=None):
        car_controls.gear_immediate = eval(gear_immediate)
    client.setCarControls(car_controls)
    return("Done")

@app.route("/hub/getControl")
def get_control():
    return json.dumps(client.getCarControls(), default=vars)

@app.route("/hub/getControl/<attr1>")
def get_control_attr1(attr1):
    car = client.getCarControls()
    try:
        return json.dumps(getattr(car, attr1), default=vars)
    except AttributeError:
        return ('', 204)
    
#  endregion

@app.route("/")
def info():
    return send_from_directory("","help.txt")


button_pressed = True

@app.route("/hub/buttonPressed")
def button_pressed_func():
    global button_pressed
    if(button_pressed):
        button_pressed = False
    else:
        button_pressed = True
    return("Done")

@app.route("/hub/controlState")
def control_state():
    if(button_pressed):
        return("STM")
    return("AI")


acc_data = None

@app.route("/hub/accData", methods = ['POST'])
def acc_data_save():
    global acc_data
    acc_data = request.json
    return("Done")

@app.route("/hub/getAccData")
def get_acc_data():
    return acc_data



if __name__ == "__main__":
    app.run()

