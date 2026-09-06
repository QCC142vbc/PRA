
import sys
from pathlib import Path

import pytest


# =========================
# PROJECT ROOT
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
    detect_bottleneck,
    calculate_trend,
    forecast_production_rate,
    calculate_analytics,
    moving_average_forecast,
    weighted_moving_average_forecast,
    trend_forecast,
    calculate_forecast_accuracy,
    calculate_forecast_reliability,
    evaluate_forecast_accuracy,
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


# =========================
# ADVANCED ANALYTICS
# =========================

def test_calculate_analytics():

    measurements = [
        {
            "efficiency": "80",
            "actual_rate": "10"
        },
        {
            "efficiency": "90",
            "actual_rate": "12"
        },
        {
            "efficiency": "85",
            "actual_rate": "11"
        }
    ]

    result = calculate_analytics(measurements)

    assert result["status"] == "ok"
    assert result["measurement_count"] == 3

    assert result["average_efficiency"] == pytest.approx(85)
    assert result["minimum_efficiency"] == 80
    assert result["maximum_efficiency"] == 90
    assert result["median_efficiency"] == 85

    assert result["average_actual_rate"] == pytest.approx(11)
    assert result["minimum_actual_rate"] == 10
    assert result["maximum_actual_rate"] == 12
    assert result["median_actual_rate"] == 11

    assert result["standard_deviation"] == pytest.approx(
        0.8164965809
    )

    assert result["coefficient_of_variation"] == pytest.approx(
        7.422695
    )


def test_calculate_analytics_no_data():

    result = calculate_analytics([])

    assert result["status"] == "no_data"


# =========================
# MOVING AVERAGE
# =========================

def test_moving_average_forecast():

    measurements = [
        {"actual_rate": "10"},
        {"actual_rate": "12"},
        {"actual_rate": "14"},
        {"actual_rate": "16"}
    ]

    result = moving_average_forecast(
        measurements,
        window=3
    )

    assert result["status"] == "ok"
    assert result["method"] == "moving_average"
    assert result["forecast_rate"] == pytest.approx(14)
    assert result["window"] == 3


# =========================
# WEIGHTED MOVING AVERAGE
# =========================

def test_weighted_moving_average_forecast():

    measurements = [
        {"actual_rate": "10"},
        {"actual_rate": "12"},
        {"actual_rate": "14"}
    ]

    result = weighted_moving_average_forecast(
        measurements,
        window=3
    )

    assert result["status"] == "ok"
    assert result["method"] == "weighted_moving_average"

    assert result["forecast_rate"] == pytest.approx(
        (10 * 1 + 12 * 2 + 14 * 3) / 6
    )


# =========================
# TREND FORECAST
# =========================

def test_trend_forecast():

    measurements = [
        {"actual_rate": "10"},
        {"actual_rate": "12"},
        {"actual_rate": "14"},
        {"actual_rate": "16"}
    ]

    result = trend_forecast(measurements)

    assert result["status"] == "ok"
    assert result["method"] == "trend"
    assert result["forecast_rate"] == pytest.approx(18)
    assert result["trend_slope"] == pytest.approx(2)


# =========================
# FORECAST ACCURACY
# =========================

def test_forecast_accuracy():

    result = calculate_forecast_accuracy(
        actual_rate=100,
        forecast_rate=90
    )

    assert result["status"] == "ok"
    assert result["accuracy_percent"] == pytest.approx(90)


# =========================
# FORECAST RELIABILITY
# =========================

def test_forecast_reliability():

    measurements = [
        {"actual_rate": "10"},
        {"actual_rate": "10"},
        {"actual_rate": "10"}
    ]

    result = calculate_forecast_reliability(
        measurements
    )

    assert result["status"] == "ok"
    assert result["reliability_percent"] == pytest.approx(100)


# =========================
# FORECAST NO DATA
# =========================

def test_forecast_no_data():

    assert (
        moving_average_forecast([])["status"]
        == "no_data"
    )

    assert (
        weighted_moving_average_forecast([])["status"]
        == "no_data"
    )

    assert (
        trend_forecast([])["status"]
        == "no_data"
    )

    assert (
        calculate_forecast_reliability([])["status"]
        == "no_data"
    )


# =========================
# FORECAST ACCURACY TRACKING
# =========================

def test_evaluate_forecast_accuracy():

    measurements = [
        {"actual_rate": "10"},
        {"actual_rate": "12"},
        {"actual_rate": "14"},
        {"actual_rate": "16"},
        {"actual_rate": "18"}
    ]

    result = evaluate_forecast_accuracy(
        measurements,
        method="moving_average",
        window=3
    )

    assert result["status"] == "ok"
    assert result["method"] == "moving_average"
    assert result["window"] == 3
    assert result["evaluation_count"] == 2
    assert result["accuracy_percent"] > 0


def test_evaluate_weighted_forecast_accuracy():

    measurements = [
        {"actual_rate": "10"},
        {"actual_rate": "12"},
        {"actual_rate": "14"},
        {"actual_rate": "16"},
        {"actual_rate": "18"}
    ]

    result = evaluate_forecast_accuracy(
        measurements,
        method="weighted_moving_average",
        window=3
    )

    assert result["status"] == "ok"
    assert result["method"] == "weighted_moving_average"
    assert result["evaluation_count"] == 2


def test_evaluate_trend_forecast_accuracy():

    measurements = [
        {"actual_rate": "10"},
        {"actual_rate": "12"},
        {"actual_rate": "14"},
        {"actual_rate": "16"},
        {"actual_rate": "18"}
    ]

    result = evaluate_forecast_accuracy(
        measurements,
        method="trend"
    )

    assert result["status"] == "ok"
    assert result["method"] == "trend"
    assert result["evaluation_count"] == 2


def test_evaluate_forecast_accuracy_insufficient_data():

    measurements = [
        {"actual_rate": "10"},
        {"actual_rate": "12"}
    ]

    result = evaluate_forecast_accuracy(
        measurements,
        method="moving_average",
        window=3
    )

    assert result["status"] == "insufficient_data"
