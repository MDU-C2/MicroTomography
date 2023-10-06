from tkinter import filedialog
import scipy as sp
import numpy as np

def load_model():
    # Open a file dialog window for selecting a file
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("MAT Files", "*.mat")]
    )

    message = "None file selected"

    # Check if a file was selected
    if file_path:
        f = sp.io.loadmat(file_path,squeeze_me=False)
        data = np.array(f["surfacePoint"]) # Gets the surface points from the .mat file
        message = f"Open model from: {file_path}"
        return data, message
    
    return None, message # no file selected