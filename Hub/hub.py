import airsim
import cv2
import numpy as np
import os
import time
from flask import jsonify, Flask
from functools import reduce

CarStateSensor = "CarState"
getGpsData = "GpsData"
getImuData = "IMU"
getBarometerData = "Barometer"
getMagnetometerData = "Magnetometer"
getDistanceSensorData = "Distance"
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()


app = Flask(__name__)

@app.route("/hub/disable")
def disable():
    client.enableApiControl(False)
    return("Disable")

@app.route("/hub/enable")
def enable():
    client.enableApiControl(True)
    return("Enable")

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
#  region getImuData
@app.route("/hub/{}".format(getImuData))
def imu_all():
    car = client.getImuData(imu_name="Imu", vehicle_name="PhysXCar")
    return str(car)


@app.route("/hub/{}/<attr1>".format(getImuData))
def imu_attr1(attr1):
    car = client.getImuData(imu_name="Imu", vehicle_name="PhysXCar")
    try:
        return str(getattr(car, attr1))
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>".format(getImuData))
def imu_attr2(attr1, attr2):
    car = client.getImuData(imu_name="Imu", vehicle_name="PhysXCar")
    try:
        return str(reduce(getattr,(attr1, attr2), car))
    except AttributeError:
        return ('', 204)
#  endregion
#  region getBarometerData
@app.route("/hub/{}".format(getBarometerData))
def barometer_all():
    car = client.getBarometerData(barometer_name="Barometer", vehicle_name="PhysXCar")
    return str(car)


@app.route("/hub/{}/<attr1>".format(getBarometerData))
def barometer_attr1(attr1):
    car = client.getBarometerData(barometer_name="Barometer", vehicle_name="PhysXCar")
    try:
        return str(getattr(car, attr1))
    except AttributeError:
        return ('', 204)

#  endregion
#  region getMagnetometerData
@app.route("/hub/{}".format(getMagnetometerData))
def magnetometer_all():
    car = client.getMagnetometerData(magnetometer_name="Magnetometer", vehicle_name="PhysXCar")
    return str(car)


@app.route("/hub/{}/<attr1>".format(getMagnetometerData))
def magnetometer_attr1(attr1):
    car = client.getMagnetometerData(magnetometer_name="Magnetometer", vehicle_name="PhysXCar")
    try:
        return str(getattr(car, attr1))
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>".format(getMagnetometerData))
def magnetometer_attr2(attr1,attr2):
    car = client.getMagnetometerData(magnetometer_name="Magnetometer", vehicle_name="PhysXCar")
    try:
        return str(reduce(getattr,(attr1, attr2), car))
    except AttributeError:
        return ('', 204)

#  endregion
#  region getDistanceSensorData
@app.route("/hub/{}".format(getDistanceSensorData))
def distance_all():
    car = client.getDistanceSensorData();
    return str(car)


@app.route("/hub/{}/<attr1>".format(getDistanceSensorData))
def distance_attr1(attr1):
    car = client.getDistanceSensorData();
    try:
        return str(getattr(car, attr1))
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>".format(getDistanceSensorData))
def distance_attr2(attr1,attr2):
    car = client.getDistanceSensorData();
    try:
        return str(reduce(getattr,(attr1, attr2), car))
    except AttributeError:
        return ('', 204)

@app.route("/hub/{}/<attr1>/<attr2>/<attr3>".format(getDistanceSensorData))
def distance_attr3(attr1,attr2,attr3):
    car = client.getDistanceSensorData();
    try:
        return str(reduce(getattr,(attr1, attr2, attr3), car))
    except AttributeError:
        return ('', 204)
#  endregion
#  endregion


def getImage():
    responses = client.simGetImages([
    airsim.ImageRequest("0", airsim.ImageType.DepthVis),  #depth visualization image
    airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, True), #depth in perspective projection
    airsim.ImageRequest("3", airsim.ImageType.Scene), #scene vision image in png format
    airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])  #scene vision image in uncompressed RGB array
    print('Retrieved images: %d', len(responses))
    myint = 7
    print(responses[2])
    #for response in responses:
    #    filename = '/Users/nejcfirbas/Desktop/' + str(myint)
    #    myint = myint + 1
    #    if response.pixels_as_float:
    #        print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
    #        airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
    #    elif response.compress: #png format
    #        print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
    #        airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
    #    else: #uncompressed array
    #        print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
    #        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) # get numpy array
    #        img_rgb = img1d.reshape(response.height, response.width, 3) # reshape array to 3 channel image array H X W X 3
    #        cv2.imwrite(os.path.normpath(filename + '.png'), img_rgb) # write to png 


if __name__ == "__main__":
    getImage()
    app.run()

    