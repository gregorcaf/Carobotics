import numpy as np
import json
import pickle
import requests
import time
import cv2
import base64

text = requests.get("http://127.0.0.1:5000/hub/Camera/0/scene")
nparr = np.fromstring(base64.b64decode(text), np.uint8)
frame_1 = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

time.sleep(0.25)

text = requests.get("http://127.0.0.1:5000/hub/Camera/0/scene")
nparr = np.fromstring(base64.b64decode(text), np.uint8)
frame_2 = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

scale_value = 2
threshold_factor = 0.2

# read image in grayscale
# frame_1 = cv2.imread("middle_1.png", 0)
# frame_2 = cv2.imread("middle_2.png", 0)

# print("TYPE: ", type(frame_1))

# convert from BGR to GRAY
# frame_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
# frame_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)

# resize image todo
# frame_1 = cv2.resize(frame_1, None, fx=scale_value, fy=scale_value)
# frame_2 = cv2.resize(frame_2, None, fx=scale_value, fy=scale_value)

# Parameters for Shi-Tomasi corner detection
feature_params = dict(maxCorners=300, qualityLevel=0.2, minDistance=2, blockSize=7)

# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# strongest corners in first frame
prev_corners = cv2.goodFeaturesToTrack(frame_1, mask=None, **feature_params)
next_corners = cv2.goodFeaturesToTrack(frame_2, mask=None, **feature_params)

next_val, status1, error1 = cv2.calcOpticalFlowPyrLK(frame_1, frame_2, prev_corners, None, **lk_params)
prev_val, status2, error2 = cv2.calcOpticalFlowPyrLK(frame_2, frame_1, next_corners, None, **lk_params)

good_new1 = next_val[status1 == 1]
good_new2 = prev_val[status2 == 1]

val_min = min(len(good_new1), len(good_new2))
x_val = 0
x_sum = 0

# iterate through array
for i in range(val_min):
    a, b = good_new1[i][0], good_new1[i][1]
    c, d = good_new2[i][0], good_new2[i][1]
    frame_1 = cv2.circle(frame_1, (a, b), 3, (0, 255, 0), -1)
    frame_2 = cv2.circle(frame_2, (c, d), 3, (0, 255, 0), -1)

    if a < c:
        x_val += 1
        x_sum += abs(a - c)
    elif a > c:
        x_val -= 1
        x_sum -= abs(a - c)

threshold = int(val_min * threshold_factor)

if threshold >= abs(x_val):
    print("no change")
    params = {
        "steering": 0.0
    }
elif x_val > 0:
    print("going right")
    params = {
        "steering": 0.5
    }
else:
    print("going left")
    params = {
        "steering": -0.5
    }

url = "http://127.0.0.1:5000/hub/control"
requests.post(url, params=params)

print("threshold: ", threshold)
print("x_coordinates_val: ", x_val)
print("sum_val: ", x_sum)

''' TESTING '''
cv2.imshow("img", frame_1)
cv2.waitKey(3000)
cv2.imshow("img", frame_2)
cv2.waitKey(3000)
cv2.destroyAllWindows()
