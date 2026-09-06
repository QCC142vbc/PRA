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