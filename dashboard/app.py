
import csv
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================
# PROJECT PATH
# =========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =========================
# CORE IMPORTS
# =========================

from core.production_rate import (
    calculate_production_rate,
    calculate_actual_production_rate,
    calculate_efficiency,
    save_measurement,
    load_measurements,
    calculate_trend,
    detect_bottleneck,
    forecast_production_rate,
    calculate_analytics,
    moving_average_forecast,
    weighted_moving_average_forecast,
    trend_forecast,
    calculate_forecast_accuracy,
    calculate_forecast_reliability,
    evaluate_forecast_accuracy
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

    try:

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
            theoretical_rate=theoretical[
                "rate_per_second"
            ],
            actual_rate=actual[
                "actual_rate_per_second"
            ]
        )

        bottleneck = detect_bottleneck(
            efficiency[
                "efficiency_percent"
            ]
        )

        st.session_state["theoretical"] = theoretical
        st.session_state["actual"] = actual
        st.session_state["efficiency"] = efficiency
        st.session_state["bottleneck"] = bottleneck

        st.success("Calculation completed.")

    except ValueError as error:

        st.error(
            f"Calculation error: {error}"
        )


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

        try:

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

        except (
            OSError,
            ValueError,
            csv.Error
        ) as error:

            st.error(
                f"Could not save measurement: {error}"
            )


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
    # TREND DATA
    # =========================

    trend = calculate_trend(measurements)

    # =========================
    # STATISTICS
    # =========================

    if trend["trend"] not in (
        "no_data",
        "insufficient_data"
    ):

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Measurements",
                len(measurements)
            )

        with col2:
            st.metric(
                "Average Efficiency",
                f"{trend['average_efficiency']:.2f}%"
            )

        with col3:
            st.metric(
                "Best Efficiency",
                f"{trend['best_efficiency']:.2f}%"
            )

        with col4:
            st.metric(
                "Worst Efficiency",
                f"{trend['worst_efficiency']:.2f}%"
            )

    else:

        st.metric(
            "Measurements",
            len(measurements)
        )


    # =========================
    # HISTORY TABLE
    # =========================

    st.divider()

    display_data = []

    for measurement in measurements:

        try:

            display_data.append({
                "Timestamp": measurement["timestamp"],
                "Machines": int(
                    float(measurement["machine_count"])
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

        except (
            KeyError,
            TypeError,
            ValueError
        ):
            continue

    if display_data:

        st.dataframe(
            display_data,
            width="stretch",
            hide_index=True
        )

    else:

        st.warning(
            "No valid historical records available."
        )


    # =========================
    # V0.9 ANALYTICS
    # =========================

    st.divider()

    st.subheader("Advanced Analytics")

    analytics = calculate_analytics(
        measurements
    )

    if analytics["status"] == "ok":

        st.write(
            "Statistical analysis of historical production performance."
        )

        st.markdown("### Efficiency Analysis")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Average",
                f"{analytics['average_efficiency']:.2f}%"
            )

        with col2:
            st.metric(
                "Minimum",
                f"{analytics['minimum_efficiency']:.2f}%"
            )

        with col3:
            st.metric(
                "Maximum",
                f"{analytics['maximum_efficiency']:.2f}%"
            )

        with col4:
            st.metric(
                "Median",
                f"{analytics['median_efficiency']:.2f}%"
            )


        st.markdown("### Production Rate Analysis")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Average",
                f"{analytics['average_actual_rate']:.2f} / sec"
            )

        with col2:
            st.metric(
                "Minimum",
                f"{analytics['minimum_actual_rate']:.2f} / sec"
            )

        with col3:
            st.metric(
                "Maximum",
                f"{analytics['maximum_actual_rate']:.2f} / sec"
            )

        with col4:
            st.metric(
                "Median",
                f"{analytics['median_actual_rate']:.2f} / sec"
            )


        st.markdown("### Production Stability")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Standard Deviation",
                f"{analytics['standard_deviation']:.4f}"
            )

        with col2:
            st.metric(
                "Coefficient of Variation",
                f"{analytics['coefficient_of_variation']:.2f}%"
            )

    else:

        st.info(
            "Not enough valid data for advanced analytics."
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

    chart_data = []

    for measurement in measurements:

        try:

            chart_data.append({
                "Timestamp": measurement["timestamp"],
                "Efficiency": float(
                    measurement["efficiency"]
                )
            })

        except (
            KeyError,
            TypeError,
            ValueError
        ):
            continue

    if chart_data:

        chart_data = pd.DataFrame(
            chart_data
        )

        chart_data["Timestamp"] = pd.to_datetime(
            chart_data["Timestamp"],
            errors="coerce"
        )

        chart_data = chart_data.dropna(
            subset=["Timestamp"]
        )

        if not chart_data.empty:

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
# V0.10 ADVANCED FORECASTING
# =========================

st.divider()

st.subheader("Advanced Forecasting")

if not measurements:

    st.info(
        "No data available for forecasting."
    )

else:

    moving_average = moving_average_forecast(
        measurements,
        window=3
    )

    weighted_average = weighted_moving_average_forecast(
        measurements,
        window=3
    )

    trend_prediction = trend_forecast(
        measurements
    )

    reliability = calculate_forecast_reliability(
        measurements
    )

    # =========================
    # FORECAST ACCURACY
    # =========================

    moving_accuracy = evaluate_forecast_accuracy(
        measurements,
        method="moving_average",
        window=3
    )

    weighted_accuracy = evaluate_forecast_accuracy(
        measurements,
        method="weighted_moving_average",
        window=3
    )

    trend_accuracy = evaluate_forecast_accuracy(
        measurements,
        method="trend"
    )

    if (
        moving_average["status"] == "no_data"
        or weighted_average["status"] == "no_data"
        or trend_prediction["status"] == "no_data"
    ):

        st.info(
            "Not enough valid data for forecasting."
        )

    else:

        st.write(
            "Production rate forecasts using multiple forecasting methods."
        )

        # =========================
        # FORECAST METHODS
        # =========================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Moving Average",
                f"{moving_average['forecast_rate']:.2f} / sec"
            )

            st.caption(
                f"Window: {moving_average['window']} measurements"
            )

        with col2:

            st.metric(
                "Weighted Moving Average",
                f"{weighted_average['forecast_rate']:.2f} / sec"
            )

            st.caption(
                f"Window: {weighted_average['window']} measurements"
            )

        with col3:

            st.metric(
                "Trend Forecast",
                f"{trend_prediction['forecast_rate']:.2f} / sec"
            )

            st.caption(
                f"Slope: {trend_prediction['trend_slope']:+.4f} / measurement"
            )


        # =========================
        # FORECAST RELIABILITY
        # =========================

        st.divider()

        st.markdown("### Forecast Reliability")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Reliability",
                f"{reliability['reliability_percent']:.2f}%"
            )

        with col2:

            if reliability["status"] == "ok":

                st.metric(
                    "Coefficient of Variation",
                    f"{reliability['coefficient_of_variation']:.2f}%"
                )

            else:

                st.metric(
                    "Coefficient of Variation",
                    "N/A"
                )


        # =========================
        # FORECAST ACCURACY
        # =========================

        st.divider()

        st.markdown("### Forecast Accuracy")

        if (
            moving_accuracy["status"] == "ok"
            and weighted_accuracy["status"] == "ok"
            and trend_accuracy["status"] == "ok"
        ):

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Moving Average Accuracy",
                    f"{moving_accuracy['accuracy_percent']:.2f}%"
                )

                st.caption(
                    f"Average error: "
                    f"{moving_accuracy['average_error']:.4f} / sec"
                )

            with col2:

                st.metric(
                    "Weighted Average Accuracy",
                    f"{weighted_accuracy['accuracy_percent']:.2f}%"
                )

                st.caption(
                    f"Average error: "
                    f"{weighted_accuracy['average_error']:.4f} / sec"
                )

            with col3:

                st.metric(
                    "Trend Accuracy",
                    f"{trend_accuracy['accuracy_percent']:.2f}%"
                )

                st.caption(
                    f"Average error: "
                    f"{trend_accuracy['average_error']:.4f} / sec"
                )

        else:

            st.info(
                "Not enough historical data to evaluate forecast accuracy."
            )


        # =========================
        # FORECAST COMPARISON
        # =========================

        st.divider()

        st.markdown("### Forecast Comparison")

        forecast_comparison = pd.DataFrame({
            "Method": [
                "Moving Average",
                "Weighted Moving Average",
                "Trend"
            ],
            "Forecast Rate": [
                moving_average["forecast_rate"],
                weighted_average["forecast_rate"],
                trend_prediction["forecast_rate"]
            ],
            "Accuracy": [
                (
                    moving_accuracy["accuracy_percent"]
                    if moving_accuracy["status"] == "ok"
                    else None
                ),
                (
                    weighted_accuracy["accuracy_percent"]
                    if weighted_accuracy["status"] == "ok"
                    else None
                ),
                (
                    trend_accuracy["accuracy_percent"]
                    if trend_accuracy["status"] == "ok"
                    else None
                )
            ],
            "Average Error": [
                (
                    moving_accuracy["average_error"]
                    if moving_accuracy["status"] == "ok"
                    else None
                ),
                (
                    weighted_accuracy["average_error"]
                    if weighted_accuracy["status"] == "ok"
                    else None
                ),
                (
                    trend_accuracy["average_error"]
                    if trend_accuracy["status"] == "ok"
                    else None
                )
            ]
        })

        st.dataframe(
            forecast_comparison,
            width="stretch",
            hide_index=True
        )


        # =========================
        # CURRENT VS FORECAST
        # =========================

        try:

            latest_actual_rate = float(
                measurements[-1]["actual_rate"]
            )

            st.divider()

            st.markdown("### Current vs Forecast")

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Latest Actual Rate",
                    f"{latest_actual_rate:.2f} / sec"
                )

            with col2:

                st.metric(
                    "Moving Average",
                    f"{moving_average['forecast_rate']:.2f} / sec",
                    f"{moving_average['forecast_rate'] - latest_actual_rate:+.2f}"
                )

            with col3:

                st.metric(
                    "Weighted Average",
                    f"{weighted_average['forecast_rate']:.2f} / sec",
                    f"{weighted_average['forecast_rate'] - latest_actual_rate:+.2f}"
                )

            with col4:

                st.metric(
                    "Trend Forecast",
                    f"{trend_prediction['forecast_rate']:.2f} / sec",
                    f"{trend_prediction['forecast_rate'] - latest_actual_rate:+.2f}"
                )

        except (
            KeyError,
            TypeError,
            ValueError
        ):

            st.info(
                "Latest actual rate could not be evaluated."
            )

