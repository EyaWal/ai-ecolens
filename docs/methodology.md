# Measurement methodology (draft)

## Candidate metrics
- `energy_wh_per_request`: measured Wh/request under a documented protocol.
- `energy_wh_per_1k_requests`: 1000 × Wh/request.
- `estimated_carbon_gco2e`: (energy_wh / 1000) × grid intensity (gCO2e/kWh).
- `estimated_monthly_energy_kwh`: request_count × energy_wh_per_request / 1000.
- `estimated_monthly_carbon_kgco2e`: monthly_energy_kwh × grid_intensity_gco2e_per_kwh / 1000.

## Caveats
These formulas do not automatically account for data center PUE, CPU/network power, embodied emissions or model training. Clearly label system boundaries and assumptions. Energy per request should only be scaled to other workloads when supported by the measurement protocol.
