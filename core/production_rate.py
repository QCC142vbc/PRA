import csv
from datetime import datetime
from pathlib import Path


# =========================
# CONFIGURATION
# =========================

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MEASUREMENTS_FILE = DATA_DIR / "measurements.csv"

FIELDNAMES = [
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


# =========================
# VALIDATION
# =========================

def _validate_number(value, name, minimum=None, strict=False):
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a number")

    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a number")

    if minimum is not None:
        if strict and value <= minimum:
            raise ValueError(
                f"{name} must be greater than {minimum}"
            )

        if not strict and value < minimum:
            raise ValueError(
                f"{name} must be {minimum} or greater"
            )

    return value


# =========================
# THEORETICAL PRODUCTION
# =========================

def calculate_production_rate(
    machine_count,
    cycle_time,
    output_per_cycle,
    measurement_time
):
    machine_count = _validate_number(
        machine_count,
        "machine_count",
        0,
        strict=True
    )

    cycle_time = _validate_number(
        cycle_time,
        "cycle_time",
        0,
        strict=True
    )

    output_per_cycle = _validate_number(
        output_per_cycle,
        "output_per_cycle",
        0,
        strict=True
    )

    measurement_time = _validate_number(
        measurement_time,
        "measurement_time",
        0,
        strict=True
    )

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
    actual_output = _validate_number(
        actual_output,
        "actual_output",
        0
    )

    measurement_time = _validate_number(
        measurement_time,
        "measurement_time",
        0,
        strict=True
    )

    actual_rate_per_second = (
        actual_output / measurement_time
    )

    actual_rate_per_minute = (
        actual_rate_per_second * 60
    )

    actual_rate_per_hour = (
        actual_rate_per_second * 3600
    )

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
    theoretical_rate = _validate_number(
        theoretical_rate,
        "theoretical_rate",
        0,
        strict=True
    )

    actual_rate = _validate_number(
        actual_rate,
        "actual_rate",
        0
    )

    efficiency = (
        actual_rate / theoretical_rate
    ) * 100

    # Small protection against floating-point overflow.
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
    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

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

    file_empty = (
        not MEASUREMENTS_FILE.exists()
        or MEASUREMENTS_FILE.stat().st_size == 0
    )

    with open(
        MEASUREMENTS_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        if file_empty:
            writer.writeheader()

        writer.writerow(measurement)

    return measurement


# =========================
# LOAD MEASUREMENTS
# =========================

def load_measurements():
    if not MEASUREMENTS_FILE.exists():
        return []

    measurements = []

    try:
        with open(
            MEASUREMENTS_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if not row:
                    continue

                if not row.get("timestamp"):
                    continue

                required_fields = [
                    "machine_count",
                    "cycle_time",
                    "output_per_cycle",
                    "measurement_time",
                    "actual_output",
                    "theoretical_rate",
                    "actual_rate",
                    "efficiency"
                ]

                if any(
                    not row.get(field)
                    for field in required_fields
                ):
                    continue

                try:
                    for field in required_fields:
                        float(row[field])

                    measurements.append(row)

                except (TypeError, ValueError):
                    continue

    except (
        OSError,
        csv.Error,
        UnicodeDecodeError
    ):
        return []

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

    efficiencies = []
    actual_rates = []

    for measurement in measurements:
        try:
            efficiency = float(
                measurement["efficiency"]
            )

            actual_rate = float(
                measurement["actual_rate"]
            )

            efficiencies.append(efficiency)
            actual_rates.append(actual_rate)

        except (
            KeyError,
            TypeError,
            ValueError
        ):
            continue

    if not efficiencies:
        return {
            "trend": "no_data",
            "change_percent": 0
        }

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
            sum(efficiencies)
            / len(efficiencies)
        ),
        "best_efficiency": max(efficiencies),
        "worst_efficiency": min(efficiencies),
        "average_actual_rate": (
            sum(actual_rates)
            / len(actual_rates)
        )
    }


# =========================
# BOTTLENECK DETECTION
# =========================

def detect_bottleneck(efficiency):
    efficiency = _validate_number(
        efficiency,
        "efficiency"
    )

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


# =========================
# PRODUCTION FORECAST
# =========================

def forecast_production_rate(measurements):

    if not measurements:
        return {
            "forecast_rate": 0,
            "status": "no_data"
        }

    actual_rates = []

    for measurement in measurements:
        try:
            actual_rate = float(
                measurement["actual_rate"]
            )

            actual_rates.append(actual_rate)

        except (
            KeyError,
            TypeError,
            ValueError
        ):
            continue

    if not actual_rates:
        return {
            "forecast_rate": 0,
            "status": "no_data"
        }

    forecast_rate = (
        sum(actual_rates)
        / len(actual_rates)
    )

    return {
        "forecast_rate": forecast_rate,
        "status": "ok",
        "measurement_count": len(actual_rates)
    }

# =========================
# ADVANCED ANALYTICS
# =========================

def calculate_analytics(measurements):
    if not measurements:
        return {
            "status": "no_data"
        }

    efficiencies = []
    actual_rates = []

    for measurement in measurements:
        try:
            efficiency = float(measurement["efficiency"])
            actual_rate = float(measurement["actual_rate"])

            efficiencies.append(efficiency)
            actual_rates.append(actual_rate)

        except (
            KeyError,
            TypeError,
            ValueError
        ):
            continue

    if not efficiencies or not actual_rates:
        return {
            "status": "no_data"
        }

    sorted_efficiencies = sorted(efficiencies)
    sorted_rates = sorted(actual_rates)

    def median(values):
        count = len(values)
        middle = count // 2

        if count % 2 == 0:
            return (
                values[middle - 1]
                + values[middle]
            ) / 2

        return values[middle]

    average_efficiency = (
        sum(efficiencies)
        / len(efficiencies)
    )

    average_rate = (
        sum(actual_rates)
        / len(actual_rates)
    )

    variance = sum(
        (rate - average_rate) ** 2
        for rate in actual_rates
    ) / len(actual_rates)

    standard_deviation = variance ** 0.5

    if average_rate == 0:
        coefficient_of_variation = 0
    else:
        coefficient_of_variation = (
            standard_deviation
            / average_rate
        ) * 100

    return {
        "status": "ok",
        "measurement_count": len(efficiencies),

        "average_efficiency": average_efficiency,
        "minimum_efficiency": min(efficiencies),
        "maximum_efficiency": max(efficiencies),
        "median_efficiency": median(
            sorted_efficiencies
        ),

        "average_actual_rate": average_rate,
        "minimum_actual_rate": min(actual_rates),
        "maximum_actual_rate": max(actual_rates),
        "median_actual_rate": median(
            sorted_rates
        ),

        "standard_deviation": standard_deviation,
        "coefficient_of_variation": (
            coefficient_of_variation
        )
    }