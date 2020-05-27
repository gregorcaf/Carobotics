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
        '''
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
        '''
        self.distanceFilt = 0
        self.objectNeutralBreakForce = objectNeutralBreakForce

    def updateMeasurement(self, time, distance):
        '''
        Prejemek posamezne meritve.
        time - float
            čas zajema, v s

        distance - float
            izmerjena oddaljenost do objekta pred vozilom v m
        '''
        self.distanceFilt = self.distanceFilt * 0.5 + distance * 0.5  # osnovno nizko sito - spremenite
        self.currentThrust = 0  # vozilo stoji na miru - spremenite

    # object properties - do not touch!!!
    @property
    def distanceFiltered(self):
        '''
        Tukaj vrnete trenutno oddaljenost ocenjeno z filtri.
        To omogoča kasnejši izris, vrnete vašo interno spremenljivko.
        '''
        return self.distanceFilt

    @property
    def thrust(self):
        '''
        Tukaj vrnete relativno količino moči motorjev, vrednost med 0 in 1.
        '''
        return self.currentThrust