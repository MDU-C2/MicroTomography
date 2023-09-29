""" A class for the laser distance sensor optoNCDT1402
functions include setting the moving average,
measuring distance in mm,
getting the info from the optoNCDT1402 and turning the laser on/off

Author: Joel Josefsson
"""

import serial
import math
from time import sleep
from serial import *


class optoNCDT1402:
    """Class for the laser
    call laser.measure() to measure the distance to the object.
    """

    def __init__(self, comPort: str = "COM3", noMeasurements: int = 1):
        """Initialize the serial communication with the parameters from the datasheet.

        Parameters:
        -----------
        comPort : string
            The COMPort on the computer where the laser is connected

        noMeasurements : int
            The desired number of measurements to average over in the measuring function.
        """
        self.ser = serial.Serial(
            comPort,
            115200,
            timeout=5,
            bytesize=8,
            parity=PARITY_NONE,
            xonxoff=True,
            stopbits=1,
        )
        self.noMeasurements = noMeasurements
        self.laserOff()

    # All the error codes from the laser with its corresponding error.
    errorCodes = {
        16370: "No object detected",
        16372: "Too close to the sensor",
        16374: "Too far from the sensor",
        16376: "Target can not be evaluated",
        16378: "External laser off",
        16380: "Target moves towards the sensor",
        16382: "Target moves away from the sensor",
        16383: "Internal error",
        16384: "Internal error: Too many H-Bytes",
        16385: "Internal error: Too many L-Bytes",
    }

    def distance(self, digitalValue):
        """Simple equation to get distance from the bits gotten from the laser.

        Parameters:
        -----------
        digitalValue : int
            The 14 bit number recieved from the laser

        Returns:
        -----------
        distance : float
            The distance to the target in mm
        """
        distance = (digitalValue * (1.02 / 16368) - 0.01) * 100
        return distance

    def measure(self):
        """Gets the data from the laser via serial port and returns the average distance in mm"""

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.distanceList = []

        i = 0
        # Loop until the desired amount of measurements are reached
        while i < self.no_Measurements:
            # Wait until atleast two values are in the buffer
            while self.ser.in_waiting < 2:
                sleep(0.1)

            # Read from serial port and get a 14 bit number
            data = self.ser.read_all()
            digitalValue = self.combineBytes(
                data[-2:]
            )  # Combine the last two bytes in the list

            # Decide what the number means, taken from the datasheet
            if digitalValue < 161:
                return "SMR back up"
            elif digitalValue < 16208:
                self.distanceList.append(self.distance(digitalValue) + 50)
                i = i + 1  # Only increment i when a distance is appended
            elif digitalValue < 16370:
                return "EMR back-up"
            elif digitalValue < 16386:
                return self.error_codes.get(digitalValue, "Unknown error")

        if self.no_Measurements == 1:
            return self.distanceList.pop()

        # Return the average distance
        return sum(self.distanceList) / len(self.distanceList)

    def combineBytes(self, dataBytes: list):
        """Combine two 8 bit bytes into 14 bits.
        Makes sure there are 1 H_Byte and 1 L_Byte

        Parameters:
        -----------
        dataBytes : list
            List of two bytes to be concatenated

        Returns:
        -----------
        digitalValue : int
            A 14 bit integeger represtenting the concatenation of the input bytes
        """
        countH = 0
        countL = 0

        # Iterate trough the two bytes
        for b in dataBytes:
            # If the 8th bit is 1, the byte is a H_Byte
            if b & 0x80:
                H_Byte = b & ~0x80  # Remove the 8th bit
                countH = countH + 1
            # if the 8th bit is 0, the byte is a L_Byte
            else:
                L_Byte = b  # No need to remove the 8th bit
                countL = countL + 1

        if countH > 1:
            return 16384
        if countL > 1:
            return 16385
        # The final length should be 14 bits (7 + 7) with the H_Byte first
        # Hence shift the H_Byte 7 steps and append the L_Byte
        return H_Byte << 7 | L_Byte

    def getInfo(self):
        """Gets the info of the optoNCDT 1402
        Requests the parameters from the laser and returns a string of the parameters

        Returns:
        -----------
        data : string
            A string describing the configurations in the optoNCDT1402
        """

        # Bytearray to get info from the laser, found in the datasheet
        requestBits = bytearray(b"+++\x0dILD1\x20\x49\x00\x02")

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        # Write the bytearray to the laser and wait until reading
        sentBytes = self.ser.write(requestBits)
        sleep(0.2)
        self.ser.read_until(b"\xA0\x49\x00\x83")  # The last row before the info string
        data = self.ser.read_until(b"\x20\x20\x0D\x0A")  # The last row in the message
        return data.decode("ascii")

    def setMovingAverage(self, averagingNumber: int = 1):
        """Sets the averaging type to moving average with a specified averaging number

        Parameters:
        -----------
        averagingNumber : int
            The number of samples to be averaged over

        Returns:
        -----------
        result : bool
            True if it succeded and false if it did not
        """

        # Max samples are 64, lowest is 1
        new_averagingNumber = averagingNumber
        if averagingNumber > 64:
            new_averagingNumber = 64
        if averagingNumber < 1:
            new_averagingNumber = 1

        setAvg = bytearray(b"+++\x0dILD1\x20\x7F\x00\x04\x00\x00\x00\x00\x00\x00\x00")
        setAvg.append(new_averagingNumber)

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        b = self.ser.write(setAvg)
        return b"ILD1\xA0\x7F\x00\x02\x20\x20\x0D\x0A" in self.ser.read_until(
            b"ILD1\xA0\x7F\x00\x02\x20\x20\x0D\x0A"
        )

    def laserOff(self):
        """Turns the laser off internally by sending a bytearray to the laser

        Returns:
        -----------
        result : bool
            True or false depending if the command worked
        """
        offBytes = bytearray(b"+++\x0dILD1\x20\x86\x00\x02")

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        sleep(0.1)
        b = self.ser.write(offBytes)

        return b"ILD1\xa0\x86\x00\x02\x20\x20\x0d\x0a" in self.ser.read_until(
            b"ILD1\xa0\x86\x00\x02\x20\x20\x0d\x0a"
        )

    def laserOn(self):
        """Turns the laser on internally by sending a bytearray to the laser

        Returns:
        -----------
        result : bool
            True or false depending if the command worked
        """
        onBytes = bytearray(b"+++\x0dILD1\x20\x87\x00\x02")

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        sleep(0.1)
        b = self.ser.write(onBytes)

        return b"ILD1\xA0\x87\x00\x02\x20\x20\x0D\x0A" in self.ser.read_until(
            b"ILD1\xA0\x87\x00\x02\x20\x20\x0D\x0A"
        )
