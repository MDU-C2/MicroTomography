from zvb import zvb8
from RobotArm import robot_control
from ObjectReconstruction import choose_points_microwave
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time

from RsInstrument import *
from zvb.InstrumentClass import VisaInstrument


def mw_init():
    resource = "TCPIP0::192.168.0.70::INSTR"
    Instrument = RsInstrument(resource, True, True, "SelectVisa='rs'")

    # Create new VisaInstrument class and setup environment
    MyVisaInstrument = VisaInstrument(Instrument)
    MyVisaInstrument.comcheck()
    MyVisaInstrument.meassetup(f_start=3.8e9, f_stop=4.2e9, points=401)

    return MyVisaInstrument


def mw_boob(mesh, points: list, distance):
    visa_instrument = mw_init()

    robot = robot_control.robot_init(2)
    robot_control.set_zone_use(robot, True)

    antenna_points, antenna_q = choose_points_microwave.ray_cast_points(
        mesh, points, distance
    )

    i = 0
    data = []
    for point, q in zip(antenna_points, antenna_q):
        print(f"Going to Coordinate: {point}, Quats: {q}")
        robot_control.move_robot_linear(robot, [point, q])
        freq_33, data_33 = visa_instrument.measure(meas_param="S33")
        freq_32, data_32 = visa_instrument.measure(meas_param="S32")
        freq_23, data_23 = visa_instrument.measure(meas_param="S23")
        freq_22, data_22 = visa_instrument.measure(meas_param="S22")
        save_csv(
            "MW_measurement_" + str(i) + ".csv",
            {
                "Frequency": freq_33,
                "Complex S33": data_33,
                "Complex S32": data_32,
                "Complex S23": data_23,
                "Complex S22": data_22,
            },
        )
        i += 1
    robot_control.close_connection(robot)
    return data


def save_csv(filename, points):
    filename = time.strftime("%Y-%m-%d-%H_%M-") + filename
    saveDirectory = os.path.join(os.getcwd(), "mw_data")
    os.makedirs(saveDirectory, exist_ok=True)
    filepath = os.path.join(saveDirectory, filename)

    df = pd.DataFrame(points, dtype=complex)

    # Save the DataFrame to a CSV file
    df.to_csv(
        filepath, index=False
    )  # Specify index=False to avoid writing row numbers as a column
