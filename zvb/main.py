import matplotlib.pyplot as plt
import numpy as np

from RsInstrument import *
from InstrumentClass import VisaInstrument

# Define variables
# resource = 'TCPIP0::192.168.0.1::INSTR'  # VISA resource string for the device
resource = 'TCPIP0::169.254.224.141::INSTR'  # VISA resource string for the device

# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.53.0')

if __name__ == '__main__':

    # Simulating instrument session
    Instrument = RsInstrument(resource, True, True, "SelectVisa='rs'")

    # Create new VisaInstrument class and setup environment
    MyVisaInstrument = VisaInstrument(Instrument)
    MyVisaInstrument.comcheck()

    MyVisaInstrument.meassetup(f_start=3.8e9, f_stop=4.2e9, points=401)

    # Acquire current measurement data
    freq_33, data_33 = MyVisaInstrument.measure(meas_param="S33")
    freq_32, data_32 = MyVisaInstrument.measure(meas_param="S32")
    freq_23, data_23 = MyVisaInstrument.measure(meas_param="S23")
    freq_22, data_22 = MyVisaInstrument.measure(meas_param="S22")

    # data_mag_22 = np.abs(data_22)
    # data_phase_22 = np.angle(data_22)
    #
    # plt.plot(freq_22, data_mag_22)
    # plt.show()
