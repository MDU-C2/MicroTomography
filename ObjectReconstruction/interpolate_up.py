import numpy as np


### Find max Z points, make one circle.
### Take that circle which correlates to the highest circle in the breast
### Add points up in stepsize, if stepsize is 2 and circle 15/2 times


def interpolate_up(points, step_size):
    top_circle = []
    i = 0
    for idx, point in enumerate(points):
        if point[2] >= -15:
            temp = point
            temp[2] = -15 + step_size
            top_circle.append(temp)
    top_circle = np.array(top_circle)
    for i in range(round(15 / step_size)):
        points = np.append(points, top_circle, axis=0)
        top_circle[:, 2] = top_circle[:, 2] + step_size

    return points
