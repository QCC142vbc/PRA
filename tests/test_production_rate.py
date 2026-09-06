import pytest

from core.production_rate import (
    calculate_production_rate,
    calculate_actual_production_rate,
    calculate_efficiency,
    detect_bottleneck,
    calculate_trend,
    forecast_production_rate,
)


# =========================
# THEORETICAL PRODUCTION
# =========================

def test_calculate_production_rate():

    result = calculate_production_rate(
        machine_count=11,
        cycle_time=0.583,
        output_per_cycle=1,
        measurement_time=160
    )

    assert result["rate_per_second"] > 0
    assert result["rate_per_minute"] > 0
    assert result["rate_per_hour"] > 0
    assert result["total_output"] > 0

    assert result["rate_per_second"] == pytest.approx(
        18.8679245283
    )


# =========================
# ACTUAL PRODUCTION
# =========================

def test_calculate_actual_production_rate():

    result = calculate_actual_production_rate(
        actual_output=2750,
        measurement_time=160
    )

    assert result["actual_rate_per_second"] == pytest.approx(
        17.1875
    )

    assert result["actual_rate_per_minute"] == pytest.approx(
        1031.25
    )

    assert result["actual_rate_per_hour"] == pytest.approx(
        61875
    )

    assert result["actual_output"] == 2750


# =========================
# EFFICIENCY
# =========================

def test_calculate_efficiency():

    result = calculate_efficiency(
        theoretical_rate=18.8679245283,
        actual_rate=17.1875
    )

    assert result["efficiency_percent"] == pytest.approx(
        91.09375
    )


# =========================
# BOTTLENECK
# =========================

def test_bottleneck_normal():

    result = detect_bottleneck(95)

    assert result["status"] == "normal"
    assert result["efficiency"] == 95


def test_bottleneck_warning():

    result = detect_bottleneck(80)

    assert result["status"] == "warning"
    assert result["efficiency"] == 80


def test_bottleneck_detected():

    result = detect_bottleneck(60)

    assert result["status"] == "bottleneck"
    assert result["efficiency"] == 60


# =========================
# TREND
# =========================

def test_trend_improving():

    measurements = [
        {
            "efficiency": "70",
            "actual_rate": "10"
        },
        {
            "efficiency": "80",
            "actual_rate": "12"
        },
        {
            "efficiency": "90",
            "actual_rate": "15"
        }
    ]

    result = calculate_trend(measurements)

    assert result["trend"] == "improving"
    assert result["first_efficiency"] == 70
    assert result["last_efficiency"] == 90
    assert result["average_efficiency"] == pytest.approx(80)
    assert result["average_actual_rate"] == pytest.approx(
        12.3333333333
    )


def test_trend_declining():

    measurements = [
        {
            "efficiency": "90",
            "actual_rate": "15"
        },
        {
            "efficiency": "80",
            "actual_rate": "12"
        },
        {
            "efficiency": "70",
            "actual_rate": "10"
        }
    ]

    result = calculate_trend(measurements)

    assert result["trend"] == "declining"


def test_trend_stable():

    measurements = [
        {
            "efficiency": "85",
            "actual_rate": "12"
        },
        {
            "efficiency": "85",
            "actual_rate": "12"
        }
    ]

    result = calculate_trend(measurements)

    assert result["trend"] == "stable"


def test_trend_no_data():

    result = calculate_trend([])

    assert result["trend"] == "no_data"
    assert result["change_percent"] == 0


def test_trend_insufficient_data():

    measurements = [
        {
            "efficiency": "85",
            "actual_rate": "12"
        }
    ]

    result = calculate_trend(measurements)

    assert result["trend"] == "insufficient_data"


# =========================
# FORECAST
# =========================

def test_forecast_production_rate():

    measurements = [
        {
            "actual_rate": "10"
        },
        {
            "actual_rate": "12"
        },
        {
            "actual_rate": "14"
        }
    ]

    result = forecast_production_rate(
        measurements
    )

    assert result["status"] == "ok"

    assert result["forecast_rate"] == pytest.approx(
        12
    )

    assert result["measurement_count"] == 3


def test_forecast_no_data():

    result = forecast_production_rate([])

    assert result["status"] == "no_data"
    assert result["forecast_rate"] == 0


# =========================
# VALIDATION
# =========================

def test_invalid_machine_count():

    with pytest.raises(ValueError):

        calculate_production_rate(
            machine_count=0,
            cycle_time=0.583,
            output_per_cycle=1,
            measurement_time=160
        )


def test_invalid_cycle_time():

    with pytest.raises(ValueError):

        calculate_production_rate(
            machine_count=11,
            cycle_time=0,
            output_per_cycle=1,
            measurement_time=160
        )


def test_invalid_output_per_cycle():

    with pytest.raises(ValueError):

        calculate_production_rate(
            machine_count=11,
            cycle_time=0.583,
            output_per_cycle=0,
            measurement_time=160
        )


def test_invalid_measurement_time():

    with pytest.raises(ValueError):

        calculate_actual_production_rate(
            actual_output=2750,
            measurement_time=0
        )


def test_negative_actual_output():

    with pytest.raises(ValueError):

        calculate_actual_production_rate(
            actual_output=-1,
            measurement_time=160
        )


def test_invalid_theoretical_rate():

    with pytest.raises(ValueError):

        calculate_efficiency(
            theoretical_rate=0,
            actual_rate=10
        )