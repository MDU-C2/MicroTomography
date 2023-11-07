import os
import pandas as pd
import numpy as np

filenameArray = ["file" + str(x) + ".csv" for x in range(6)]

file_path = os.path.join("testData", filenameArray[0])

df = pd.read_csv(file_path)
data = pd.DataFrame(df, columns=["X_value", "Y_value", "Z_value"]).to_numpy()

delta_prev = np.full_like(data, 0)
delta_full = np.empty([1, 3])


variance = []
deltamax = []
deltamin = []

for filename in filenameArray[1:]:
    file_path = os.path.join("testData", filename)
    df = pd.read_csv(file_path)

    data_comp = pd.DataFrame(df, columns=["X_value", "Y_value", "Z_value"]).to_numpy()

    delta = np.abs(data - data_comp)
    deltamax.append(np.max(delta, axis=0))
    deltamin.append(np.min(delta, axis=0))

    variance.append(np.var(delta, axis=0))

    data_new = delta + delta_prev

    delta_full = np.append(delta_full, delta, axis=0)

    delta_prev = data_new


data_new = data_new / 6


filename = "deltaData.csv"
data = pd.DataFrame(data_new, columns=["X_value", "Y_value", "Z_value"])
file_path = os.path.join("testData", filename)

with open(file_path, "w", newline="") as csvfile:
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file

    df.to_csv(csvfile, index=False)

delta_full = delta_full[1:, :]
print("mean delta_full:", np.mean(delta_full, axis=0))
print("max delta_full:", np.max(delta_full, axis=0))
print("min delta_full:", np.min(delta_full, axis=0))
print("var delta_full:", np.var(delta_full, axis=0))
print("Variance :", variance)
print("variance on variance :", np.max(variance))
print("max : ", deltamax)
print("min : ", deltamin)


test = ["mean delta_full" + np.str_(np.mean(delta_full, axis=0))]
print(test)
