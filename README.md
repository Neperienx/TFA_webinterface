# TFA Web Interface

A simple **Python-only web interface** for exploring and visualizing your climate data. The first version in this repository is built with **Streamlit**, so you can run it locally with a few commands and immediately get an interactive browser UI for:

- loading the included CSV file or your own export,
- visualizing one or more measurements on an interactive chart,
- selecting a time frame,
- selecting or unselecting signals from the GUI,
- reviewing summary statistics and filtered raw data.

## What is included

- `app.py` – the Streamlit application.
- `requirements.txt` – Python dependencies needed to run the interface.
- `KlimaLoggPro.csv` – the sample dataset already in the repository.

## Features implemented in this first version

### 1. Interactive data visualization
The app reads the CSV file, converts timestamps, handles missing values such as `---`, and plots the selected data series on an interactive time-series chart.

### 2. Time-frame selection
A date-range picker in the sidebar lets you focus on the exact period you want to analyze.

### 3. Select / unselect signals
A multiselect widget in the sidebar lets you turn individual measurements on or off without editing code.

### 4. Data summary and inspection
Below the chart, the app shows:
- summary statistics for the selected signals,
- a filtered raw-data table for inspection.

---

## Step-by-step setup

## 1) Make sure Python is installed
Use **Python 3.11 or newer** if possible.

Check your version:

```bash
python --version
```

If that does not work, try:

```bash
python3 --version
```

## 2) Open a terminal in this project folder
If you already cloned or downloaded the repository, move into it:

```bash
cd /path/to/TFA_webinterface
```

## 3) Create a virtual environment
Creating a virtual environment keeps the project dependencies isolated.

### Linux / macOS
```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 4) Install the required packages
Install everything listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 5) Start the web interface
Run the Streamlit app:

```bash
streamlit run app.py
```

When Streamlit starts, it will print a local URL such as:

```text
http://localhost:8501
```

Open that address in your browser.

---

## How to use the interface

### Option A – use the bundled sample data
If you just launch the app, it will automatically load `KlimaLoggPro.csv`.

### Option B – upload your own CSV
Use the **Upload a CSV export** control in the sidebar.

For best results, your file should follow the same structure as the sample file:
- a `Timestamp` column,
- semicolon-separated values,
- comma decimal values,
- missing values optionally marked as `---`.

### In the sidebar
After loading data, use the sidebar to:

1. **Choose a time frame** using the date selector.
2. **Select or unselect signals** using the multiselect widget.
3. Instantly update the graph and tables.

### In the main page
You will see:

- a metrics row with row count, signal count, and selected date span,
- an interactive line chart,
- a summary statistics table,
- a filtered raw-data table.

---

## Project structure

```text
TFA_webinterface/
├── app.py
├── KlimaLoggPro.csv
├── README.md
└── requirements.txt
```

---

## Troubleshooting

### `pip install -r requirements.txt` fails
Try upgrading pip first:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### `streamlit: command not found`
Run Streamlit through Python instead:

```bash
python -m streamlit run app.py
```

### The app opens but no chart is shown
Make sure:
- the selected date range contains data,
- at least one signal is selected,
- your uploaded CSV follows the expected structure.

---

## Suggested next steps

Good next features for the app would be:

- hourly / daily / weekly aggregation,
- sensor grouping presets,
- downloadable filtered exports,
- anomaly detection,
- comparison views between sensors,
- custom dashboards.

If you want, I can next help you add:
1. aggregation controls,
2. export buttons,
3. multiple chart types,
4. a cleaner dashboard layout.
