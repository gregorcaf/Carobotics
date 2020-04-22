import requests

import sounddevice as sd
import queue
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

# 1 for generated / 2 for recorded
amplification = 2

# 15 for generated / 15 for recorded
middleValue = 15

# 2 for generated / 1 for recorded
steeringChannel = 1

inHigh = 0
currentChannel = 0
samplesSinceHigh = 0
channels = np.zeros(8)
channels.fill(middleValue)

cleaned_channels = np.zeros(8)

q = queue.Queue()


#gumb nimam pojma kaj bi mogo naredit
def send_to_hub(throttle, steering, handbrake):
    url = "http://127.0.0.1:5000/hub/control"
    params = {
        "throttle" : throttle,
        "steering" : steering
        #,"handbrake" : handbrake
    }
    return requests.post(url, params=params)


def update_plot(frame):

    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines


def print_sound(indata, outdata, frames, time, status):
    global inHigh
    global currentChannel
    global samplesSinceHigh
    global channels
    global cleaned_channels
    global amplification
    global middleValue

    data_to_plot = np.zeros((1, 8))

    data = indata*100

    sample_time = 1.0/44100
    for index, value in enumerate(data):
        if value > 30 and inHigh == 0:
            inHigh = 1
            pulse_time = sample_time * samplesSinceHigh * 10000
            samplesSinceHigh = 0
            print(pulse_time)
            if pulse_time > 30:
                currentChannel = 0
                continue

            if currentChannel < 8:
                if abs(channels[currentChannel] - pulse_time) < 0.7:
                    channels[currentChannel] = pulse_time
                else:
                    channels[currentChannel] -= (channels[currentChannel] - pulse_time)/25
            currentChannel += 1

        elif value < -15 and inHigh == 1:
            inHigh = 0

        data_to_plot += channels
        samplesSinceHigh += 1

        if index == 128 or index == 256 or index == 384 or index == 512:
            data_to_plot /= 128
            data_to_plot -= middleValue
            for i in range(8):
                if abs(data_to_plot[0][i]) < 0.5:
                    data_to_plot[0][i] = 0

                data_to_plot[0][i] /= (8/amplification)
                if data_to_plot[0][i] > 1:
                    data_to_plot[0][i] = 1
                elif data_to_plot[0][i] < -1:
                    data_to_plot[0][i] = -1

            cleaned_channels = data_to_plot
            q.put(data_to_plot)
            data_to_plot = np.zeros((1, 8))

    send_to_hub(cleaned_channels[0][0], cleaned_channels[0][steeringChannel], 0)


if __name__ == "__main__":
    length = int(10 * 44100 / 1000)
    plotdata = np.zeros((length, 8))
    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    ax.legend(['channel {}'.format(c) for c in range(8)],
              loc='top right')
    ax.axis((0, length, -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)
    ani = FuncAnimation(fig, update_plot, interval=10, blit=True)

    with sd.Stream(channels=1, callback=print_sound):
        plt.show()
