import numpy as np
import requests
import time
import cv2
import base64
from datetime import datetime

# Initialize PID
pid_P = -7
pid_I = -3
pid_D = 0.01
pidTarget = 1400
pidError = 0
pidIntegral = 0
timePrevious = datetime.now()

lastThrottle = 0
lastSpeed = 0

while True:

    # time.sleep(0.25)

    text = requests.get("http://127.0.0.1:5000/hub/Camera/0/scene")
    nparrFrame = np.fromstring(base64.b64decode(text.content), np.uint8)
    current_frame = cv2.imdecode(nparrFrame, cv2.IMREAD_GRAYSCALE).copy()

    depthRaw = requests.get("http://127.0.0.1:5000/hub/Camera/1/depthvis")
    nparrDepth = np.fromstring(base64.b64decode(depthRaw.content), np.uint8)
    currentDepth = cv2.imdecode(nparrDepth, cv2.IMREAD_GRAYSCALE).copy()

    scale_value = 4
    threshold_factor = 0.2

    halfWidth = (currentDepth.shape[0]/2) - 2

    for y in range(currentDepth.shape[0]):
        for x in range(currentDepth.shape[1]):
            if currentDepth[y][x] > 180 or y > halfWidth:
                current_frame[y][x] = 255
            else:
                current_frame[y][x] = 0

    cv2.imshow("img", current_frame)
    cv2.waitKey(1)

    distCounter = 0
    dist = 0

    xCounter = 0
    lrDist = 0

    for y in range(current_frame.shape[0]):
        for x in range(current_frame.shape[1]):
            if current_frame[y][x] == 0:
                distCounter += 1
                dist += currentDepth[y][x]
                lrDist += x
                xCounter += 1

    if distCounter != 0:
        dist /= distCounter

    dist *= 10

    if xCounter != 0:
        lrDist /= xCounter

    lrDist -= (currentDepth.shape[1]/2)
    lrDist /= currentDepth.shape[1]/2

    cv2.imshow("img", current_frame)
    cv2.waitKey(1)

    timeDiff = datetime.now() - timePrevious
    timePrevious += timeDiff

    previous_pid_error = pidError
    previous_pid_integral = pidIntegral
    pidError = (pidTarget - dist) + 200
    pidIntegral = previous_pid_integral + previous_pid_error * (timeDiff.microseconds/1000)
    pid_derivative = (pidError - previous_pid_error) / (timeDiff.microseconds/1000)
    currentThrust = pid_P * pidError + pid_I * pidIntegral + pid_D * pid_derivative
    # print(dist)
    # print(pidError)
    # print(currentThrust)

    speed = (currentThrust/1000000) - lastThrottle
    lastThrottle = (currentThrust/1000000)

    print(speed)

    if speed > 0.5:
        speed = 0.5

    if speed < -0.5:
        speed = -0.5

    lastSpeed = speed

    params = {
        "steering": lrDist,
        "throttle": speed  # (dist - 160) / 300
    }

    # print("Points: " + str(xNum))
    # print("Distance: " + str(dist))
    # print("Speed: " + str(params["throttle"]))
    # print("Steering: " + str(params["steering"]))
    # print("")

    url = "http://127.0.0.1:5000/hub/control"
    requests.post(url, params=params)

    last_frame = current_frame

print("threshold: ", threshold)
print("x_coordinates_val: ", x_val)
print("sum_val: ", x_sum)

''' TESTING 
cv2.imshow("img", frame_1)
cv2.waitKey(3000)
cv2.imshow("img", frame_2)
cv2.waitKey(3000)
cv2.destroyAllWindows()
'''
