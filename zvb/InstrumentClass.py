import numpy as np
from time import sleep


class VisaInstrument:
    def __init__(self, RsInstrument):
        """Preparation of the communication (termination, etc...)"""

        self.Inst = RsInstrument

        print("Preparing communication...", end=" ")

        self.Inst.visa_timeout = 5000  # Timeout for VISA Read Operations
        self.Inst.opc_timeout = 5000  # Timeout for opc-synchronised operations
        self.Inst.instrument_status_checking = True  # Error check after each command, can be True or False
        self.Inst.clear_status()  # Clear status register
        print("DONE!", end=" ")
        print(f'VISA Manufacturer: {self.Inst.visa_manufacturer}')  # Confirm VISA package to be chosen

    def comcheck(self):
        """Check communication with the device"""

        print("Checking communication...", end=" ")
        # Just knock on the door to see if instrument is present
        idnresponse = self.Inst.query_str('*IDN?')
        sleep(1)
        print('Hello, I am ' + idnresponse, end=" ")
        print("DONE!")

    def meassetup(self, f_start: float, f_stop: float, points: int, meas_param: str = "S11", format: str =
    "MAGNitude") -> None:
        print("Setting up measurement environment...", end=" ")

        # RF Setup first
        # Be sure to have the display updated whilst remote control
        self.Inst.write_str_with_opc('SYSTEM:DISPLAY:UPDATE ON')

        # Set start frequency
        self.Inst.write_str_with_opc('SENSe1:FREQuency:Start ' + str(f_start))

        # Set stop frequency
        self.Inst.write_str_with_opc('SENSe1:FREQuency:Stop ' + str(f_stop))

        # Set sweep points
        self.Inst.write_str_with_opc('SENSe1:SWEep:POINts ' + str(points))

        # Channel 1 is created by default, so we don't need to explicitly open it
        # Prepare SMN measurement in diagram 1
        self.Inst.write_str_with_opc("CALCulate1:PARameter:MEAS 'Trc1', '" + meas_param + "'")  # Create a trace on
        # channel 1 and change to desired S-parameters
        self.Inst.write_str_with_opc('CALCulate1:Format ' + format)  # Change active trace format to dB mag

        sleep(1)  # Wait for VNA response
        print("DONE!")
        return

    # def saves2p(self, snp_filename: str, pc_filename: str):
    #     """Save the measurement to a s2p file"""
    #     print("Saving measurement...", end="")
    #     self.Inst.write_str_with_opc(f'MMEMory:STORe:TRACe:PORTs 1, "{snp_filename}", COMPlex, 1, 2')
    #     # An S2P file does only contain real and imaginary part of each scatter parameter of the measurement.
    #     # To extract e.g. the magnitude and phase data of each trace, better use the command
    #     # MMEMory:STORe:TRACe:CHANnel 1, 'tracefile.csv', FORM, LINPhase
    #     # Using this simple file format it will be stored in path C:\Users\Public\Documents\Rohde-Schwarz\Vna
    #     sleep(1)  # Wait for VNA response
    #     self.Inst.read_file_from_instrument_to_pc(snp_filename, pc_filename)
    #     sleep(1)  # Wait for VNA response
    #     print("DONE!")

    def measure(self, meas_param: str = "S11"):
        # Channel 1 is created by default, so we don't need to explicitly open it
        # Prepare SMN measurement in diagram 1
        self.Inst.write_str_with_opc("CALCulate1:PARameter:MEAS 'Trc1', '" + meas_param + "'")  # Create a trace on
        sleep(1)  # Wait for VNA response

        freq = self.Inst.query_bin_or_ascii_float_list('CALC:DATA:STIM?')  # Request number of frequency points
        data_temp = self.Inst.query_bin_or_ascii_float_list('CALCulate1:DATA? SDATa')

        data_real = data_temp[0::2]
        data_imag = data_temp[1::2]
        data = np.vectorize(complex)(data_real, data_imag)

        return freq, data

    def close(self):
        """Close the VISA session"""

        self.Inst.close()

