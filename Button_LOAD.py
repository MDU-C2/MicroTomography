import tkinter as tk
from tkinter import filedialog


def load_on_click():
    # Create a Tkinter root window (it won't be displayed)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog window for selecting a file
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("CSV Files", "*.csv")]
    )

    # Check if a file was selected
    if file_path:
        return file_path
    else:
        print("No file selected")

    # Close the Tkinter root window (optional)
    root.destroy()