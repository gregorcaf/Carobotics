import numpy as np
import requests
import time
import cv2
import base64
# from PIL import Image
from io import StringIO
from datetime import datetime

def readb64(base64_string):
    sbuf = StringIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

# Initialize PID
pid_P = -10
pid_I = 0
pid_D = 0
pidTarget = 1200
pidError = 0
pidIntegral = 0
timePrevious = datetime.now()

lastThrottle = 0
lastSpeed = 0

while True:

    try:
        depthRaw = requests.get("http://127.0.0.1:5000/hub/Camera/1/scene")
        nparrDepth = np.fromstring(base64.b64decode(depthRaw.content), np.uint8)
        image = cv2.imdecode(nparrDepth, cv2.IMREAD_COLOR).copy()

        image = image[image.shape[0] // 2:, :, :]
        height = image.shape[0]
        width = image.shape[1]

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0,50,50])
        upper_red = np.array([10,255,255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)
        lower_red = np.array([170,50,50])
        upper_red = np.array([180,255,255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        output_img = mask0+mask1

        black_left = np.count_nonzero(output_img[:, :width // 2] == 0)
        black_right = np.count_nonzero(output_img[:, width // 2:] == 0)

        """ calculate steering """
        steering = (black_right - black_left) / ((width * height) / 2)

        params = {
            "steering": steering,
            "throttle": 0.1
        }

        url = "http://127.0.0.1:5000/hub/control"
        requests.post(url, params=params)

        print("black left: {}\nblack right: {}\nsteering: {}".format(black_left, black_right, steering))
        print(output_img.shape)
        cv2.imshow("window_name", output_img)
        cv2.waitKey(1)
        wait(1000)

        # print(currentDepth.shape)
        # cv2.imshow("img", currentDepth)
        # cv2.waitKey(1)
    except:
        print("error ni dobo sliko")


# image = cv2.imread("slika.jpg")
height = image.shape[0]
width = image.shape[1]
image = image[height//2:,:,:]


""" ZAZNAVA RDEČE OGRAJE """
# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# lower_red = np.array([0,50,50])
# upper_red = np.array([10,255,255])
# mask0 = cv2.inRange(hsv, lower_red, upper_red)

# lower_red = np.array([170,50,50])
# upper_red = np.array([180,255,255])
# mask1 = cv2.inRange(hsv, lower_red, upper_red)

# output_img = mask0+mask1


""" ZAZNAVA ORANŽNIH ČRT NA CESTI """
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
output_img = cv2.inRange(hsv,(10, 100, 20), (25, 255, 255))


""" count black pixels """
black_left = np.count_nonzero(output_img[:,:width//2] == 0)
black_right = np.count_nonzero(output_img[:,width//2:] == 0)

""" calculate steering """
steering = (black_right - black_left) / ((width * height) / 2)

""" test print for debug """
print("black left: {}\nblack right: {}\nsteering: {}".format(black_left, black_right, steering))
print(output_img.shape)
cv2.imshow("window_name", output_img) 
cv2.waitKey(0)














#     scale_value = 4
#     threshold_factor = 0.2

#     halfWidth = (currentDepth.shape[0]/2) - 2

#     distCounter = 0
#     dist = 0

#     xCounter = 0
#     lrDist = 0

#     for y in range(currentDepth.shape[0]):
#         for x in range(currentDepth.shape[1]):
#             if currentDepth[y][x] > 180 or y > halfWidth:
#                 currentDepth[y][x] = 255
#             else:
#                 distCounter += 1
#                 dist += currentDepth[y][x]
#                 lrDist += x
#                 xCounter += 1
#                 currentDepth[y][x] = 0

#     if distCounter != 0:
#         dist /= distCounter

#     dist *= 10

#     if xCounter != 0:
#         lrDist /= xCounter

#     lrDist -= (currentDepth.shape[1]/2)
#     lrDist /= currentDepth.shape[1]/2

#     cv2.imshow("img", currentDepth)
#     cv2.waitKey(1)

#     timeDiff = datetime.now() - timePrevious
#     timePrevious += timeDiff

#     previous_pid_error = pidError
#     previous_pid_integral = pidIntegral
#     pidError = (pidTarget - dist) + 200
#     pidIntegral = previous_pid_integral + previous_pid_error * (timeDiff.microseconds/1000)
#     pid_derivative = (pidError - previous_pid_error) / (timeDiff.microseconds/1000)
#     currentThrust = pid_P * pidError + pid_I * pidIntegral + pid_D * pid_derivative
#     # print(dist)
#     # print(pidError)
#     # print(currentThrust)

#     speed = (currentThrust/10000)# - lastThrottle
#     lastThrottle = (currentThrust/10000)

#     print(speed)

#     if speed > 0.5:
#         speed = 0.5

#     if speed < -0.5:
#         speed = -0.5

#     params = {
#         "steering": lrDist,
#         "throttle": speed  # (dist - 160) / 300
#     }

#     # print("Points: " + str(xNum))
#     # print("Distance: " + str(dist))
#     # print("Speed: " + str(params["throttle"]))
#     # print("Steering: " + str(params["steering"]))
#     # print("")

#     url = "http://127.0.0.1:5000/hub/control"
#     requests.post(url, params=params)


# print("threshold: ", threshold)
# print("x_coordinates_val: ", x_val)
# print("sum_val: ", x_sum)

# ''' TESTING 
# cv2.imshow("img", frame_1)
# cv2.waitKey(3000)
# cv2.imshow("img", frame_2)
# cv2.waitKey(3000)
# cv2.destroyAllWindows()
# '''