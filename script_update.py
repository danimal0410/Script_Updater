import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import sys
from datetime import datetime
from alive_progress import alive_bar

# Globals to hold the DataFrames
fandango_df = None
search_volume_df = None
df_match_ref = pd.read_excel("./Matched_DMAs_Updated.xlsx")
df_merge_final = None
script_name = None

#Function to write to python script to Scripts folder
def write_py():
    global script_name
    now_var = datetime.now()
    script_name = f'script_{now_var}'
    with open(f'./Scripts/{script_name}', 'w') as file:
        file.write('_dma_modifier = max_aggregate([\n')
        for x in df_merge_final['DMA ID']:
            weight_var = (df_merge_final.loc[df_merge_final['DMA ID'] == x, 'Composite Score'].values[0])
            file.write(f'([dma_id == {x}], {weight_var}),\n')
        file.write('])\n')
        file.write('return _dma_modifier')

def make_script():
    global df_merge_final
    # Merge uploaded data frames with the matched reference file to combine all necessary data for weight calculatiopns.
    df_merge_1 = df_match_ref.merge(fandango_df, left_on='Fandango DMA', right_on='DMA Market')
    df_merge_final = df_merge_1.merge(search_volume_df, left_on='Search DMA', right_on='geo_name')
    
    #Use merged data to calculate Indexed Search Per Person, first by creating the search per person column, then avg, then Indexed Search PP column
    df_merge_final['Search PP'] = df_merge_final['Indexed Search'] / df_merge_final['Population']
    search_pp_avg = df_merge_final['Search PP'].mean()
    df_merge_final['Search PP Index'] = df_merge_final['Search PP'] / search_pp_avg

    #Use merged files to calculate Sales PP Index with new methodology to account for the percentage share of sales format
    df_merge_final['Population Share'] = df_merge_final['Population'] / df_merge_final['Population'].sum()
    df_merge_final['Sales PP Index'] = df_merge_final['Primary - Share of Tickets Sold'] / df_merge_final['Population Share']

    #Add final weighting column for each DMA
    df_merge_final['Composite Score'] = ((df_merge_final['Sales PP Index'] * 0.5) +  (df_merge_final['Search PP Index'] * 0.5))

    #Add excel export for testing purposes
    date = datetime.now()
    print('Log file exported')
    df_merge_final.to_excel(f'./Logs/log_export_{date}.xlsx')

    #link to write_py
    write_py()

def check_both_loaded():
    return fandango_df is not None and search_volume_df is not None

def prompt_continue():
    answer = input("\nDo you wish to continue? (Y/n): ").strip()
    if answer.lower() == 'n':
        print("Exiting script.")
        sys.exit()
    elif answer == 'Y':
        make_script()
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
            fandango_df = df.drop('Row', axis=1)
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
