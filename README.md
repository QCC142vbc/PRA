# Production Rate Analyzer

Production performance analysis tool built with Python and Streamlit.

The project calculates theoretical production rate, actual production rate, efficiency, bottleneck status, historical trends, and production forecasts.

## Features

* Theoretical production rate calculation
* Actual production rate calculation
* Production efficiency
* Bottleneck detection
* Measurement storage
* Historical measurement analysis
* Production trend analysis
* Production forecasting
* Automated tests

## Project Structure

```text
LRP/
├── core/
│   └── production_rate.py
│
├── dashboard/
│   └── app.py
│
├── tests/
│   └── test_production_rate.py
│
├── data/
│   └── measurements.csv
│
└── README.md
```

## Requirements

* Python 3.11+
* Streamlit
* Pandas
* Pytest

## Installation

Install the required packages:

```bash
pip install streamlit pandas pytest
```

## Run

From the project root:

```bash
streamlit run dashboard/app.py
```

## Run Tests

From the project root:

```bash
pytest
```

## Data

Measurements are stored in:

```text
data/measurements.csv
```

Each measurement contains:

* timestamp
* machine count
* cycle time
* output per cycle
* measurement time
* actual output
* theoretical rate
* actual rate
* efficiency

## Version

Current version: v0.8

v0.8 focuses on stabilization, validation, testing, refactoring, and production optimization.
