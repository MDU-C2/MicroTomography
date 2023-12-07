import sys
import os

sys.path.append("C:/Users/jjn17015/Documents/MicroTomography")

from RobotArm import robot_control
from ObjectReconstruction import choose_points_microwave
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time

from RsInstrument import *

from zvb.InstrumentClass import VisaInstrument

from skrf import Frequency, Network


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
    MyVisaInstrument.meassetup(f_start=3.8e9, f_stop=4.6e9, points=801)

    return MyVisaInstrument


def mw_boob(mesh, points: list, distance: (int | float)) -> None:
    """Scans the mesh with the points on the mesh closest to the input points with a distance from the mesh

    Parameters
    ----------
    mesh : TriangleMesh
        The mesh of the scanned object
    points : list, shape(, 3)
        The points in the space you want to scan in the shape [X, Y, Z]
    distance : Int or Float
        The distance from the mesh you want to scan
    """
    visa_instrument = mw_init()

    robot = robot_control.robot_init(2)
    robot_control.set_zone_use(robot, True)

    antenna_points, antenna_q, _ = choose_points_microwave.get_points(
        mesh, points, distance
    )

    i = 0
    for point, q in zip(antenna_points, antenna_q):
        fig, ax1 = plt.subplots()

        color1 = "tab:red"
        ax1.set_xlabel("Frequency (Hz)")
        ax1.set_ylabel("dB", color=color1)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color2 = "tab:blue"
        ax2.set_ylabel("dB", color=color2)
        
        print(f"Going to Coordinate: {point}, Quats: {q}")
        robot_control.move_robot_linear(robot, [point, q])
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
            "MW_measurement_" + str(i),
            data,
        )

        """for key, value in data.items():
            if key != "Frequency":
                plt.plot(np.abs(data["Frequency"]), np.abs(value), label=key)"""

        save_s2p("MW_measurement_" + str(i), frequency=freq, S22 = data_22, S23=data_23, S32 = data_32, S33=data_33)

        (line1,) = ax1.plot(
            np.abs(data["Frequency"]),
            20 * np.log10(np.abs(data["S22"])),
            color=color1,
            label="S22",
        )
        ax1.tick_params(axis="y", labelcolor=color1)

        (line2,) = ax2.plot(
            np.abs(data["Frequency"]),
            20 * np.log10(np.abs(data["S23"])),
            color=color2,
            label="S23",
        )
        ax2.tick_params(axis="y", labelcolor=color2)

        ax1.legend(handles=[line1, line2])
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()
        i += 1
    robot_control.close_connection(robot)


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

    net = Network(frequency=Frequency.from_f(frequency), s=s)
    net.write_touchstone(filename=filename, dir=saveDirectory)


def read_complex_csv(path: str) -> pd.DataFrame:
    """Reads the complex data from a .csv file

    Parameters
    ----------
    path : string
        The path of the file you want to read.

    Returns
    -------
    Pandas Dataframe
        A Dataframe containing the complex data stored in the path
    """
    data = pd.read_csv(path)
    for name in data.columns:
        data[name] = data[name].apply(lambda s: complex(s))

    return data


if __name__ == "__main__":
    data = read_complex_csv(r"mw_data\2023-11-28-14_59-MW_measurement_0.csv")

    data = {name: data[name] for name in data.columns}

    plt.plot(data["Frequency"], 20 * np.log10(np.abs(data["Complex S22"])))
    plt.plot(data["Frequency"], 20 * np.log10(np.abs(data["Complex S23"])))
    plt.plot(data["Frequency"], 20 * np.log10(np.abs(data["Complex S32"])))
    plt.plot(data["Frequency"], 20 * np.log10(np.abs(data["Complex S33"])))
    plt.show()

    """for key, value in data.items():
        if key != "Frequency":
            plt.plot(np.abs(data["Frequency"]), np.abs(value), label=key)"""

    fig, ax1 = plt.subplots()

    color1 = "tab:red"
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("dB", color=color1)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color2 = "tab:blue"
    ax2.set_ylabel("dB", color=color2)  # we already handled the x-label with ax1

    (axis_1,) = ax1.plot(
        np.abs(data["Frequency"]),
        20 * np.log10(np.abs(data["Complex S22"])),
        color=color1,
        label="S22",
    )
    ax1.tick_params(axis="y", labelcolor=color1)

    (axis_2,) = ax2.plot(
        np.abs(data["Frequency"]),
        20 * np.log10(np.abs(data["Complex S23"])),
        color=color2,
        label="S23",
    )
    ax2.tick_params(axis="y", labelcolor=color2)
    # plt.legend()
    ax1.legend(handles=[axis_1, axis_2])

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
