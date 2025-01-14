import pandas as pd
from ObjectReconstruction.surface_reconstruction import poisson_surface_reconstruction

class emptyClass:
    """
    A empty class for robot connection in init. It do nothing.
    """
    pass

class class_GUI:
    """
    Create a mesh variable and read quaternion in the csv file. 
    If there is no csv file, then create a csv file with standard quaternion [0.999954527, 0.00941712207, 0.00150357889, 9.45543129e-06]
    """
    def __init__(self):
        
        self.mesh = []
        self.robot = emptyClass
        try:
            data = pd.read_csv("GUI/quaternions.csv")
            self.quaternion = data["Quaternions"].to_list()
        except:
            print("No quaternion.csv in GUI Folder. We create a new one.")
            self.quaternion = []
            self.changeQua([0.999954527, 0.00941712207, 0.00150357889, 9.45543129e-06])
            data = pd.read_csv("GUI/quaternions.csv")
            self.quaternion = data["Quaternions"].to_list()

    #Update the quaternions in both variable and csv file.
    def changeQua(self, quaternions):
        self.quaternion = quaternions
        df = pd.DataFrame(self.quaternion, columns=["Quaternions"])
        df.to_csv('GUI/quaternions.csv', index=False)  # Specify index=False to avoid writing row numbers as a column

    #Update the mesh in both variable and csv file.
    def recon3D(self, result):
        self.mesh = poisson_surface_reconstruction(result, save=False,  re_resolution=5)