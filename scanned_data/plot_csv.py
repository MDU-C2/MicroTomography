import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv(r"scanned_data/nipple5.csv")

X = data["X_value"].values
Y = data["Y_value"].values
Z = data["Z_value"].values

fig = plt.figure()
ax1 = fig.add_subplot(projection="3d")

ax1.scatter(X, Y, Z)

plt.show()