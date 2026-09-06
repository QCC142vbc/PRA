# Production Rate Analyzer

Production performance analysis tool built with Python and Streamlit.

The project calculates theoretical production rate, actual production rate, efficiency, bottleneck status, historical trends, production analytics, and advanced production forecasts.

## Features

* Theoretical production rate calculation

* Actual production rate calculation

* Production efficiency

* Bottleneck detection

* Measurement storage

* Historical measurement analysis

* Production trend analysis

* Production forecasting

* Advanced forecasting methods

  * Moving Average
  * Weighted Moving Average
  * Trend Forecast

* Forecast accuracy evaluation

* Forecast reliability analysis

* Production performance analytics

  * Average efficiency
  * Minimum and maximum efficiency
  * Median efficiency
  * Average production rate
  * Minimum and maximum production rate
  * Median production rate
  * Standard deviation
  * Coefficient of variation

* Forecast comparison

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

## Forecasting

The analyzer supports multiple forecasting methods:

* Moving Average — forecasts production rate using the latest measurements.

* Weighted Moving Average — gives greater importance to more recent measurements.

* Trend Forecast — estimates the next production rate using the historical production trend.

Forecast performance can also be evaluated against historical actual production rates.

The system calculates:

* Forecast accuracy

* Average forecast error

* Forecast reliability

* Coefficient of variation

* Forecast comparison between methods

## Analytics

Historical measurements can be analyzed to identify production performance and stability.

The analytics module calculates:

* Average efficiency

* Minimum efficiency

* Maximum efficiency

* Median efficiency

* Average actual production rate

* Minimum actual production rate

* Maximum actual production rate

* Median actual production rate

* Standard deviation

* Coefficient of variation

These metrics provide a more detailed view of production performance than a simple average.

## Version

Current version: v0.10

v0.10 focuses on advanced forecasting, forecast accuracy tracking, forecast reliability, production analytics, and comparison of forecasting methods.
