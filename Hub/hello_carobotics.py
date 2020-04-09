import airsim
import cv2
import numpy as np
import os
import setup_path 
import time

# connect to the AirSim simulator 
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

# izpis podatkov v file
file = open("carobotics_results.txt","a") 
print("START\n")

for i in range(20):
    car_controls.is_manual_gear = False
    car_controls.throttle = 0.5

    if (i == 5):
        # zavoj v levo
        car_controls.throttle = 0.2
        car_controls.steering = -0.3
    elif (i == 10):
        # zavoj v desno
        car_controls.throttle = 0.2
        car_controls.steering = 0.3
    else:
        car_controls.steering = 0
    
    client.setCarControls(car_controls)

    car_state = client.getCarState()
    buffer = "Speed: {}\t Gear: {}\tRPM: {}\tHandbrake: {} \n".format(car_state.speed, car_state.gear, car_state.rpm, car_state.handbrake)
    file.write(buffer)
    time.sleep(1)

file.close()

car_controls.throttle = 0
car_controls.brake = 1
client.setCarControls(car_controls)

client.reset()
client.enableApiControl(False)