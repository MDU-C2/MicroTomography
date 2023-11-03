import numpy as np
import time
import matplotlib.pyplot as plt
import winsound
import random

size = 100
array = np.random.randint(1, size, 100)
plt.ion
sortedarray = []
sortedarray = np.sort(array)
x = np.arange(size)
figure, ax = plt.subplots()
line1 = ax.bar(x, array)
t = time.time()
plt.title("Geeks For Geeks", fontsize=20)
line1.remove()

figure.show()
i = 1
while not (sortedarray == array).all():
    np.random.shuffle(array)
    plt.title("Bogosort - # of swaps :%i" % i, fontsize=20)
    line1 = ax.bar(x, array, color="grey", width=1)
    figure.canvas.draw()
    figure.canvas.flush_events()

    # duration = 50
    # time.sleep(0.01)
    # sum = np.sum(sortedarray == array)
    # frequency = 200 + 40 * (sum * 10)
    # winsound.Beep(frequency, duration)
    line1.remove()
    i = i + 1
totalElapsed = time.time() - t
plt.title("Bogosort - # of swaps :%i" % i, fontsize=20)
line1 = ax.bar(x, array, color="grey", width=0.1)
figure.canvas.draw()
# figure.canvas.flush_events()
plt.show()
print("Time to complete bogosort : ", totalElapsed, "Swaps needed :", i)
print("hello")
