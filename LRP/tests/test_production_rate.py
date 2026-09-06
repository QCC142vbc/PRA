from core.production_rate import (
    calculate_production_rate,
    calculate_actual_production_rate,
    calculate_efficiency
)


# THEORETICAL PRODUCTION
result = calculate_production_rate(
    machine_count=11,
    cycle_time=0.583,
    output_per_cycle=1,
    measurement_time=160
)

print("THEORETICAL:")
print(result)


# ACTUAL PRODUCTION
actual_result = calculate_actual_production_rate(
    actual_output=2750,
    measurement_time=160
)

print("\nACTUAL:")
print(actual_result)


# EFFICIENCY
efficiency_result = calculate_efficiency(
    theoretical_rate=result["rate_per_second"],
    actual_rate=actual_result["actual_rate_per_second"]
)

print("\nEFFICIENCY:")
print(efficiency_result)