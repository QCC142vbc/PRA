import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.production_rate import calculate_production_rate

st.set_page_config(
    page_title="Production Rate Analyzer",
    layout="centered"
)

st.title("Production Rate Analyzer")
st.write("Calculate theoretical production capacity.")

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

if st.button("Calculate", type="primary"):

    result = calculate_production_rate(
        machine_count=machine_count,
        cycle_time=cycle_time,
        output_per_cycle=output_per_cycle,
        measurement_time=measurement_time
    )

    st.subheader("Results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Production/sec",
            f"{result['rate_per_second']:.2f}"
        )

        st.metric(
            "Production / min",
            f"{result['rate_per_minute']:.2f}"
        )

    with col2:
        st.metric(
            "Production / hour",
            f"{result['rate_per_hour']:.2f}"
        )

        st.metric(
            "Total production",
            f"{result['total_output']:.2f}"
        )