from RsInstrument import *
from time import sleep

s2p_filename = r"C:\Rhode&Schwarz\NWA\Traces\test.s1p"  # Name and path of the s2p file on the instrument
pc_filename = r"C:\Users\jjn17015\Downloads\Testcode from Daniel\traces\test.s1p"  # Name and path of the s2p file on the PC


def zvb8_setup():
    # Define variables
    resource = "TCPIP0::192.168.0.70::INSTR"  # VISA resource string for the device

    # Make sure you have the last version of the RsInstrument
    RsInstrument.assert_minimum_version("1.53.0")

    # Define the device handle
    Instrument = RsInstrument(resource, True, True, "SelectVisa='rs'")

    sleep(
        1
    )  # Eventually add some waiting time when reset is performed during initialization
    comprep(Instrument)
    comcheck(Instrument)
    meassetup(Instrument)
    return Instrument


def comprep(Instrument):
    """Preparation of the communication (termination, etc...)"""
    print(
        f"VISA Manufacturer: {Instrument.visa_manufacturer}"
    )  # Confirm VISA package to be chosen
    Instrument.visa_timeout = 5000  # Timeout for VISA Read Operations
    Instrument.opc_timeout = 5000  # Timeout for opc-synchronised operations
    Instrument.instrument_status_checking = (
        True  # Error check after each command, can be True or False
    )
    Instrument.clear_status()  # Clear status register


def close(Instrument):
    """Close the VISA session"""
    Instrument.close()


def comcheck(Instrument):
    """Check communication with the device"""

    # Just knock on the door to see if instrument is present
    idnResponse = Instrument.query_str("*IDN?")
    sleep(1)
    print("Hello, I am " + idnResponse)


def meassetup(Instrument):
    # RF Setup first
    Instrument.write_str_with_opc("SYSTEM:DISPLAY:UPDATE ON")  # Update Display
    Instrument.write_str_with_opc("SENSe1:FREQuency:Start 3e9")  # Set start frequency
    Instrument.write_str_with_opc("SENSe1:FREQuency:Stop 5e9")  # Set stop frequency
    Instrument.write_str_with_opc(
        "SENSe1:SWEep:POINts 501"
    )  # Set number of sweep points

    # Channel 1 is created by default, so we don't need to explicitly open it
    # Prepare S22 measurement in diagram 1
    Instrument.write_str_with_opc(
        "CALCulate1:PARameter:MEAS 'Trc1', 'S22'"
    )  # Create a trace on channel 1 and change to desired S-parameters
    Instrument.write_str_with_opc(
        "CALCulate1:Format MAGNitude"
    )  # Change active trace format to dB mag
    sleep(1)  # Wait for VNA response


def measure(Instrument):
    """Perform a single sweep measurement"""

    # data = Instrument.query_bin_or_ascii_float_list('CALCulate1:DATA? SDATa')   # Retrieve unformatted data (real and imaginary part) from Channel 1
    data = Instrument.query_bin_or_ascii_float_list(
        "CALCulate1:DATA? FDATa"
    )  # Retrieve formatted data from Channel 1
    sleep(1)  # Wait for VNA response

    # print("CH1 Trace Result Data is: ", data)
    # plt.plot(data)
    # plt.show()

    return data


def saves2p(Instrument):
    """Save the measurement to a s2p file"""
    Instrument.write_str_with_opc(
        f'MMEMory:STORe:TRACe:PORTs 1, "{s2p_filename}", COMPlex, 1, 2'
    )
    # An S2P file does only contain real and imaginary part of each scatter parameter of the measurement.
    # To extract e.g. the magnitude and phase data of each trace, better use the command
    # MMEMory:STORe:TRACe:CHANnel 1, 'tracefile.csv', FORM, LINPhase
    # Using this simple file format it will be stored in path
    # C:\Users\Public\Documents\Rohde-Schwarz\Vna


def fileget(Instrument):
    """Perform calibration with short element"""
    Instrument.read_file_from_instrument_to_pc(s2p_filename, pc_filename)


# ---------------------------
# Main Program begins here
# just calling the functions
# ---------------------------

z = zvb8_setup()
# d = measure(z)
# print(d)
saves2p(z)

# comprep()
# comcheck()
# meassetup()
# measure()
# saves2p()
# fileget()
# close()

# print('I am done')
