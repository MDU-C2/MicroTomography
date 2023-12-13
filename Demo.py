import sys
import os

from matplotlib import pyplot as plt
import numpy as np
from ObjectReconstruction import choose_points_microwave
from ObjectReconstruction.interpolate_up import interpolate_up
from ObjectReconstruction.surface_reconstruction import poisson_surface_reconstruction
from RaspberryPi.linearActuatorController import linear_actuator
from RobotArm import robot_control
from zvb.titi_bakonkadonk_brest_8008 import mw_init

pathname = os.getcwd()

sys.path.append("../Microtomography")


from RobotArm.scan_breast_phantom import scan_points

from ObjectReconstruction.read_save_csv import read_csv

result = read_csv("scanned_data/2023-11-29-09_01-brest_no_nipple.csv")
result = interpolate_up(result, step_size=2)

print("Getting lowest point in mesh")
lowest_point = np.min(result[:, 2])
la_point = lowest_point - 10
print("The linear actuator will be placed at : ", la_point)

print("making mesh")
mesh = poisson_surface_reconstruction(result, save=False, re_resolution=5)

la = linear_actuator()

points = np.array(
    [
        [60, 0, -30],
        [60, 60, -30],
        [0, 60, -30],
        [-60, 60, -30],
        [-60, 0, -30],
        [-60, -60, -30],
        [0, -60, -30],
        [60, -60, -30],
    ]
)
distance = 10

antenna_points, antenna_q, _ = choose_points_microwave.get_points(
    mesh, points, distance
)

while True:
    """_ = scan_points(
        120,
        5,
        -50,
        16,
        -15,
        0,
    )"""
    la.move_to_desired_location_upwards(la_point)
    visa_instrument = mw_init()

    robot = robot_control.robot_init(2)
    robot_control.set_zone_use(robot, True)

    fig, ax1 = plt.subplots()

    color1 = "tab:red"
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("dB", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color2 = "tab:blue"
    ax2.set_ylabel("dB", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.ion()
    # plt.show()

    freq, data_33 = visa_instrument.measure(meas_param="S33")
    _, data_32 = visa_instrument.measure(meas_param="S32")
    _, data_23 = visa_instrument.measure(meas_param="S23")
    _, data_22 = visa_instrument.measure(meas_param="S22")

    (line1,) = ax1.plot(
        np.abs(freq),
        20 * np.log10(np.abs(data_22)),
        color=color1,
        label="S22",
    )

    (line2,) = ax2.plot(
        np.abs(freq),
        20 * np.log10(np.abs(data_23)),
        color=color2,
        label="S23",
    )

    ax1.legend(handles=[line1, line2])

    for point, q in zip(antenna_points, antenna_q):
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

        """(line1,) = ax1.plot(
            np.abs(data["Frequency"]),
            20 * np.log10(np.abs(data["S22"])),
            color=color1,
            label="S22",
        )"""
        line1.set_ydata(20 * np.log10(np.abs(data["S22"])))
        line2.set_ydata(20 * np.log10(np.abs(data["S23"])))
        # ax1.ylim(max(20 * np.log10(np.abs(data["S22"]))), min(20 * np.log10(np.abs(data["S22"]))))
        # ax2.ylim(max(20 * np.log10(np.abs(data["S23"]))), min(20 * np.log10(np.abs(data["S23"]))))

        ax1.relim()
        ax2.relim()
        """(line2,) = ax2.plot(
            np.abs(data["Frequency"]),
            20 * np.log10(np.abs(data["S23"])),
            color=color2,
            label="S23",
        )"""

        # ax1.legend(handles=[line1, line2])
        fig.canvas.draw()
        fig.canvas.flush_events()

        plt.pause(1)
        la.move_to_zeroLocation()

    robot_control.close_connection(robot)
