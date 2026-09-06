import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from core.production_rate import (
    calculate_production_rate,
    calculate_actual_production_rate,
    calculate_efficiency,
    save_measurement,
    load_measurements,
    calculate_trend,
    detect_bottleneck,
    forecast_production_rate
)


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Production Rate Analyzer",
    layout="wide"
)

st.title("Production Rate Analyzer")

st.write(
    "Production performance and historical measurement analysis."
)


# =========================
# INPUT
# =========================

st.subheader("Production Setup")

col1, col2, col3 = st.columns(3)

with col1:
    machine_count = st.number_input(
        "Machine count",
        min_value=1,
        value=11,
        step=1
    )

with col2:
    cycle_time = st.number_input(
        "Cycle time (sec)",
        min_value=0.001,
        value=0.583,
        step=0.001
    )

with col3:
    output_per_cycle = st.number_input(
        "Output per cycle",
        min_value=0.001,
        value=1.0,
        step=0.1
    )

col1, col2 = st.columns(2)

with col1:
    measurement_time = st.number_input(
        "Measurement time (sec)",
        min_value=0.001,
        value=160.0,
        step=1.0
    )

with col2:
    actual_output = st.number_input(
        "Actual production",
        min_value=0.0,
        value=2750.0,
        step=1.0
    )


# =========================
# CALCULATE
# =========================

if st.button("Calculate", type="primary"):

    theoretical = calculate_production_rate(
        machine_count=machine_count,
        cycle_time=cycle_time,
        output_per_cycle=output_per_cycle,
        measurement_time=measurement_time
    )

    actual = calculate_actual_production_rate(
        actual_output=actual_output,
        measurement_time=measurement_time
    )

    efficiency = calculate_efficiency(
        theoretical_rate=theoretical["rate_per_second"],
        actual_rate=actual["actual_rate_per_second"]
    )

    bottleneck = detect_bottleneck(
        efficiency["efficiency_percent"]
    )

    st.session_state["theoretical"] = theoretical
    st.session_state["actual"] = actual
    st.session_state["efficiency"] = efficiency
    st.session_state["bottleneck"] = bottleneck


# =========================
# CURRENT RESULT
# =========================

if "theoretical" in st.session_state:

    theoretical = st.session_state["theoretical"]
    actual = st.session_state["actual"]
    efficiency = st.session_state["efficiency"]
    bottleneck = st.session_state["bottleneck"]

    st.divider()

    st.subheader("Current Production Performance")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Theoretical Rate",
            f"{theoretical['rate_per_second']:.2f} / sec"
        )

    with col2:
        st.metric(
            "Actual Rate",
            f"{actual['actual_rate_per_second']:.2f} / sec"
        )

    with col3:
        st.metric(
            "Efficiency",
            f"{efficiency['efficiency_percent']:.2f}%"
        )


    # =========================
    # BOTTLENECK DETECTION
    # =========================

    st.divider()

    st.subheader("Bottleneck Detection")

    if bottleneck["status"] == "normal":

        st.success(
            f"Status: Normal "
            f"({bottleneck['efficiency']:.2f}%)"
        )

    elif bottleneck["status"] == "warning":

        st.warning(
            f"Status: Warning "
            f"({bottleneck['efficiency']:.2f}%)"
        )

    else:

        st.error(
            f"Status: Bottleneck "
            f"({bottleneck['efficiency']:.2f}%)"
        )


    # =========================
    # DETAILED RESULTS
    # =========================

    st.divider()

    st.subheader("Detailed Results")

    col1, col2 = st.columns(2)

    with col1:

        st.write("Theoretical Production")

        st.write(
            f"Per second: "
            f"{theoretical['rate_per_second']:.2f}"
        )

        st.write(
            f"Per minute: "
            f"{theoretical['rate_per_minute']:.2f}"
        )

        st.write(
            f"Per hour: "
            f"{theoretical['rate_per_hour']:.2f}"
        )

        st.write(
            f"Measurement output: "
            f"{theoretical['total_output']:.2f}"
        )

    with col2:

        st.write("Actual Production")

        st.write(
            f"Per second: "
            f"{actual['actual_rate_per_second']:.2f}"
        )

        st.write(
            f"Per minute: "
            f"{actual['actual_rate_per_minute']:.2f}"
        )

        st.write(
            f"Per hour: "
            f"{actual['actual_rate_per_hour']:.2f}"
        )

        st.write(
            f"Actual output: "
            f"{actual['actual_output']:.2f}"
        )


    # =========================
    # SAVE
    # =========================

    st.divider()

    st.subheader("Measurement")

    if st.button("Save Measurement"):

        saved_measurement = save_measurement(
            machine_count=machine_count,
            cycle_time=cycle_time,
            output_per_cycle=output_per_cycle,
            measurement_time=measurement_time,
            actual_output=actual_output,
            theoretical_rate=theoretical[
                "rate_per_second"
            ],
            actual_rate=actual[
                "actual_rate_per_second"
            ],
            efficiency=efficiency[
                "efficiency_percent"
            ]
        )

        st.success(
            "Measurement saved successfully."
        )

        st.json(saved_measurement)


# =========================
# HISTORICAL DATA
# =========================

st.divider()

st.subheader("Historical Measurements")

measurements = load_measurements()

if not measurements:

    st.info(
        "No historical measurements available."
    )

else:

    # =========================
    # STATISTICS
    # =========================

    efficiencies = [
        float(measurement["efficiency"])
        for measurement in measurements
    ]

    actual_rates = [
        float(measurement["actual_rate"])
        for measurement in measurements
    ]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Measurements",
            len(measurements)
        )

    with col2:
        st.metric(
            "Average Efficiency",
            f"{sum(efficiencies) / len(efficiencies):.2f}%"
        )

    with col3:
        st.metric(
            "Best Efficiency",
            f"{max(efficiencies):.2f}%"
        )

    with col4:
        st.metric(
            "Worst Efficiency",
            f"{min(efficiencies):.2f}%"
        )


    # =========================
    # HISTORY TABLE
    # =========================

    st.divider()

    display_data = []

    for measurement in measurements:

        display_data.append({
            "Timestamp": measurement["timestamp"],
            "Machines": int(
                measurement["machine_count"]
            ),
            "Cycle Time": float(
                measurement["cycle_time"]
            ),
            "Measurement Time": float(
                measurement["measurement_time"]
            ),
            "Actual Output": float(
                measurement["actual_output"]
            ),
            "Theoretical Rate": float(
                measurement["theoretical_rate"]
            ),
            "Actual Rate": float(
                measurement["actual_rate"]
            ),
            "Efficiency": float(
                measurement["efficiency"]
            )
        })

    st.dataframe(
        display_data,
        width="stretch",
        hide_index=True
    )


# =========================
# TREND ANALYSIS
# =========================

st.divider()

st.subheader("Production Trend")

trend = calculate_trend(measurements)

if trend["trend"] == "no_data":

    st.info(
        "No data available for trend analysis."
    )

elif trend["trend"] == "insufficient_data":

    st.info(
        "At least two measurements are required."
    )

else:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Trend",
            trend["trend"].replace(
                "_",
                " "
            ).title()
        )

    with col2:
        st.metric(
            "Efficiency Change",
            f"{trend['change_percent']:+.2f}%"
        )

    with col3:
        st.metric(
            "Average Actual Rate",
            f"{trend['average_actual_rate']:.2f} / sec"
        )

    st.divider()

    # =========================
    # EFFICIENCY CHART
    # =========================

    chart_data = pd.DataFrame({
        "Timestamp": [
            measurement["timestamp"]
            for measurement in measurements
        ],
        "Efficiency": [
            float(measurement["efficiency"])
            for measurement in measurements
        ]
    })

    chart_data["Timestamp"] = pd.to_datetime(
        chart_data["Timestamp"]
    )

    chart_data = chart_data.set_index(
        "Timestamp"
    )

    st.line_chart(
        chart_data["Efficiency"]
    )

    st.write(
        f"First efficiency: "
        f"{trend['first_efficiency']:.2f}%"
    )

    st.write(
        f"Last efficiency: "
        f"{trend['last_efficiency']:.2f}%"
    )


# =========================
# PRODUCTION FORECAST
# =========================

st.divider()

st.subheader("Production Forecast")

forecast = forecast_production_rate(measurements)

if forecast["status"] == "no_data":

    st.info(
        "No data available for forecasting."
    )

else:

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Forecast Production Rate",
            f"{forecast['forecast_rate']:.2f} / sec"
        )

    with col2:
        st.metric(
            "Based On Measurements",
            forecast["measurement_count"]
        )