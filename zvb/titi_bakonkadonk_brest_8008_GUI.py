import sys
import os

path = os.getcwd()
sys.path.append(path)

from RobotArm import robot_control
from ObjectReconstruction import choose_points_microwave
import numpy as np
import pandas as pd
import os
import time

from RsInstrument import *
from zvb.InstrumentClass import VisaInstrument

def mw_init() -> VisaInstrument:
    """Initializes the zvb8 Network analyser with the ip address 192.168.0.70

    Returns
    -------
    VisaInstrument
        The object for the Network analyser
    """
    resource = "TCPIP0::192.168.0.70::INSTR"
    Instrument = RsInstrument(resource, True, True, "SelectVisa='rs'")

    # Create new VisaInstrument class and setup environment
    MyVisaInstrument = VisaInstrument(Instrument)
    MyVisaInstrument.comcheck()
    MyVisaInstrument.meassetup(f_start=3.8e9, f_stop=4.2e9, points=401)

    return MyVisaInstrument


def mw_boob(mesh, points: list, distance: (int | float), quaternions):
    """Scans the mesh with the points on the mesh closest to the input points with a distance from the mesh

    Parameters
    ----------
    mesh : TriangleMesh
        The mesh of the scanned object
    points : list, shape(, 3)
        The points in the space you want to scan in the shape [X, Y, Z]
    distance : Int or Float
        The distance from the mesh you want to scan
    quaternions : [q1, q2, q3, q4]
        The quaternions of the robot arm
    """
    robot = robot_control.robot_init(2, quaternions)
    robot_control.set_zone_use(robot, True)


    antenna_points, antenna_q = choose_points_microwave.ray_cast_points(mesh, points, distance)

    robot_control.close_connection(robot) robot_control.close_connection(robot)
    return antenna_points, antenna_q

def mw_micromovement(mesh, points: list, distance: (int | float), quaternions):
    """Scans the mesh with the points on the mesh closest to the input points with a distance from the mesh

    Parameters
    ----------
    mesh : TriangleMesh
        The mesh of the scanned object
    points : list, shape(, 3)
        The points in the space you want to scan in the shape [X, Y, Z]
    distance : Int or Float
        The distance from the mesh you want to scan
    quaternions : [q1, q2, q3, q4]
        The quaternions of the robot arm
    """
    robot = robot_control.robot_init(2, quaternions)
    robot_control.set_zone_use(robot, True)

    antenna_points, antenna_q = choose_points_microwave.ray_cast_points(mesh, points, distance)

    robot_control.close_connection(robot)
    return antenna_points, antenna_q

def networkMeasure(robot,point, q, i, quaternions):
    visa_instrument = mw_init()
    #robot = robot_control.robot_init(2, quaternions)
    #robot_control.set_zone_use(robot, True)

    robot_control.move_robot_linear(robot, [point, q])
    freq, data_33 = visa_instrument.measure(meas_param="S33")
    _, data_32 = visa_instrument.measure(meas_param="S32")
    _, data_23 = visa_instrument.measure(meas_param="S23")
    _, data_22 = visa_instrument.measure(meas_param="S22")
    save_csv(
        "MW_measurement_" + str(i),
        {
            "Frequency": freq,
            "S33": data_33,
            "S32": data_32,
            "S23": data_23,
            "S22": data_22,
        },
    )
    
    return freq, data_33, data_32, data_23, data_22


def save_csv(filename: str, points: dict):
    """Save the microwave data to a csv file

    Parameters
    ----------
    filename : string
        The name of the file you want to save without extention. It will be asved in the form YYYY-MM-DD-HH-MM-filename
    points : dict
        A dict containing the frequencies and the S parametes you want to save.
    """
    filename = time.strftime("%Y-%m-%d-%H_%M-") + filename + ".csv"
    saveDirectory = os.path.join(os.getcwd(), "mw_data")
    os.makedirs(saveDirectory, exist_ok=True)
    filepath = os.path.join(saveDirectory, filename)

    df = pd.DataFrame(points, dtype=complex)

    # Save the DataFrame to a CSV file
    df.to_csv(
        filepath, index=False
    )  # Specify index=False to avoid writing row numbers as a column


def save_s2p(filename: str, frequency: list, **kwargs):
    """Saves the data from the Network analyzer in a s2p file

    Parameters
    ----------
    filename : String
        The name of the file you want to save without extention. It will be asved in the form YYYY-MM-DD-HH-MM-filename
    frequency : list
        A list containing all the frequencies of the data
    """
    s = np.zeros((len(frequency), 2, 2), dtype=complex)
    for key, value in kwargs.items():
        if key == "S22":
            s[:, 0, 0] = value

        elif key == "S23":
            s[:, 0, 1] = value

        elif key == "S32":
            s[:, 1, 0] = value

        elif key == "S33":
            s[:, 1, 1] = value

    saveDirectory = os.path.join(os.getcwd(), "mw_data")
    filename = time.strftime("%Y-%m-%d-%H_%M-") + filename

    #net = Network(frequency=Frequency.from_f(frequency), s=s)
    #net.write_touchstone(filename=filename, dir=saveDirectory)


def read_complex_csv(path: str) -> list:
    """Reads the complex data from a .csv file

    Parameters
    ----------
    path : string
        The path of the file you want to read.

    Returns
    -------
    list
        A list containing the complex data stored in the path
    """
    data = pd.read_csv(path)
    for name in data.columns[1:]:
        data[name] = data[name].apply(lambda s: complex(s))

    return data

def connectRobot(quaternions):
    robot = robot_control.robot_init(2, quaternions)
    robot_control.set_zone_use(robot, True)

    return robot

def closeRobot(robot):
    robot_control.close_connection(robot)



    
