import numpy as np
import requests
import time
import cv2
import base64
from datetime import datetime

# Initialize PID
pid_P = -15
pid_I = -1.5
pid_D = 0.1
pidTarget = 270
pidError = 0
pidIntegral = 0
timePrevious = datetime.now()

lastThrottle = 0
lastSpeed = 0

while True:

    # time.sleep(0.25)

    depthRaw = requests.get("http://127.0.0.1:5000/hub/Camera/1/depthvis")
    nparrDepth = np.fromstring(base64.b64decode(depthRaw.content), np.uint8)
    currentDepth = cv2.imdecode(nparrDepth, cv2.IMREAD_GRAYSCALE).copy()

    scale_value = 4
    threshold_factor = 0.2

    halfWidth = (currentDepth.shape[0]/2) - 2

    distCounter = 0
    dist = 0

    xCounter = 0
    lrDist = 0

    for y in range(currentDepth.shape[0]):
        for x in range(currentDepth.shape[1]):
            if currentDepth[y][x] > 180 or y > halfWidth:
                currentDepth[y][x] = 255
            else:

                distCounter += 1
                dist += currentDepth[y][x]
                lrDist += x
                xCounter += 1
                currentDepth[y][x] = 0

    if distCounter != 0:
        dist /= distCounter
    else:
        dist = pidTarget

    dist *= 10
    dist -= 1000

    if xCounter != 0:
        lrDist /= xCounter

    lrDist -= (currentDepth.shape[1]/2)
    lrDist /= currentDepth.shape[1]/2

    cv2.imshow("img", currentDepth)
    cv2.waitKey(1)

    timeDiff = datetime.now() - timePrevious
    timePrevious += timeDiff

    previous_pid_error = pidError
    previous_pid_integral = pidIntegral
    pidError = (pidTarget - dist) + 270
    pidIntegral = previous_pid_integral + previous_pid_error * (timeDiff.microseconds/1000000)
    pid_derivative = (pidError - previous_pid_error) / (timeDiff.microseconds/1000000)
    currentThrust = pid_P * pidError + pid_I * pidIntegral + pid_D * pid_derivative

    speed = (currentThrust/12000)
    lastThrottle = (currentThrust/12000)

    print(dist)
    print(speed)

    if speed > 0.3:
        speed = 0.3

    if speed < -0.3:
        speed = -0.3

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
