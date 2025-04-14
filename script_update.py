import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import sys

# Globals to hold the DataFrames
fandango_df = None
search_volume_df = None

def Placeholder():
    # Placeholder logic
    print("Running Placeholder function... (nothing here yet)")

def check_both_loaded():
    return fandango_df is not None and search_volume_df is not None

def prompt_continue():
    answer = input("\nDo you wish to continue? (Y/n): ").strip()
    if answer.lower() == 'n':
        print("Exiting script.")
        sys.exit()
    elif answer == 'Y':
        Placeholder()
    else:
        print("Invalid input. Exiting by default.")
        sys.exit()

def load_file(file_type):
    global fandango_df, search_volume_df

    file_path = filedialog.askopenfilename(
        title=f"Select {file_type}",
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

        messagebox.showinfo("Success", f"{file_type} loaded successfully with shape {df.shape}")
        print(f"\n=== {file_type} ===")
        print(df.head())

        if file_type == "Fandango Sales File":
            fandango_df = df
        elif file_type == "Search Volume File":
            search_volume_df = df

        # If both loaded, destroy GUI and prompt in terminal
        if check_both_loaded():
            root.destroy()  # Closes the GUI
            prompt_continue()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load {file_type}: {e}")
        return

# GUI setup
def main():
    global root
    root = tk.Tk()
    root.title("File Loader")
    root.geometry("350x150")

    tk.Label(root, text="Load your input files:").pack(pady=10)

    btn1 = tk.Button(root, text="Load Fandango Sales File", command=lambda: load_file("Fandango Sales File"))
    btn1.pack(pady=5)

    btn2 = tk.Button(root, text="Load Search Volume File", command=lambda: load_file("Search Volume File"))
    btn2.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
