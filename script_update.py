import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

def load_file():
    file_path = filedialog.askopenfilename(
        title="Select Excel or CSV file",
        filetypes=(("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv"), ("All files", "*.*"))
    )

    if not file_path:
        return  # User cancelled

    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext in ('.xls', '.xlsx'):
            df = pd.read_excel(file_path)
        else:
            messagebox.showerror("Unsupported Format", f"File type {ext} not supported.")
            return

        # Show a basic confirmation message
        messagebox.showinfo("Success", f"Loaded file with shape {df.shape}")
        print(df.head())  # Print to console for inspection
        return df

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")
        return

# Basic GUI
def main():
    root = tk.Tk()
    root.title("Excel/CSV to DataFrame Loader")
    root.geometry("300x100")

    btn = tk.Button(root, text="Select File", command=load_file)
    btn.pack(pady=30)

    root.mainloop()

if __name__ == "__main__":
    main()
