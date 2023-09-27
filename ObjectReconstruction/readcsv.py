import pandas as pd

class readFile():
    def readCSV(filename):
        data = pd.read_csv(filename, header=None, delimiter=r"\s+")
        return data.values
        