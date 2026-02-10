# CSVForge

A minimalist and modular Python toolkit for cleaning, normalizing, and standardizing CSV datasets. Originally designed for healthcare data integration, **CSVForge** is built to be data-agnostic, making it suitable for any tabular data workflow.

## Core Features

- **Data Separation:** Effortlessly split active records from deleted ones based on status fields.
- **Schema Standardization:** Dynamically rename and unify column headers using pattern matching.
- **Smart Deduplication:** Group records and resolve duplicates by prioritizing specific data sources (e.g., Master systems vs. secondary sources).
- **Environment Agnostic:** Optimized for both Windows and Linux environments.
- **Auto-Directory Management:** Built-in path handling for `raw`, `cleaned`, and `processed` data stages.

## Setup

```bash
# 1. Clone and enter the project
git clone [https://github.com/](https://github.com/)<your-username>/CSVForge.git
cd CSVForge

# 2. Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```
