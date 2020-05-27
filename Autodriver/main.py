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
        """
        Inicializacija AutoLander implementacije.
        Tu prejmete informacije o letalniku.

        objectMass - float
            masa vozila v kg

        objectMaxThrustForce - float
            maksimalna sila potiska motorjev v N

        objectNeutralBreakForce - float
            sila v N, s katero vozilo zavira če je moč motorja 0N

        desired distance - float
            željena oddaljenost objekta od tarče
        """

        # Initialize defaults
        self.distanceFilt = 0
        self.timePrevious = 0
        self.currentThrust = 0

        # Initialize kalman
        self.Q = 0.0001
        self.R = 35
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
        self.pidTarget = desiredDistance
        self.pidError = 0
        self.pidIntegral = 0
        
    def updateMeasurement(self, time, distance):
        """
        Prejemek posamezne meritve.
        time - float
            čas zajema, v s

        distance - float
            izmerjena oddaljenost do objekta pred vozilom v m
        """

        # Kalman filter
        self.priori_estimate = self.posteri_estimate
        self.priori_error_estimate = self.priori_error_estimate + self.Q

        self.blending_factor = self.priori_error_estimate / (self.priori_error_estimate + self.R)
        self.posteri_estimate = self.priori_estimate + self.blending_factor * (distance - self.priori_estimate)
        self.posteri_error_estimate = (1 - self.blending_factor) * self.priori_error_estimate
        self.distanceFilt = self.posteri_estimate

        # PID controll
        previous_pid_error = self.pidError
        previous_pid_integral = self.pidIntegral
        self.pidError = self.pidTarget - self.distanceFilt
        self.pidIntegral = previous_pid_integral + previous_pid_error * (time - self.timePrevious)
        pid_derivative = (self.pidError - previous_pid_error) / (time - self.timePrevious)
        self.currentThrust = self.pid_P * self.pidError + self.pid_I * self.pidIntegral + self.pid_D * pid_derivative

        self.timePrevious = time

    @property
    def distanceFiltered(self):
        """
        Tukaj vrnete trenutno oddaljenost ocenjeno z filtri.
        To omogoča kasnejši izris, vrnete vašo interno spremenljivko.
        """
        return self.distanceFilt
    
    @property
    def thrust(self):
        """
        Tukaj vrnete relativno količino moči motorjev, vrednost med 0 in 1.
        """
        return self.currentThrust

