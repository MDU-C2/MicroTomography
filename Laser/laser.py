import serial
import math
from serial import *


class laser:
    error_codes = {
        16370: "No object detected",
        16372: "Too close to the sensor",
        16374: "Too far from the sensor",
        16376: "Target can not be evaluated",
        16378: "External laser off",
        16380: "Target moves towards the sensor",
        16382: "Target moves away from the sensor",
        16383: "Internal error",
    }

    def __init__(self, comPort, no_Measurements):
        self.ser = serial.Serial(
            comPort,
            115200,
            timeout=None,
            bytesize=8,
            parity=PARITY_NONE,
            xonxoff=True,
            stopbits=1,
        )
        self.stupid_list = []
        self.no_Measurements = no_Measurements

    def distance(digitalValue):
        return (digitalValue * (1.02 / 16368) - 0.01) * 100

    def measure(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        i = 0

        while i < self.no_Measurements:
            while self.ser.in_waiting < 2:
                continue

            data = self.ser.read_all()
            digitalValue = self.combineBytes(data[0:2])

            if digitalValue < 161:
                return "SMR back up"
            elif digitalValue < 16208:
                self.stupid_list.append(self.distance(digitalValue) + 50)
                i = i + 1
            elif digitalValue < 16370:
                return "EMR back-up"
            elif digitalValue < 16384:
                return self.error_codes.get(digitalValue, "Unknown error")

        return sum(self.stupid_list) / len(self.stupid_list)

    def combineBytes(self, dataBytes):
        for b in dataBytes:
            if b & 0x80:
                H_Byte = b & ~0x80
            else:
                L_Byte = b

        return H_Byte << 7 | L_Byte
