from tkinter import filedialog
import pandas as pd


# Create a function to save data to a CSV file
def save_model(data):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
    )

    message = "Saving cancel"

    if file_path:
        with open(file_path, "w", newline="") as csvfile:
            df = pd.DataFrame(data, columns=["X_value", "Y_value", "Z_value"])

            # Save the DataFrame to a CSV file
            df.to_csv(
                csvfile, index=False
            )  # Specify index=False to avoid writing row numbers as a column
            message = f"Model saved to: {file_path}"

    return message
