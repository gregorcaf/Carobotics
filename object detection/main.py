import numpy as np
import cv2
import tensorflow as tf

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

img = cv2.imread("street_2.jpg")
img = cv2.resize(img, None, fx=1, fy=1)
height, width, channels = img.shape

# DETECTING OBJECTS
# swapRB = True (cv2 works with bgr instead of rgb)
blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(416, 416), mean=(0, 0, 0), swapRB=True, crop=False)
net.setInput(blob)
outs = net.forward(output_layers)

# REGIONS OF DETECTED OBJECTS
# 1...bottom left
# 2...bottom middle left
# 3...bottom middle
# 4...bottom middle right
# 5...bottom right
# 6...top left
# 7...top middle left
# 8...top middle
# 9...top middle right
# 10...top right

boxes = []
labels = []
positions = []
confidences = []
region = 0
font = cv2.FONT_HERSHEY_PLAIN

print("width: ", width)
print("height: ", height)
print("--------")
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.7:
            # DETECTED OBJECT
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # BOUNDING BOX
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            labels.append(classes[class_id])
            confidences.append(confidence)

            if center_y >= height / (3 / 2):
                if center_x <= width / 5:
                    positions.append(1)  # 1...bottom left
                elif center_x <= width / (5 / 2):
                    positions.append(2)  # 2...bottom middle left
                elif center_x <= width / (5 / 3):
                    positions.append(3)  # 3...bottom middle
                elif center_x <= width / (5 / 4):
                    positions.append(4)  # 4...bottom middle right
                else:
                    positions.append(5)  # 5...bottom right
            else:
                if center_x <= width / 5:
                    positions.append(6)  # 6...top left
                elif center_x <= width / (5 / 2):
                    positions.append(7)  # 7...top middle left
                elif center_x <= width / (5 / 3):
                    positions.append(8)  # 6...top middle
                elif center_x <= width / (5 / 4):
                    positions.append(9)  # 9...top middle right
                else:
                    positions.append(10)  # 10...top right

for i in range(len(boxes)):
    x, y, w, h = boxes[i]

    if positions[i] == 1:
        region = "bottom left"
    elif positions[i] == 2:
        region = "bottom middle left"
    elif positions[i] == 3:
        region = "bottom middle"
    elif positions[i] == 4:
        region = "bottom middle right"
    elif positions[i] == 5:
        region = "bottom right"
    elif positions[i] == 6:
        region = "top left"
    elif positions[i] == 7:
        region = "top middle left"
    elif positions[i] == 8:
        region = "top middle"
    elif positions[i] == 9:
        region = "top middle right"
    elif positions[i] == 10:
        region = "top right"

    print("label: ", labels[i])
    print("confidence: ", confidences[i])
    print("region: ", region)

    if positions[i] > 5:
        print("position: top 2/3\n")
        color_value = (0, 255, 0)  # BGR
    else:
        print("thirds: bottom 1/3\n")
        color_value = (0, 0, 255)  # BGR

    cv2.rectangle(img, pt1=(x, y), pt2=(x + w, y + h), color=color_value, thickness=2)
    cv2.putText(img, labels[i], (x, y), font, 1, (255, 255, 0), 2)

cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
