from tkinter import filedialog


def load_model():
    # Open a file dialog window for selecting a file
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("CSV Files", "*.csv")]
    )

    # Check if a file was selected
    if file_path:
        return file_path

