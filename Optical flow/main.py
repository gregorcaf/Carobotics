import numpy as np
import requests
import time
import cv2
import base64

R = 35
Q = 0.0001
posteri_estimate_initial = 0.0
posteri_error_estimate_initial = 1.0
priori_estimate = posteri_estimate_initial
priori_error_estimate = posteri_error_estimate_initial + Q
blending_factor = 0
posteri_estimate = 0
posteri_error_estimate = 0

# Initialize PID
pid_P = -10.0
pid_I = -2.5
pid_D = 0.01
pid_target = 150
pid_error = 0
pid_error_avg = 0
pid_integral = 0
pid_integral_avg = 0

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

    for x in range(currentDepth.shape[0]):
        for y in range(currentDepth.shape[1]):
            if currentDepth[x][y] > 180:
                current_frame[x][y] = 255

    feature_params = dict(maxCorners=300, qualityLevel=0.2, minDistance=2, blockSize=7)

    # strongest corners in first frame
    next_corners = cv2.goodFeaturesToTrack(current_frame, mask=None, **feature_params)

    for i in range(next_corners.shape[0]):
        current_frame = cv2.circle(current_frame, (next_corners[i][0][0], next_corners[i][0][1]), 3, 0, -1)

    xNum = 0

    distCounter = 0
    dist = 0

    for x in range(current_frame.shape[0]):
        for y in range(current_frame.shape[1]):
            if current_frame[x][y] != 0:
                current_frame[x][y] = 255
            else:
                distCounter += 1
                dist += currentDepth[x][y]
                if y > (currentDepth.shape[1]/2 + 10):
                    xNum += 1
                elif y < (currentDepth.shape[1]/2 - 10):
                    xNum -= 1

    dist /= distCounter

    cv2.imshow("img", current_frame)
    cv2.waitKey(1)

    params = {
        "steering": 0.0,
        "throttle": 0.0
    }

    if xNum > 0:
        print("going right")
        params = {
            "steering": 0.5,
            "throttle": 0.25,
        }
    elif xNum < 0:
        print("going left")
        params = {
            "steering": -0.5,
            "throttle": 0.25,
        }

    posteri_estimate_val = posteri_estimate
    priori_estimate = posteri_estimate_val
    priori_error_estimate += Q

    blending_factor = priori_error_estimate / (priori_error_estimate + R)
    posteri_estimate = priori_estimate + blending_factor * (dist - priori_estimate)
    posteri_error_estimate = (1 - blending_factor) * priori_error_estimate
    distance_filtered = posteri_estimate

    # PID control init
    previous_pid_error = pid_error
    previous_pid_integral = pid_integral
    desired_distance = pid_target
    actual_distance = distance_filtered

    # calculate pid error
    pid_error = desired_distance - actual_distance

    # calculate pid integral
    pid_derivative = (pid_error - previous_pid_error) / 0.2
    demo_derivative_val = abs(pid_derivative)
    pid_integral = previous_pid_integral + previous_pid_error * 0.2

    # update previous time
    time_previous = time

    # calculate current thrust with PID values
    params["throttle"] = pid_P * pid_error + pid_I * pid_integral + pid_D * pid_derivative

    print("Points: " + str(xNum))
    print("Distance: " + str(dist))
    print("Speed: " + str(params["throttle"]))

    url = "http://127.0.0.1:5000/hub/control"
    requests.post(url, params=params)

    last_frame = current_frame

    time.sleep(0.1)

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
