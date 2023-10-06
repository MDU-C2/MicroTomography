import numpy as np

from pytransform3d.rotations import (
    matrix_from_axis_angle,
    quaternion_from_matrix,
)


def generate_scan_points_cylinder(
    diameter, zStepSize: int, zMin: int, azimuthPoints: int
):
    """Generates points in a cylindrical pattern with quaternion angles pointing inwards toward (0, 0) in each z plane

    Parameters
    ----------
    diameter
        The diameter of the cylinder
    zStepSize : int
        The number of mm between each z-plane
    zMin : int
        The lowest point of the cylinder
    azimuthPoints : int
        Number of points in the azimuth angle

    Returns
    -------
    points : list
        List of coordinates for each point and the corresponding quaternion
    """
    if zMin > 0:
        raise AssertionError("zMin must be negative")
    R1 = matrix_from_axis_angle(np.array([0, 1, 0, np.pi / 2]))
    azimuth = (np.pi * np.linspace(0, 360 - (360 / azimuthPoints), azimuthPoints)) / 180
    points = []

    z = [h for h in reversed(range(zMin, 0 + zStepSize, zStepSize))]

    for angle in azimuth:
        for h in z:
            x = diameter * np.cos(angle)
            y = diameter * np.sin(angle)
            R2 = matrix_from_axis_angle(np.array([1, 0, 0, np.pi - angle]))
            R = np.matmul(R1, R2)

            points.append([[x, y, h], quaternion_from_matrix(R)])

    return points


def generate_scan_points_halfSphere(
    radius, azimuthPoints: int, elevationPoints: int, zMin=0
):
    """Generates points in a half-sphere below z=0 and the quaternion angles such that the z-axis always points to (0, 0, 0)

    Parameters
    ----------
    radius
        The radius of the half-sphere
    azimouthPoints : int
        Number of points in the azimouth plane
    elevationPoints : int
        Number of points in the elevation plane
    zMin : optional
        Sets how low the half-sphere should go in the z-axis

    Returns
    -------
    points : list
        List of both the coordinates and the quaternion of the points
    """
    if zMin > 0:
        raise AssertionError("zMin must be negative")
    azimuth = (np.pi * np.linspace(0, 360, azimuthPoints)) / 180
    elevation = (np.pi * np.linspace(-180, -90, elevationPoints)) / 180
    zParam = 1
    if zMin != 0:
        zParam = zMin / radius

    points = []
    for theta in azimuth:
        for phi in elevation:
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.sin(phi) * np.sin(theta)
            z = radius * np.cos(phi) * (-zParam)

            R2 = matrix_from_axis_angle(np.array([0, 1, 0, np.pi + phi]))
            R1 = matrix_from_axis_angle(np.array([0, 0, 1, theta]))
            R = np.matmul(R1, R2)
            points.append([[x, y, z], quaternion_from_matrix(R)])

    return points


generate_scan_points_halfSphere(10, 10, 10)
