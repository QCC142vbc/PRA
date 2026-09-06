def calculate_efficiency(
        theoretical_rate, actual_rate
):
    if theoretical_rate <= 0:
        raise ValueError("Theoretical Rate must be greater than 0!")

    if actual_rate <= 0:
        raise ValueError("Actual Rate must be greater than 0!")

    efficiency = (actual_rate / theoretical_rate) * 100

    return {
        "efficiency_percent": efficiency
    }

def calculate_actual_production_rate(
        actual_output, measurement_time
):
    if actual_output <= 0:
        raise ValueError("Actual Output must be greater than 0!")
    if measurement_time <= 0:
        raise ValueError("Measurement Time must be greater than 0!")

    actual_rate_per_second = actual_output / measurement_time

    actual_rate_per_minute = actual_rate_per_second * 60
    actual_rate_per_hour = actual_rate_per_second * 3600

    return {
        "actual_rate_per_second": actual_rate_per_second,
        "actual_rate_per_minute": actual_rate_per_minute,
        "actual_rate_per_hour": actual_rate_per_hour,
        "actual_output": actual_output
    }






def calculate_production_rate(
    machine_count,
    cycle_time,
    output_per_cycle,
    measurement_time
):
    if machine_count <= 0:
        raise ValueError("Machine Count must be greater than 0!")

    if cycle_time <= 0:
        raise ValueError("Cycle Time must be greater than 0!")

    if output_per_cycle <= 0:
        raise ValueError("Output/Cycle must be greater than 0!")

    if measurement_time <= 0:
        raise ValueError("Measurement Time must be greater than 0!")


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