from tkinter import filedialog
import pandas as pd

# Create a function to save data to a CSV file
def save_model_to_csv(data):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv", 
        filetypes=[("CSV Files", "*.csv")]
    )

    if file_path:
        with open(file_path, 'w', newline='') as csvfile:
            df = pd.DataFrame(data)

            # Save the DataFrame to a CSV file
            df.to_csv(csvfile, index=False)  # Specify index=False to avoid writing row numbers as a column

        return file_path

