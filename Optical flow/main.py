import numpy as np
import requests
import time
import cv2
import base64

# text = requests.get("http://127.0.0.1:5000/hub/Camera/0/scene")
# nparrFrame = np.frombuffer(base64.b64decode(text.content), np.uint8)
# last_frame = cv2.imdecode(nparrFrame, cv2.IMREAD_GRAYSCALE)
#
# depthRaw = requests.get("http://127.0.0.1:5000/hub/Camera/0/depthvis")
# nparrDepth = np.frombuffer(base64.b64decode(depthRaw.content), np.uint8)
# currentDepth = cv2.imdecode(nparrDepth, cv2.IMREAD_GRAYSCALE)
#
# for x in range(currentDepth.shape[0]):
#     for y in range(currentDepth.shape[1]):
#         if currentDepth[x][y] > 180:
#             last_frame[x][y] = 255

while True:

    time.sleep(0.25)

    text = requests.get("http://127.0.0.1:5000/hub/Camera/0/scene")
    nparrFrame = np.fromstring(base64.b64decode(text.content), np.uint8)
    current_frame = cv2.imdecode(nparrFrame, cv2.IMREAD_COLOR)

    cv2.imshow("img", current_frame)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

    depthRaw = requests.get("http://127.0.0.1:5000/hub/Camera/0/depthvis")
    nparrDepth = np.fromstring(base64.b64decode(depthRaw.content), np.uint8)
    currentDepth = cv2.imdecode(nparrDepth, cv2.IMREAD_GRAYSCALE)

    cv2.imshow("img", currentDepth)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

    segRaw = requests.get("http://127.0.0.1:5000/hub/Camera/0/segmentation")
    nparrSeg = np.fromstring(base64.b64decode(segRaw.content), np.uint8)
    currentSeg = cv2.imdecode(nparrSeg, cv2.IMREAD_GRAYSCALE)

    cv2.imshow("img", currentSeg)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
    break

    scale_value = 2
    threshold_factor = 0.2

    # for x in range(currentDepth.shape[0]):
    #    for y in range(currentDepth.shape[1]):
    #        if currentDepth[x][y] > 180:
    #            current_frame[x][y] = 255

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
    prev_corners = cv2.goodFeaturesToTrack(last_frame, mask=None, **feature_params)
    next_corners = cv2.goodFeaturesToTrack(current_frame, mask=None, **feature_params)

    next_val, status1, error1 = cv2.calcOpticalFlowPyrLK(last_frame, current_frame, prev_corners, None, **lk_params)
    prev_val, status2, error2 = cv2.calcOpticalFlowPyrLK(current_frame, last_frame, next_corners, None, **lk_params)

    good_new1 = next_val[status1 == 1]
    good_new2 = prev_val[status2 == 1]

    val_min = min(len(good_new1), len(good_new2))
    x_val = 0
    x_sum = 0

    # iterate through array
    for i in range(val_min):
        a, b = good_new1[i][0], good_new1[i][1]
        c, d = good_new2[i][0], good_new2[i][1]
        frame_1 = cv2.circle(last_frame, (a, b), 3, (0, 255, 0), -1)
        frame_2 = cv2.circle(current_frame, (c, d), 3, (0, 255, 0), -1)

        if a < c:
            x_val += 1
            x_sum += abs(a - c)
        elif a > c:
            x_val -= 1
            x_sum -= abs(a - c)

    cv2.imshow("img", current_frame)
    cv2.waitKey(5000)
    cv2.imshow("img", currentDepth)
    cv2.waitKey(5000)
    cv2.imshow("img", currentSeg)
    cv2.waitKey(5000)
    break
    threshold = int(val_min * threshold_factor)

<<<<<<< HEAD
=======
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
params = 0

if threshold >= abs(x_val):
    print("no change")
>>>>>>> 94a32aaf04aa40ac9f028ac008b0d30d456b2a3b
    params = {
        "steering": 0.0
    }

    if threshold >= abs(x_val):
        print("no change")
        params = {
            "steering": 0.0,
            "throttle": 0.0,
        }
    elif x_val > 0:
        print("going right")
        params = {
            "steering": 0.5,
            "throttle": 0.5,
        }
    else:
        print("going left")
        params = {
            "steering": -0.5,
            "throttle": 0.5,
        }

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
