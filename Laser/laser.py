import serial
import math
from serial import *


class laser:
    """ Class for the laser
    call laser.measure() to measure the distance to the object.
    """

    def __init__(self, comPort, no_Measurements):
        """ Initialize the serial communication with the parameters from the datasheet.
        
        Keyword arguments:
        comPort -- The COMPort on the computer where the laser is connected
        no_Measurements -- The desired number of measurements to average over. 
        """
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

    #All the error codes from the laser with its corresponding error.
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
    
    def distance(self, digitalValue):
        """ Simple equation to get distance from the bits gotten from the laser.
        
        Keyword arguments
        digitalValue -- The 14 bit number gotten from the laser
        """

        return (digitalValue * (1.02 / 16368) - 0.01) * 100

    def measure(self):
        """ Gets the data from the laser via serial port and returns the average distance in mm """

        self.ser.flushInput()
        self.ser.flushOutput()
        i = 0
        # Loop until the desired amount of measurements are reached
        while i < self.no_Measurements:
            # Wait until atleast two values are in the buffer
            while self.ser.in_waiting < 2:
                continue
            
            # Read from serial port and get a 14 bit number
            data = self.ser.read_all()
            digitalValue = self.combineBytes(data[0:2])

            # Decide what the number means, taken from the datasheet
            if digitalValue < 161:
                return "SMR back up"
            elif digitalValue < 16208:
                self.stupid_list.append(self.distance(digitalValue) + 50)
                i = i + 1   # Only increment i when a distance is appended
            elif digitalValue < 16370:
                return "EMR back-up"
            elif digitalValue < 16384:
                return self.error_codes.get(digitalValue, "Unknown error")
        # Return the average distance
        return sum(self.stupid_list) / len(self.stupid_list)

    def combineBytes(self, dataBytes):
        """ Combine two 8 bit bytes into 14 bits

        Keyword arguments:
        dataBytes -- List of two bytes
        """
        # Iterate trough the two bytes
        for b in dataBytes:
            # If the 8th bit is 1, the byte is a H_Byte
            if b & 0x80:
                H_Byte = b & ~0x80  # Remove the 8th bit
            # if the 8th bit is 0, the byte is a L_Byte
            else:
                L_Byte = b # No need to remove the 8th bit
        # The final lenght should be 14 bits (7 + 7) with the H_Byte first
        # Hence shift the H_Byte 7 steps and append the L_Byte
        return H_Byte << 7 | L_Byte
