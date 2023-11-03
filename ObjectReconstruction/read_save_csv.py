import pandas as pd
import os


def read_csv(filename):
    data = pd.read_csv(filename, header=None, delimiter=r"\s+")
    return data.values


def save_csv(filename, points):
    d = {"X": points[:, 0], "Y": points[:, 1], "Z": points[:, 2]}
    currentWD = os.getcwd()
    os.makedirs(os.path.join(currentWD, "scanned_data"), exist_ok=True)
    filepath = os.path.join(currentWD, "scanned_data", filename)
    dataFrame = pd.DataFrame(data=d)
    dataFrame.to_csv(filepath, index=False)
