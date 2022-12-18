from enum import IntEnum
import math

class EDA_ANGLE_T(IntEnum):
    TENTHS_OF_A_DEGREE_T = 0
    DEGREES_T = 1
    RADIANS_T = 2

class EDA_ANGLE:
    def __init__(self, value, type):
        if type == int(EDA_ANGLE_T.RADIANS_T):
            self.value = value / (math.pi / 180)
        elif type == int(EDA_ANGLE_T.TENTHS_OF_A_DEGREE_T):
            self.value = value / 10
        else:
            self.value = value

    def AsDegrees(self):
        return self.value

    def AsTenthsOfADegree(self):
        return int(self.value * 10)

    def AsRadians(self):
        return self.value * math.pi / 180

    def __add__(self, other):
        return EDA_ANGLE(self.value + other.value, EDA_ANGLE_T.DEGREES_T)

    def __iadd__(self, other):
        self.value += other.value
        return self

    def __sub__(self, other):
        return EDA_ANGLE(self.value - other.value, EDA_ANGLE_T.DEGREES_T)

    def __isub__(self, other):
        self.value -= other.value
        return self

    def __mul__(self, other):
        return EDA_ANGLE(self.value * other, EDA_ANGLE_T.DEGREES_T)

    def __rmul__(self, other):
        return EDA_ANGLE(other * self.value, EDA_ANGLE_T.DEGREES_T)

    def __truediv__(self, other):
        return EDA_ANGLE(self.value / other, EDA_ANGLE_T.DEGREES_T)
