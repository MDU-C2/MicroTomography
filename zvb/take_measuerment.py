from RsInstrument import *
from zvb.InstrumentClass import VisaInstrument
from titi_bakonkadonk_brest_8008_GUI import mw_init, save_csv


def take_measurement():
    visa_instrument = mw_init()
    # robot = robot_control.robot_init(2, quaternions)
    # robot_control.set_zone_use(robot, True)

    freq, data_33 = visa_instrument.measure(meas_param="S33")
    _, data_32 = visa_instrument.measure(meas_param="S32")
    _, data_23 = visa_instrument.measure(meas_param="S23")
    _, data_22 = visa_instrument.measure(meas_param="S22")
    save_csv(
        "MW_measurement_",
        {
            "Frequency": freq,
            "S33": data_33,
            "S32": data_32,
            "S23": data_23,
            "S22": data_22,
        },
    )

    return freq, data_33, data_32, data_23, data_22
