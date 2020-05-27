import numpy as np
import time
import cv2

start_time = time.time()
scale_value = 0.3

# read image in grayscale
frame_1 = cv2.imread("longboard_3.png", 0)
frame_2 = cv2.imread("longboard_1.png", 0)

# resize image
frame_1 = cv2.resize(frame_1, None, fx=scale_value, fy=scale_value)
frame_2 = cv2.resize(frame_2, None, fx=scale_value, fy=scale_value)

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

'''
for i, (new, old) in enumerate(zip(good_new1, good_old1)):
    a, b = new.ravel()
    points_1.append(np.array([a, b]))
    frame_1 = cv2.circle(frame_1, (a, b), 3, (0, 255, 0), -1)
'''

val_min = min(len(good_new1), len(good_new2))
x_val = 0
x_sum = 0
for i in range(val_min):
    a, b = good_new1[i][0], good_new1[i][1]
    c, d = good_new2[i][0], good_new2[i][1]
    # frame_1 = cv2.circle(frame_1, (a, b), 3, (0, 255, 0), -1)
    # frame_2 = cv2.circle(frame_2, (c, d), 3, (0, 255, 0), -1)

    if a < c:
        x_val += 1
        x_sum += abs(a - c)
    else:
        x_val -= 1
        x_sum -= abs(a - c)


if x_val > 0:
    print("going right")
else:
    print("going left")

print("x_coordinates_val: ", x_val)
print("sum_val: ", x_sum)
print("--- %s seconds ---" % (time.time() - start_time))

'''
cv2.imshow("img", frame_1)
cv2.waitKey(3000)
cv2.imshow("img", frame_2)
cv2.waitKey(3000)
cv2.destroyAllWindows()
'''