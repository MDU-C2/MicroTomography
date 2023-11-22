import zvb8
import matplotlib.pyplot as plt
import numpy as np

f = np.linspace(3e+9, 5e+9, 501)

inst = zvb8.zvb8_setup()

data = zvb8.measure(inst)

fig, ax = plt.subplots()
ax.plot(f, data)
ax.set(xlabel="Frequency (Hz)", ylabel="Magnitude (dB)", title="Electromagnetic field")
plt.show()
