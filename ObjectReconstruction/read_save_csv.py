## Author : Filip Lindhe

import pandas as pd
import numpy as np
import os
import time


def read_csv(filename):
    data = pd.read_csv(filename)
    return data.to_numpy()


def save_csv(filename, points):
    filename = time.strftime("%Y-%m-%d-%H_%M-") + filename
    saveDirectory = os.path.join(os.getcwd(), "scanned_data")
    os.makedirs(saveDirectory, exist_ok=True)
    filepath = os.path.join(saveDirectory, filename)

    df = pd.DataFrame(points, columns=["X_value", "Y_value", "Z_value"])

    # Save the DataFrame to a CSV file
    df.to_csv(
        filepath, index=False
    )  # Specify index=False to avoid writing row numbers as a column
