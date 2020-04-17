import requests

#gumb nimam pojma kaj bi mogo naredit
def send_to_hub(throttle, steering, handbrake):
    url = "http://127.0.0.1:5000/hub/control"
    params = {
        "throttle" : throttle,
        "steering" : steering
        #,"handbrake" : handbrake
    }
    return requests.post(url, params=params)
    

if __name__ == "__main__":
    send_to_hub(1,-0.25,0)
    print("done")
