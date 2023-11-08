from tkinter import filedialog
import pandas as pd


def load_model():
    # Open a file dialog window for selecting a file
    file_path = filedialog.askopenfilename(
        title="Select a File", filetypes=[("CSV Files", "*.csv")]
    )

    message = "None file selected"

    # Check if a file was selected
    if file_path:
        data = pd.read_csv(file_path)
        message = f"Open model from: {file_path}"
        return data, message

    return None, message  # no file selected
