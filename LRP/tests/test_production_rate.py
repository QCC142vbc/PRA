from core.production_rate import calculate_production_rate


result = calculate_production_rate(
    machine_count=11,
    cycle_time=0.583,
    output_per_cycle=1,
    measurement_time=160
)

print(result)