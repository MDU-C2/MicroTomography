from zvb import zvb8
from RobotArm import robot_control
from ObjectReconstruction import choose_points_microwave


def mw_boob(mesh, points: list, distance):
    # instrument = zvb8.zvb8_setup()
    robot = robot_control.robot_init(2)
    robot_control.set_zone_use(robot, 1)

    antenna_points, antenna_q = choose_points_microwave.ray_cast_points(mesh, points, distance)
    print(f"Coordinate: {antenna_points}, Quats: {antenna_q}")

    data = []
    for point, q in zip(antenna_points, antenna_q):
        robot_control.move_robot_linear(robot, [point, q])
        # data.append(zvb8.measure(instrument))

    return data


