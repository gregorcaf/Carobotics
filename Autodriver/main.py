import numpy as np
import math


class KalmanFilter(object):
    def __init__(self, process_variance, estimated_measurement_variance):
        self.process_variance = process_variance
        self.estimated_measurement_variance = estimated_measurement_variance
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0

    def input_latest_noisy_measurement(self, measurement):
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.process_variance

        blending_factor = priori_error_estimate / (priori_error_estimate + self.estimated_measurement_variance)
        self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
        self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate

    def get_latest_estimated_measurement(self):
        return self.posteri_estimate


class AutoDriver():
    def __init__(self, objectMass, objectMaxThrustForce, objectNeutralBreakForce, desiredDistance):
        # objectMass - masa vozila v kg
        # objectMaxThrustForce - maksimalna sila potiska motorjev v N
        # objectNeutralBreakForce - sila v N, s katero vozilo zavira če je moč motorja 0N
        # desired distance - željena oddaljenost objekta od tarče

        self.object_mass = objectMass
        self.object_max_thrust_force = objectMaxThrustForce
        self.object_neutral_break_force = objectNeutralBreakForce

        # Initialize defaults
        self.distance_filtered = 0
        self.time_previous = 0
        self.current_thrust = 0
        self.car_data = [self.object_mass, self.object_max_thrust_force, self.object_neutral_break_force]
        self.history_data = []
        self.times = []
        self.times_delta = []

        # Initialize kalman
        self.R = 35
        self.Q = 0.0001
        self.posteri_estimate_initial = 0.0
        self.posteri_error_estimate_initial = 1.0
        self.priori_estimate = self.posteri_estimate_initial
        self.priori_error_estimate = self.posteri_error_estimate_initial + self.Q
        self.blending_factor = 0
        self.posteri_estimate = 0
        self.posteri_error_estimate = 0

        # Initialize PID
        self.pid_P = -10.0
        self.pid_I = -2.5
        self.pid_D = 0.01
        self.pid_target = desiredDistance
        self.pid_error = 0
        self.pid_error_avg = 0
        self.pid_integral = 0
        self.pid_integral_avg = 0

    def updateMeasurement(self, time, distance):
        # time - čas zajema, v s
        # distance - izmerjena oddaljenost do objekta pred vozilom v m

        # Kalman filter
        posteri_estimate_val = self.posteri_estimate
        self.priori_estimate = posteri_estimate_val
        self.priori_error_estimate += self.Q

        self.blending_factor = self.priori_error_estimate / (self.priori_error_estimate + self.R)
        self.posteri_estimate = self.priori_estimate + self.blending_factor * (distance - self.priori_estimate)
        self.posteri_error_estimate = (1 - self.blending_factor) * self.priori_error_estimate
        self.distance_filtered = self.posteri_estimate

        # PID control init
        previous_pid_error = self.pid_error
        previous_pid_integral = self.pid_integral
        desired_distance = self.pid_target
        actual_distance = self.distance_filtered

        # calculate pid error
        self.pid_error = desired_distance - actual_distance

        # calculate pid integral
        time_val = time - self.time_previous
        pid_derivative = (self.pid_error - previous_pid_error) / time_val
        demo_derivative_val = abs(pid_derivative)
        self.pid_integral = previous_pid_integral + previous_pid_error * time_val

        # update previous time
        self.time_previous = time
        self.times.append(time)
        self.times_delta.append(time_val)

        # calculate current thrust with PID values
        self.current_thrust = self.pid_P * self.pid_error + self.pid_I * self.pid_integral + self.pid_D * pid_derivative

        # append data to history
        data = np.array([time, time_val, self.current_thrust, self.blending_factor])
        self.history_data.append(data)
        i = len(self.history_data) - 1
        # DEMO TESTING HISTORY
        # print("history data: ", self.history_data[i])

        # calculate stopping distance with fraction = 1
        velocity = abs(self.current_thrust * 60)
        bd = (math.pow(velocity, 2)) / (1 * 2 * 9.81)
        rd = self.current_thrust * 0.5
        stopping_distance = rd * bd
        # print("stop distance: ", stopping_distance)

    @property
    def distanceFiltered(self):
        # print("actual distance: ", self.distance_filtered)
        return self.distance_filtered

    @property
    def thrust(self):
        # print("thrust: ", self.current_thrust)
        return self.current_thrust
