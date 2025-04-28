# 📄 README: Data Merge & DV360 Script Generator

## 📚 Overview

This Python script does the following:
- Loads two user-selected Excel (or CSV) files:
  - A Fandango Sales file
  - A Search Volume file
- Merges them with a reference DMA mapping file (`Matched_DMAs_Updated.xlsx`).
- Calculates several metrics:
  - **Indexed Search Per Person**
  - **Sales Per Person Index**
  - **Composite Score** (final weight per DMA)
- Exports a log of the merged/calculated dataset.
- Auto-generates a DV360-ready Python script inside the `Scripts/` directory, applying calculated DMA modifiers.

The script **relies heavily on a GUI prompt** for file selection and a terminal prompt for final confirmation.

---

## ⚙️ Dependencies

You must have the following installed:

- Python 3.7+
- **Packages:**
  - `pandas`
  - `tkinter` (standard with Python, but confirm it's working)
  - `os`
  - `sys`
  - `datetime`
  - `alive-progress` (for progress bar visualization)

Install all non-standard packages:
```bash
pip install pandas alive-progress
```

✅ `tkinter` usually comes with Python installations. If it's missing:
- On Ubuntu/Debian: `sudo apt-get install python3-tk`
- On MacOS/Windows: reinstall Python with the "tcl/tk" option checked.

---

## 🗂️ Project Structure

Expected file and folder layout:

```
.
├── Matched_DMAs_Updated.xlsx    # Static mapping file (must exist in root)
├── Scripts/                     # Output folder for generated DV360 scripts
├── Logs/                        # Output folder for log files
└── script_update.py             # This script
```

> 🔥 If `Scripts/` or `Logs/` folders don't exist, the script **WILL fail**. Create them manually.

---

## 🚀 How to Use

1. **Prepare Files:**
   - `Matched_DMAs_Updated.xlsx` must be in the same folder as this script.
   - Create empty `Scripts/` and `Logs/` directories if missing.

2. **Run the script:**
   ```bash
   python script_update.py
   ```

3. **Load Files:**
   - Load Fandango Sales File first.
   - Load Search Volume File next.

4. **Confirm Prompt:**
   - After both files are loaded, you'll be prompted in terminal to continue (`Y` to proceed).

5. **Output:**
   - Merged data exported to `Logs/`.
   - A new DV360 upload script generated inside `Scripts/`, named `script_YYYY-MM-DD HH:MM:SS.ssssss`.

---

## 🧹 To-Do List (a.k.a Known Issues and Improvements)

- [ ] Automatically create `Scripts/` and `Logs/` folders if missing.
- [ ] Add better error handling if files are missing critical columns.
- [ ] Improve filename sanitation (currently uses raw datetime — ugly and fragile).
- [ ] Allow user to specify custom output filenames.
- [ ] Remove GUI dependency (allow pure CLI operation for server environments).
- [ ] Add full logging (not just Excel export) for debugging failures.
- [ ] Use argparse instead of hardcoded flow control for better flexibility.

---

## ⚠️ Important Warnings

- If your Fandango or Search Volume files have different column names than expected, the script will **crash without a helpful error**.
- Any pop-up error messages will close once acknowledged — no error logs are kept.
- Be careful when rerunning — the script **overwrites outputs** without warning.

---

## ✍️ Author

Internal use script. No warranty. Not production-ready. Use at your own risk.  
Last updated: April 2025.

---

Would you like me to also give you a **more professional "polished" version** (in case you need a client-facing one)?  
Or a quick **bash script** that checks if the `Scripts/` and `Logs/` folders exist and creates them automatically? 🚀