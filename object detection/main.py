import numpy as np
import cv2
import sounddevice as sd
import soundfile as sf
import librosa
import sys

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

# loading model and configuration
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

with open("classes.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

sound, fs = librosa.load('sound.mp3')

# img = cv2.imread("street_1.jpg")
# img = cv2.resize(img, None, fx=0.7, fy=0.7)

capture = cv2.VideoCapture("street.mp4")
color_value = 0
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

i = 0
while capture.isOpened():
    i += 1
    ret, frame_1 = capture.read()

    # DETECTING OBJECTS
    if i % 4 == 0:
        # cv2.resize(frame_1, None, fx=0.7, fy=0.7)
        blob = cv2.dnn.blobFromImage(frame_1, scalefactor=0.00392, size=(416, 416), mean=(0, 0, 0), swapRB=True,
                                     crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        boxes = []
        labels = []
        positions = []
        confidences = []
        region = 0
        font = cv2.FONT_HERSHEY_SIMPLEX

        print("image width: ", width)
        print("image height: ", height)
        print("--------")
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.uint8(np.argmax(scores))
                confidence = scores[class_id]

                # DETECTED OBJECT
                if confidence > 0.7:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # bottom left coordinate of box
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    labels.append(classes[class_id])
                    confidences.append(confidence)

                    # oddaljenost do spodnjega roba <= 1/3 visine slike => WARNING
                    if height - y - h <= height / 3:
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
            print("region: ", region, "\n")

            if positions[i] > 5:
                # green
                color_value = (0, 255, 0)  # BGR
            elif positions[i] == 2 or positions[i] == 3 or positions[i] == 4:
                # red
                color_value = (0, 0, 255)  # BGR
            else:
                # orange
                color_value = (0, 165, 255)  # BGR

            # display bounding box and label
            cv2.rectangle(frame_1, pt1=(x, y), pt2=(x + w, y + h), color=color_value, thickness=2)
            cv2.line(frame_1, pt1=(width // 5, height), pt2=(width // 5, 0), color=(0, 0, 0), thickness=2)
            cv2.line(frame_1, pt1=(int(width / (5 / 2)), height), pt2=(int(width / (5 / 2)), 0), color=(0, 0, 0), thickness=2)
            cv2.line(frame_1, pt1=(int(width / (5 / 3)), height), pt2=(int(width / (5 / 3)), 0), color=(0, 0, 0), thickness=2)
            cv2.line(frame_1, pt1=(int(width / (5 / 4)), height), pt2=(int(width / (5 / 4)), 0), color=(0, 0, 0), thickness=2)
            cv2.line(frame_1, pt1=(0, int(height / (3 / 2))), pt2=(width, int(height / (3 / 2))), color=(0, 0, 0), thickness=2)
            cv2.putText(frame_1, text=labels[i], org=(x, y), fontFace=font, fontScale=0.5, color=(255, 255, 0), thickness=2)

            if color_value == (0, 0, 255):
                sd.play(sound, fs)
                sd.wait()

        cv2.imshow("image", frame_1)
        k = cv2.waitKey(1)
        if k == 27:
            break
        # play the sound
        print("------------")


cv2.destroyAllWindows()
capture.release()

