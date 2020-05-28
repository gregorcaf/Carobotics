import numpy as np
import cv2
import sounddevice as sd
from scipy.io import wavfile

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

# loading model, configuration, sound
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
fs, sound = wavfile.read("sound.wav")

with open("classes.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

scale_value = 0.5  # 1...fully sized frame
fps_value = 4  # 1...every frame, 2...every second frame, 3...every third frame, etc.
color_value = 0
index = 0

is_sound = False

capture = cv2.VideoCapture("test_1.mp4")

width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) * scale_value)
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale_value)

frames = []

while 1:
    index += 1
    ret, frame = capture.read()

    # check if last frame was captured
    if not ret:
        break

    # DETECTING OBJECTS
    if index % fps_value == 0:
        is_sound = False
        frame = cv2.resize(frame, None, fx=scale_value, fy=scale_value)
        blob = cv2.dnn.blobFromImage(frame, scalefactor=0.00392, size=(416, 416), mean=(0, 0, 0), swapRB=True,
                                     crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        boxes = []
        labels = []
        positions = []
        confidences = []
        region = 0
        font = cv2.FONT_HERSHEY_SIMPLEX

        print("--------")
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.uint8(np.argmax(scores))
                confidence = scores[class_id]

                # DETECTED OBJECT (only for person)
                if confidence > 0.7 and classes[class_id] == "person":
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

        # CREATE BOUNDING BOX
        for i in range(len(boxes)):
            x, y, w, h = boxes[i]

            print("label: ", labels[i])
            print("confidence: ", confidences[i])
            print("position: ", positions[i], "\n")

            if positions[i] > 5:
                color_value = (0, 255, 0)  # green, BGR
            elif positions[i] == 2 or positions[i] == 3 or positions[i] == 4:
                color_value = (0, 0, 255)  # red, BGR
                is_sound = True
            else:
                color_value = (0, 165, 255)  # orange, BGR

            # display bounding box and label
            cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=color_value, thickness=2)
            cv2.putText(frame, text=labels[i], org=(x, y), fontFace=font, fontScale=0.5, color=(255, 255, 0),
                        thickness=2)

        cv2.line(frame, pt1=(width // 5, height), pt2=(width // 5, 0), color=(0, 0, 0), thickness=2)
        cv2.line(frame, pt1=(int(width / (5 / 2)), height), pt2=(int(width / (5 / 2)), 0), color=(0, 0, 0),
                 thickness=2)
        cv2.line(frame, pt1=(int(width / (5 / 3)), height), pt2=(int(width / (5 / 3)), 0), color=(0, 0, 0),
                 thickness=2)
        cv2.line(frame, pt1=(int(width / (5 / 4)), height), pt2=(int(width / (5 / 4)), 0), color=(0, 0, 0),
                 thickness=2)
        cv2.line(frame, pt1=(0, int(height / (3 / 2))), pt2=(width, int(height / (3 / 2))), color=(0, 0, 0),
                 thickness=2)

        cv2.imshow("image", frame)
        k = cv2.waitKey(1)
        if k & 0xFF == 27:
            break

        if is_sound:
            sd.play(sound, fs)
            sd.wait()

        '''
        frames.append(frame)
        print("I: ", index)
        print("------------")

out = cv2.VideoWriter('output_demo.mp4', cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), 28, (width, height))

for i in range(len(frames)):
    print(i)
    out.write(frames[i])
    # cv2.imshow("frame", frames[i])
    # cv2.waitKey(1)
'''

capture.release()
cv2.destroyAllWindows()
