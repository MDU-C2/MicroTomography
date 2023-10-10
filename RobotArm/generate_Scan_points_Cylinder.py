import numpy as np

from pytransform3d.rotations import (
    matrix_from_quaternion,
    concatenate_quaternions,
    quaternion_from_axis_angle,
)


def generate_scan_points_cylinder(
    radius: (int | float),
    zStepSize: int,
    zMin: int,
    azimuthPoints: int,
    zOffset: (int | float) = 0,
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
    zOffset: int or float
        Sets an offset in the z-axis

    Returns
    -------
    points : list, shape [(3,), (4,)]
        List of coordinates for each point and the corresponding quaternion
    """
    if zMin > 0:
        raise ValueError("zMin must be negative")
    q1 = quaternion_from_axis_angle(np.array([0, 1, 0, np.pi / 2]))
    azimuth = np.linspace(0, np.pi - (np.pi / azimuthPoints), azimuthPoints)
    points = []

    z = [h for h in reversed(range(zMin, zOffset + zStepSize, zStepSize))]

    for angle in azimuth:
        for h in z:
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            q2 = quaternion_from_axis_angle(np.array([1, 0, 0, np.pi - angle]))
            q = concatenate_quaternions(q1=q1, q2=q2)

            points.append([np.array([x, y, h]), q])

    return points


def generate_scan_points_halfSphere(
    radius: (int | float),
    azimuthPoints: int,
    elevationPoints: int,
    zMin=0,
    zOffset: (int | float) = 0,
):
    """Generates points in a half-sphere below z=0 and the quaternion angles such that the z-axis of the end effector always points to (0, 0, 0)

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
    zOffset: int or float
        Sets an offset in the z-axis

    Returns
    -------
    points : list, shape [(3,), (4,)]
        List of both the coordinates and the quaternion of the points
    """
    if zMin > 0:
        raise ValueError("zMin must be negative")
    azimuth = np.linspace(0, np.pi - (np.pi / azimuthPoints), azimuthPoints)
    elevation = np.linspace(np.pi / 2, np.pi, elevationPoints)
    zParam = 1
    if zMin != 0:
        zParam = zMin / radius

    points = []
    for theta in azimuth:
        for phi in elevation:
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.sin(phi) * np.sin(theta)
            z = (radius * np.cos(phi) * (zParam)) + zOffset

            q2 = quaternion_from_axis_angle(np.array([0, 1, 0, np.pi + phi]))
            q1 = quaternion_from_axis_angle(np.array([0, 0, 1, theta]))
            q = concatenate_quaternions(q1=q1, q2=q2)

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
