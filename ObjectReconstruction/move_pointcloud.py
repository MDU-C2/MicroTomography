import numpy as np


def move_pointcloud(data):
    max_x = np.max(data[:, 0])
    min_x = np.min(data[:, 0])
    max_y = np.max(data[:, 1])
    min_y = np.min(data[:, 1])

    data[:, 0] = data[:, 0] - (min_x + max_x) / 2
    data[:, 1] = data[:, 1] - (min_y + max_y) / 2
    return data
