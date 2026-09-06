import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.production_rate import (
    calculate_production_rate,
    calculate_actual_production_rate,
    calculate_efficiency,
    save_measurement
)


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Production Rate Analyzer",
    layout="centered"
)

st.title("Production Rate Analyzer")
st.write("Compare theoretical and actual production performance.")


# =========================
# INPUT
# =========================

st.subheader("Production Setup")

machine_count = st.number_input(
    "Machine count",
    min_value=1,
    value=11,
    step=1
)

cycle_time = st.number_input(
    "Cycle time (sec)",
    min_value=0.001,
    value=0.583,
    step=0.001
)

output_per_cycle = st.number_input(
    "Output per cycle",
    min_value=0.001,
    value=1.0,
    step=0.1
)

measurement_time = st.number_input(
    "Measurement time (sec)",
    min_value=0.001,
    value=160.0,
    step=1.0
)

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

    # Store results in session state
    st.session_state["theoretical"] = theoretical
    st.session_state["actual"] = actual
    st.session_state["efficiency"] = efficiency


# =========================
# RESULTS
# =========================

if "theoretical" in st.session_state:

    theoretical = st.session_state["theoretical"]
    actual = st.session_state["actual"]
    efficiency = st.session_state["efficiency"]

    st.subheader("Production Performance")

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

    st.divider()

    # =========================
    # DETAILED RESULTS
    # =========================

    st.subheader("Detailed Results")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Theoretical Production")

        st.write(
            f"Per second: {theoretical['rate_per_second']:.2f}"
        )

        st.write(
            f"Per minute: {theoretical['rate_per_minute']:.2f}"
        )

        st.write(
            f"Per hour: {theoretical['rate_per_hour']:.2f}"
        )

        st.write(
            f"Measurement output: {theoretical['total_output']:.2f}"
        )

    with col2:
        st.write("Actual Production")

        st.write(
            f"Per second: {actual['actual_rate_per_second']:.2f}"
        )

        st.write(
            f"Per minute: {actual['actual_rate_per_minute']:.2f}"
        )

        st.write(
            f"Per hour: {actual['actual_rate_per_hour']:.2f}"
        )

        st.write(
            f"Actual output: {actual['actual_output']:.2f}"
        )

    st.divider()

    # =========================
    # SAVE MEASUREMENT
    # =========================

    st.subheader("Measurement")

    if st.button("Save Measurement"):

        saved_measurement = save_measurement(
            machine_count=machine_count,
            cycle_time=cycle_time,
            output_per_cycle=output_per_cycle,
            measurement_time=measurement_time,
            actual_output=actual_output,
            theoretical_rate=theoretical["rate_per_second"],
            actual_rate=actual["actual_rate_per_second"],
            efficiency=efficiency["efficiency_percent"]
        )

        st.success("Measurement saved successfully.")

        st.json(saved_measurement)