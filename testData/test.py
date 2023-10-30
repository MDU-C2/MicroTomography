import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv(r"testData\rawfile0.csv")
print(data)

x = data.loc[:, "X_value"].values
y = data.loc[:, "Y_value"].values
z = data.loc[:, "Z_value"].values
dist = data.loc[:, "Laser Distance"].values

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

ax.scatter(x, y, z)
plt.show()

a = dist - abs(z)

a = np.append(a[0:7], a[-8:])
print(a)

fig, ax = plt.subplots()
ax.scatter([x for x in range(len(dist))], dist)
ax.grid(True)
plt.show()
