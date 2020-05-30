import numpy as np
import requests
import time
import cv2
import base64

text = requests.get("http://127.0.0.1:5000/hub/Camera/0/scene")
nparrFrame = np.frombuffer(base64.b64decode(text.content), np.uint8)
last_frame = cv2.imdecode(nparrFrame, cv2.IMREAD_GRAYSCALE)

depthRaw = requests.get("http://127.0.0.1:5000/hub/Camera/1/depthvis")
nparrDepth = np.frombuffer(base64.b64decode(depthRaw.content), np.uint8)
currentDepth = cv2.imdecode(nparrDepth, cv2.IMREAD_GRAYSCALE)

for x in range(currentDepth.shape[0]):
    for y in range(currentDepth.shape[1]):
        if currentDepth[x][y] > 180:
            last_frame[x][y] = 255

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

    for x in range(current_frame.shape[0]):
        for y in range(current_frame.shape[1]):
            if current_frame[x][y] != 0:
                current_frame[x][y] = 255
            else:
                if y > (currentDepth.shape[1]/2 + 10):
                    xNum += 1
                elif y < (currentDepth.shape[1]/2 - 10):
                    xNum -= 1

    print(xNum)

    cv2.imshow("img", current_frame)
    cv2.waitKey(1)

    params = {
        "steering": 0.0,
        "throttle": -1
    }

    '''if xNum > 0:
        print("going right")
        params = {
            "steering": 0.5,
            "throttle": 1,
        }
    elif xNum < 0:
        print("going left")
        params = {
            "steering": -0.5,
            "throttle": 1,
        }
    '''
    url = "http://127.0.0.1:5000/hub/control"
    requests.post(url, params=params)

    last_frame = current_frame

    time.sleep(0.25)

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
