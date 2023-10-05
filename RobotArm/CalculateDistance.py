import math


def calculateDistance(points, theta, measuredDistance):
    distanceOriginToRobot = math.sqrt(points[0] ** 2 + points[1] ** 2)

    distanceOriginToPoint = distanceOriginToRobot - measuredDistance

    return [
        distanceOriginToPoint * math.cos(theta),
        distanceOriginToPoint * math.sin(theta),
        points[3],
    ]
