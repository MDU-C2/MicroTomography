from tkinter import filedialog
import scipy as sp

# Create a function to save data to a CSV file
def save_model(data):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".mat", 
        filetypes=[("MAT Files", "*.mat")]
    )

    message = "Saving cancel"

    if file_path:
        #with open(file_path, 'w', newline='') as matfile:
            # Save the data to a MAT file
        sp.io.savemat(file_path, {'surfacePoint': data})
        message = f"Model saved to: {file_path}"

    return message

