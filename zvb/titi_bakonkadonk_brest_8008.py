from zvb import zvb8
from RobotArm import robot_control
from ObjectReconstruction import choose_points_microwave
import matplotlib.pyplot as plt
import numpy as np


def mw_boob(mesh, points: list, distance):
    instrument = zvb8.zvb8_setup()
    robot = robot_control.robot_init(2)
    robot_control.set_zone_use(robot, True)

    antenna_points, antenna_q = choose_points_microwave.ray_cast_points(
        mesh, points, distance
    )
    
    f = np.linspace(3e+9, 5e+9, 501)
    
    data = []
    for point, q in zip(antenna_points, antenna_q):
        _, ax = plt.subplots()
        ax.set(xlabel="Frequency (Hz)", ylabel="Magnitude (dB)", title="Electromagnetic field")

        print(f"Going to Coordinate: {point}, Quats: {q}")
        robot_control.move_robot_linear(robot, [point, q])
        mw_data = zvb8.measure(instrument)
        data.append(mw_data)
        ax.plot(f, mw_data)
        
        plt.show()

    return data
