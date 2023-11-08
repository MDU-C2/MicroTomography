"""Generates scan points for the yumi in a cylindrical pattern or a half-sphere.
Also transforms a laser distance and a robot coordinate to a point on the breast.
"""

import numpy as np

from pytransform3d.rotations import (
    matrix_from_quaternion,
    concatenate_quaternions,
    quaternion_from_axis_angle,
    plot_basis,
)


def generate_scan_points_cylinder(
    radius: (int | float),
    z_stepsize: int,
    z_min: int,
    azimuth_points: int,
    z_offset: (int | float) = 0,
    laser_angle: (int | float) = 0,
):
    """Generates points in a cylindrical pattern with quaternion angles pointing inwards toward
    (0, 0) in each z plane

    Parameters
    ----------
    radius : int or float
        The radius of the cylinder
    z_stepsize : int
        The number of mm between each z-plane
    z_min : int
        The lowest point of the cylinder
    azimuth_points : int
        Number of points in the azimuth angle
    z_offset: int or float, default: 0
        Sets an offset in the z-axis
    laser_angle: int or float, default: 0
        Sets the angle of the end effector to point up wards by a certain angle.


    Returns
    -------
    points : list, shape [(3,), (4,)]
        List of coordinates for each point and the corresponding quaternion
    """
    if z_min > 0:
        raise ValueError("z_min must be negative.")
    if z_offset > 0:
        raise ValueError("Offset must be negative to not hit the roof.")
    if laser_angle >= 90:
        raise ValueError(
            "The angle is larger than 90 degrees, the end effector will not point at the object."
        )
    if laser_angle <= -90:
        raise ValueError(
            "The angle is less than -90 degrees, the end effector will not point at the object."
        )

    laser_angle = np.deg2rad(laser_angle)
    q2 = quaternion_from_axis_angle(np.array([0, 1, 0, np.pi / 2 - laser_angle]))
    azimuth = np.linspace(0, 2 * np.pi - ((2 * np.pi) / azimuth_points), azimuth_points)
    points = []

    z = [h for h in reversed(range(z_min, z_offset + z_stepsize, z_stepsize))]

    for angle in azimuth:
        for h in z:
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            q1 = quaternion_from_axis_angle(np.array([0, 0, 1, np.pi + angle]))
            q = concatenate_quaternions(q1, q2)

            points.append([np.array([x, y, h]), q])

    return points


def generate_scan_points_halfsphere(
    radius: (int | float),
    azimuth_points: int,
    elevation_points: int,
    z_min: (int | float) = 0,
    z_offset: (int | float) = 0,
):
    """Generates points in a half-sphere below z=0 and the quaternion angles such that the
    z-axis of the end effector always points to (0, 0, 0)

    Parameters
    ----------
    radius: int or float
        The radius of the half-sphere
    azimuthPoints : int
        Number of points in the azimouth plane
    elevationPoints : int
        Number of points in the elevation plane
    zMin : optional
        Sets how low the half-sphere should go in the z-axis
    zOffset: int or float, default: 0
        Sets an offset in the z-axis

    Returns
    -------
    points : list, shape [(3,), (4,)]
        List of both the coordinates and the quaternion of the points
    """
    if z_min > 0:
        raise ValueError("z_min must be negative")
    azimuth = np.linspace(0, 2 * np.pi - ((2 * np.pi) / azimuth_points), azimuth_points)
    elevation = np.linspace(np.pi / 2, np.pi, elevation_points)
    z_param = 1
    if z_min != 0:
        z_param = -z_min / radius

    points = []
    for theta in azimuth:
        for phi in elevation:
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.sin(phi) * np.sin(theta)
            z = (radius * np.cos(phi) * (z_param)) + z_offset

            q1 = quaternion_from_axis_angle(np.array([0, 0, 1, theta]))

            q2 = quaternion_from_axis_angle(np.array([0, 1, 0, phi + np.pi]))

            q3 = quaternion_from_axis_angle(np.array([0, 0, 1, np.pi]))

            q2 = concatenate_quaternions(q2, q3)

            q = concatenate_quaternions(q1=q1, q2=q2)

            if phi == elevation[-1] and theta != azimuth[0]:
                continue
            points.append([np.array([x, y, z]), q])

    return points


def transform_laser_distance(point: list, laser_distance: (int | float)):
    """Transform the point measured by the laser from the user frame to the tool frame

    Parameters
    ----------
    point : array-like, shape [(3,), (4,)]
        A list containing the coordinates of the laser and the quaternions of the
        laser in the form [[Coordinates], [Quaternions]]
    laserDistance : int or float
        The distance measured by the laser in mm

    Returns
    -------
    list, shape(3,)
        A list of coordinates for the point measured by the laser
    """
    point_to_transform = np.array([0, 0, laser_distance])
    laser_coordinates = point[0]
    rotation_matrix = matrix_from_quaternion(point[1])

    transformed_point = (rotation_matrix @ point_to_transform) + laser_coordinates

    return transformed_point
