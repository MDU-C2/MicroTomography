# Network analyser - zvb8

This document is for information regarding the Network analyser zvb8.

## Prerequisites

To find the zvb8 with your computer, R&S visa must be installed. It can be downloaded from <https://www.rohde-schwarz.com/us/applications/r-s-visa-application-note_56280-148812.html>. It also includes a tool to check connection to the zvb8 to ensure you are able to find it.

The network analyser must have a static ip address, currently it is set on the router to be *192.168.0.70*.

You also need RsInstrument installed in your python environment. Install it with

``` console
pip install RsInstrument
```

## InstrumentClass.py
The class InstrumentClass.py is used for all zvb8 functionality.

### VisaInstrument
The class itself is initialized with a visainstrument defined outside the class and sets some parameters in the instrument before confirming a connection have been established.

An example of initialising the class is:
``` python
from RsInstrument import *
from InstrumentClass import VisaInstrument

resource = "TCPIP0::192.168.0.70::INSTR"
Instrument = RsInstrument(resource, True, True, "SelectVisa='rs'")

MyVisaInstrument = VisaInstrument(Instrument)
```

### comcheck
Checks if the instrument is present by asking what IDN it is.

### meassetup
Defines parameters to measure. The parameters to define are *start frequency*, *stop frequency*, *number of points*, *S-parameters*, *format*.

An example is:
``` python
MyVisaInstrument.meassetup(f_start=3.8e9, f_stop=4.2e9, points=401)
```

### measure
This method gets measurement based on the *meas_param* parameter and returns the frequencies and the complex data. 

Example:
``` python
freq_33, data_33 = MyVisaInstrument.measure(meas_param="S33")
freq_32, data_32 = MyVisaInstrument.measure(meas_param="S32")
freq_23, data_23 = MyVisaInstrument.measure(meas_param="S23")
freq_22, data_22 = MyVisaInstrument.measure(meas_param="S22")
```

### close
Simply closes the connection to the instrument.

## Examples of using InstrumentClass.py
### Setting up the class to measure
In this example the class is initialised with an instrument with ip *192.168.0.70* and sets it up for measurments with frequencies between 3.8GHz and 4.9Ghz and 801 measurement points.
``` python
from zvb.InstrumentClass import VisaInstrument
from InstrumentClass import VisaInstrument

resource = "TCPIP0::192.168.0.70::INSTR"
Instrument = RsInstrument(resource, True, True, "SelectVisa='rs'")

MyVisaInstrument = VisaInstrument(Instrument)
MyVisaInstrument.comcheck()
MyVisaInstrument.meassetup(f_start=3.8e9, f_stop=4.6e9, points=801)
```

### Get measurements and plot the magnitiude
In this example the instument is initialised with the same parameters as above and takes four measurements which is then plotted with matplotlib in dB magnitude.

``` python
import matplotlib.pyplot as plt
import numpy as np

from zvb.InstrumentClass import VisaInstrument
from InstrumentClass import VisaInstrument

resource = "TCPIP0::192.168.0.70::INSTR"
Instrument = RsInstrument(resource, True, True, "SelectVisa='rs'")

MyVisaInstrument = VisaInstrument(Instrument)
MyVisaInstrument.comcheck()
MyVisaInstrument.meassetup(f_start=3.8e9, f_stop=4.6e9, points=801)

freq, data_33 = visa_instrument.measure(meas_param="S33")
_, data_32 = visa_instrument.measure(meas_param="S32")
_, data_23 = visa_instrument.measure(meas_param="S23")
_, data_22 = visa_instrument.measure(meas_param="S22")

plt.plot(freq, 20 * np.log10(np.abs(data33)))
plt.plot(freq, 20 * np.log10(np.abs(data32)))
plt.plot(freq, 20 * np.log10(np.abs(data23)))
plt.plot(freq, 20 * np.log10(np.abs(data22)))
plt.show()
```


