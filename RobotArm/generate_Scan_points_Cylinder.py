import numpy as np

from pytransform3d.rotations import *

"""matrix_from_axis_angle,
    quaternion_from_matrix,
    matrix_from_quaternion,"""


def generate_scan_points_cylinder(
    radius: (int | float), zStepSize: int, zMin: int, azimuthPoints: int, zOffset=0
):
    """Generates points in a cylindrical pattern with quaternion angles pointing inwards toward (0, 0) in each z plane

    Parameters
    ----------
    radius : int or float
        The radius of the cylinder
    zStepSize : int
        The number of mm between each z-plane
    zMin : int
        The lowest point of the cylinder
    azimuthPoints : int
        Number of points in the azimuth angle

    Returns
    -------
    points : list, shape [(3,), (4,)]
        List of coordinates for each point and the corresponding quaternion
    """
    if zMin > 0:
        raise AssertionError("zMin must be negative")
    # R1 = matrix_from_axis_angle(np.array([0, 1, 0, np.pi / 2]))
    q1 = quaternion_from_axis_angle(np.array([0, 1, 0, np.pi / 2]))
    azimuth = (np.pi * np.linspace(0, 360 - (360 / azimuthPoints), azimuthPoints)) / 180
    points = []

    z = [h for h in reversed(range(zMin, zOffset + zStepSize, zStepSize))]

    for angle in azimuth:
        for h in z:
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            # R2 = matrix_from_axis_angle(np.array([1, 0, 0, np.pi - angle]))
            q2 = quaternion_from_axis_angle(np.array([1, 0, 0, np.pi - angle]))
            # R = np.matmul(R1, R2)
            q = concatenate_quaternions(q1=q1, q2=q2)

            # points.append([np.array([x, y, h]), quaternion_from_matrix(R)])
            points.append([np.array([x, y, h]), q])

    return points


def generate_scan_points_halfSphere(
    radius: (int | float), azimuthPoints: int, elevationPoints: int, zMin=0
):
    """Generates points in a half-sphere below z=0 and the quaternion angles such that the z-axis always points to (0, 0, 0)

    Parameters
    ----------
    radius: int or float
        The radius of the half-sphere
    azimouthPoints : int
        Number of points in the azimouth plane
    elevationPoints : int
        Number of points in the elevation plane
    zMin : optional
        Sets how low the half-sphere should go in the z-axis

    Returns
    -------
    points : list, shape [(3,), (4,)]
        List of both the coordinates and the quaternion of the points
    """
    if zMin > 0:
        raise AssertionError("zMin must be negative")
    azimuth = (np.pi * np.linspace(0, 360 - (360 / azimuthPoints), azimuthPoints)) / 180
    elevation = (np.pi * np.linspace(0, 90, elevationPoints)) / 180
    zParam = 1
    if zMin != 0:
        zParam = zMin / radius

    points = []
    for theta in azimuth:
        for phi in elevation:
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.sin(phi) * np.sin(theta)
            z = radius * np.cos(phi) * (zParam)

            # R2 = matrix_from_axis_angle(np.array([0, 1, 0, np.pi + phi]))
            q1 = quaternion_from_axis_angle(np.array([0, 1, 0, np.pi + phi]))
            # R1 = matrix_from_axis_angle(np.array([0, 0, 1, theta]))
            q2 = quaternion_from_axis_angle(np.array([0, 0, 1, theta]))
            q = concatenate_quaternions(q1=q2, q2=q1)
            # R = np.matmul(R1, R2)
            # points.append([np.array([x, y, z]), quaternion_from_matrix(R)])
            plot_basis(R=matrix_from_quaternion(q), p=np.array([x, y, z]))
            points.append([np.array([x, y, z]), q])

    return points


def transformLaserDistance(point: list, laserDistance: (int | float)):
    """Transform the point measured by the laser from the user frame to the tool frame

    Parameters
    ----------
    point : array-like, shape [(3,), (4,)]
        A list containing the coordinates of the laser and the quaternions of the laser in the form [[Coordinates], [Quaternions]]
    laserDistance : int or float
        The distance measured by the laser in mm

    Returns
    -------
    list, shape(3,)
        A list of coordinates for the point measured by the laser
    """
    p = np.array([0, 0, laserDistance])
    laserCoordinates = point[0]
    R = matrix_from_quaternion(point[1])

    p_new = (R @ p) + laserCoordinates

    return p_new


import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

# points = generate_scan_points_halfSphere(10, 10, 10, -20)
points = generate_scan_points_cylinder(100, 10, -100, 10, -10)
ax.scatter(
    [coord[0][0] for coord in points],
    [coord[0][1] for coord in points],
    [coord[0][2] for coord in points],
)
plt.show()

q1 = quaternion_from_axis_angle(np.array([0, 1, 0, np.pi / 2]))
q2 = quaternion_from_axis_angle(np.array([1, 0, 0, np.pi]))

R1 = matrix_from_axis_angle(np.array([0, 1, 0, np.pi / 2]))
R2 = matrix_from_axis_angle(np.array([1, 0, 0, np.pi]))
R = R1 @ R2
print(quaternion_from_matrix(R))

print(concatenate_quaternions(q1, q2))
