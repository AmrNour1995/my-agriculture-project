# 🌾 Agricultural Data Analysis Project

A structured, end-to-end data analysis pipeline built on the FAO global agriculture dataset.  
The project covers 180+ countries and 14 years of production data (2000–2013), answering real analytical questions through SQL queries, Python processing, and publication-ready visualizations.

---

## Why This Project Exists

Most agriculture datasets sit untouched in CSV files.  
This project turns raw FAO data into a clear narrative:  
**which countries grew, which declined, what crops dominated, and whether diversity actually drives output.**

---

## Project Structure

```
agro_project/
│
├── agro_analyzer.py      ← main script (all logic lives here)
├── FAO.csv               ← raw dataset (not included, see below)
├── README.md             ← you are here
│
└── outputs/
    └── plots/            ← all charts auto-saved here (9 PNG files)
```

---

## What the Analysis Covers

| # | Section | Question Being Answered |
|---|---------|------------------------|
| 1 | Top Growth Rate | Which 5 countries grew fastest between 2000–2004 and 2005–2009? |
| 2 | Top Producers 2013 | Who dominated global output in 2013? |
| 3 | Ghana KPI | What was Ghana's total production in 2013? |
| 4 | USA Comparison | Did the US grow or shrink across the two periods? |
| 5 | Annual Expansion | Who added the most absolute tonnage per year? |
| 6 | Production Decline | Which countries contracted the most on average? |
| 7 | Top Crops | What are the 10 highest-volume crops globally? |
| 8 | Crop Correlation | Do top crops move together or independently over time? |
| 9 | Diversity vs Output | Does growing more crop types lead to higher total production? |
| 10 | Best & Worst Years | Which single year was the global peak — and which was the low? |

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| `Python 3.x` | Core language |
| `pandas` | Data loading, cleaning, manipulation |
| `matplotlib` + `seaborn` | All visualizations |
| `SQLAlchemy` | Python–SQL bridge |
| `SQL Server Express` | Query engine (runs locally) |
| `numpy` | Correlation and trendline math |

---

## Setup & Installation

### 1. Install dependencies

```bash
pip install pandas matplotlib seaborn sqlalchemy numpy pyodbc
```

### 2. Make sure SQL Server Express is running

The project connects to a local SQL Server instance:

```
Server:   localhost\SQLEXPRESS
Database: AgricultureDB
Auth:     Windows Authentication (Trusted Connection)
```

> If your setup is different, update `CONNECTION_STRING` at the top of `agro_analyzer.py`.

### 3. Add the dataset

Place your `FAO.csv` file in the same folder as `agro_analyzer.py`.  
The dataset is available from the [FAO Statistics Division](https://www.fao.org/faostat/en/#data) or via public Kaggle mirrors.

### 4. Run

```bash
python agro_analyzer.py
```

On startup, the script will:
- Create the `outputs/plots/` folder automatically
- Load and clean the CSV
- Push data to SQL Server
- Run all 10 analyses in sequence
- Save each chart as a numbered PNG **and** display it on screen

---

## Output Charts

All charts are saved to `outputs/plots/` with numbered names so they stay ordered:

```
01_top_growth_rate.png
02_top_producers_2013.png
03_usa_lollipop.png
04_top_expansion.png
05_top_decline.png
06_top_items.png
07_crop_correlation.png
08_diversity_vs_production.png
09_best_worst_years.png
```

---

## Architecture

The codebase is split into four focused classes — each with a single responsibility:

```
AgroDataLoader   →   loads CSV, cleans data, pushes to SQL
AgroQueries      →   all SQL statements in one place
AgroCharts       →   reusable chart functions (save + show)
AgroAnalyzer     →   ties everything together, runs the report
```

This separation means:
- Changing a query? Go to `AgroQueries`. One place.
- Changing chart styling? Go to `AgroCharts`. One place.
- Adding a new analysis section? Add one method to `AgroAnalyzer`.

---

## A Note on Data Cleaning

The original dataset uses empty cells for missing production values.  
Instead of replacing them with zeros (which would distort averages and totals),  
this project converts them to `NaN` and lets SQL's `SUM` and Python's `mean` handle them correctly.

```python
# What the original code did — misleading
df.fillna(0, inplace=True)

# What this project does — accurate
df[YEARS] = df[YEARS].apply(pd.to_numeric, errors="coerce")
```

---

## Possible Extensions

- Add a Streamlit dashboard for interactive filtering by country or crop
- Export a PDF summary report alongside the PNG charts
- Extend the year range if a newer FAO dataset is available
- Add a forecasting section using simple regression on the yearly totals

---

## Dataset Source

**Food and Agriculture Organization of the United Nations (FAO)**  
FAOSTAT — Crops and livestock products  
[https://www.fao.org/faostat](https://www.fao.org/faostat)
