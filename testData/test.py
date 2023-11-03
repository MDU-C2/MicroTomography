import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data1 = pd.read_csv(r"testData\calibrationAfterAbsacc.csv")
data2 = pd.read_csv(r"testData\calibrationTest0.csv")
# print(data)

x1 = data1.loc[:, "X_value"].values
y1 = data1.loc[:, "Y_value"].values
z1 = data1.loc[:, "Z_value"].values
dist1 = data1.loc[:, "Laser Distance"].values

z1 = z1 + dist1

x2 = data2.loc[:, "X_value"].values
y2 = data2.loc[:, "Y_value"].values
z2 = data2.loc[:, "Z_value"].values
dist2 = data2.loc[:, "Laser Distance"].values

z2 = z2 + dist2

"""fig = plt.figure()
ax = fig.add_subplot(projection="3d")"""

"""ax.scatter(x, y, z)
plt.show()"""
e1 = z1 - 757
e2 = z2 - 757

# a = dist - abs(z)

# a = np.append(a[0:7], a[-8:])
# print(a)

fig, ax = plt.subplots()
ax.scatter([x for x in range(len(e1))], e1)
ax.scatter([x for x in range(len(e2))], e2)
ax.grid(True)
plt.show()
