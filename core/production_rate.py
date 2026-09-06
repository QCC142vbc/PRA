import csv
from datetime import datetime
from pathlib import Path


# =========================
# THEORETICAL PRODUCTION
# =========================

def calculate_production_rate(
    machine_count,
    cycle_time,
    output_per_cycle,
    measurement_time
):
    if machine_count <= 0:
        raise ValueError("machine_count must be greater than 0")

    if cycle_time <= 0:
        raise ValueError("cycle_time must be greater than 0")

    if output_per_cycle <= 0:
        raise ValueError("output_per_cycle must be greater than 0")

    if measurement_time <= 0:
        raise ValueError("measurement_time must be greater than 0")

    rate_per_second = (
        machine_count * output_per_cycle
    ) / cycle_time

    rate_per_minute = rate_per_second * 60
    rate_per_hour = rate_per_second * 3600
    total_output = rate_per_second * measurement_time

    return {
        "rate_per_second": rate_per_second,
        "rate_per_minute": rate_per_minute,
        "rate_per_hour": rate_per_hour,
        "total_output": total_output
    }


# =========================
# ACTUAL PRODUCTION
# =========================

def calculate_actual_production_rate(
    actual_output,
    measurement_time
):
    if actual_output < 0:
        raise ValueError("actual_output must be 0 or greater")

    if measurement_time <= 0:
        raise ValueError("measurement_time must be greater than 0")

    actual_rate_per_second = actual_output / measurement_time
    actual_rate_per_minute = actual_rate_per_second * 60
    actual_rate_per_hour = actual_rate_per_second * 3600

    return {
        "actual_rate_per_second": actual_rate_per_second,
        "actual_rate_per_minute": actual_rate_per_minute,
        "actual_rate_per_hour": actual_rate_per_hour,
        "actual_output": actual_output
    }


# =========================
# EFFICIENCY
# =========================

def calculate_efficiency(
    theoretical_rate,
    actual_rate
):
    if theoretical_rate <= 0:
        raise ValueError(
            "theoretical_rate must be greater than 0"
        )

    if actual_rate < 0:
        raise ValueError(
            "actual_rate must be 0 or greater"
        )

    efficiency = (
        actual_rate / theoretical_rate
    ) * 100

    efficiency = min(efficiency, 100.01)

    return {
        "efficiency_percent": efficiency
    }

# =========================
# SAVE MEASUREMENT
# =========================

def save_measurement(
    machine_count,
    cycle_time,
    output_per_cycle,
    measurement_time,
    actual_output,
    theoretical_rate,
    actual_rate,
    efficiency
):
    data_dir = (
        Path(__file__).resolve().parent.parent / "data"
    )

    data_dir.mkdir(exist_ok=True)

    file_path = data_dir / "measurements.csv"

    measurement = {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        "machine_count": machine_count,
        "cycle_time": cycle_time,
        "output_per_cycle": output_per_cycle,
        "measurement_time": measurement_time,
        "actual_output": actual_output,
        "theoretical_rate": theoretical_rate,
        "actual_rate": actual_rate,
        "efficiency": efficiency
    }

    fieldnames = [
        "timestamp",
        "machine_count",
        "cycle_time",
        "output_per_cycle",
        "measurement_time",
        "actual_output",
        "theoretical_rate",
        "actual_rate",
        "efficiency"
    ]

    file_exists = file_path.exists()
    file_empty = (
        not file_exists
        or file_path.stat().st_size == 0
    )

    with open(
        file_path,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        if file_empty:
            writer.writeheader()

        writer.writerow(measurement)

    return measurement


# =========================
# LOAD MEASUREMENTS
# =========================

def load_measurements():
    data_dir = (
        Path(__file__).resolve().parent.parent / "data"
    )

    file_path = data_dir / "measurements.csv"

    if not file_path.exists():
        return []

    with open(
        file_path,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        measurements = list(reader)

    return measurements

# =========================
# TREND ANALYSIS
# =========================

def calculate_trend(measurements):
    if not measurements:
        return {
            "trend": "no_data",
            "change_percent": 0
        }

    efficiencies = [
        float(measurement["efficiency"])
        for measurement in measurements
    ]

    actual_rates = [
        float(measurement["actual_rate"])
        for measurement in measurements
    ]

    if len(efficiencies) < 2:
        return {
            "trend": "insufficient_data",
            "change_percent": 0
        }

    first_efficiency = efficiencies[0]
    last_efficiency = efficiencies[-1]

    if first_efficiency == 0:
        efficiency_change = 0
    else:
        efficiency_change = (
            (last_efficiency - first_efficiency)
            / first_efficiency
        ) * 100

    if last_efficiency > first_efficiency:
        trend = "improving"
    elif last_efficiency < first_efficiency:
        trend = "declining"
    else:
        trend = "stable"

    return {
        "trend": trend,
        "change_percent": efficiency_change,
        "first_efficiency": first_efficiency,
        "last_efficiency": last_efficiency,
        "average_efficiency": (
            sum(efficiencies) / len(efficiencies)
        ),
        "best_efficiency": max(efficiencies),
        "worst_efficiency": min(efficiencies),
        "average_actual_rate": (
            sum(actual_rates) / len(actual_rates)
        )
    }

# =========================
# BOTTLENECK DETECTION
# =========================

def detect_bottleneck(efficiency):
    if efficiency >= 90:
        status = "normal"
    elif efficiency >= 75:
        status = "warning"
    else:
        status = "bottleneck"

    return {
        "status": status,
        "efficiency": efficiency
    }