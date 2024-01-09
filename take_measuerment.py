from RsInstrument import *
import sys
import os

path = os.getcwd()
sys.path.append(path)

from RaspberryPi.linearActuatorController import linear_actuator
from zvb.InstrumentClass import VisaInstrument
from zvb.titi_bakonkadonk_brest_8008_GUI import mw_init, save_csv
from zvb.titi_bakonkadonk_brest_8008 import save_s2p


def take_measurement():
    visa_instrument = mw_init()
    # robot = robot_control.robot_init(2, quaternions)
    # robot_control.set_zone_use(robot, True)

    freq, data_33 = visa_instrument.measure(meas_param="S33")
    _, data_32 = visa_instrument.measure(meas_param="S32")
    _, data_23 = visa_instrument.measure(meas_param="S23")
    _, data_22 = visa_instrument.measure(meas_param="S22")
    data = {
            "Frequency": freq,
            "S33": data_33,
            "S32": data_32,
            "S23": data_23,
            "S22": data_22,
        }
    save_csv(
        "MW_measurement_",
        data,
    )

    save_s2p("MW_measurement_", **data)


    return freq, data_33, data_32, data_23, data_22

if __name__ == "__main__":
    la = linear_actuator()
    while True:
        choice = ""
        while choice not in ["1", "2"]:
            choice = input("Move transmiter = 1, Take measurement = 2\n Enter your choice:")
        if choice == "1":
            la.move_actuator()
        if choice == "2":
            take_measurement()
