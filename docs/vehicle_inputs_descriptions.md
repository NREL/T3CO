# Vehicle Input Descriptions

| vehicle parameter                    | description                                                                                                                                       | data type      |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| scenario_name                        | Vehicle name                                                                                                                                      |  string        |
| selection                            | Vehicle database ID                                                                                                                               |  int           |
| veh_year                             | Vehicle year                                                                                                                                      |  int           |
| veh_pt_type                          | Vehicle powertrain type, one of [CONV, HEV, PHEV, BEV]                                                                                            |  string        |
| drag_coef                            | Aerodynamic drag coefficient                                                                                                                      |  float         |
| frontal_area_m2                      | Frontal area, $m^2$                                                                                                                               |  float         |
| glider_kg                            | Vehicle mass excluding cargo, passengers, and powertrain components, $kg$                                                                         |  float         |
| veh_cg_m                             | Vehicle center of mass height, $m$ NOTE: positive for FWD, negative for RWD, AWD, 4WD                                                             |  float         |
| drive_axle_weight_frac               | Fraction of weight on the drive axle while stopped                                                                                                |  float         |
| wheel_base_m                         | Wheelbase, $m$                                                                                                                                    |  float         |
| cargo_kg                             | Cargo mass including passengers, $kg$                                                                                                             |  float         |
| veh_override_kg                      | Total vehicle mass, overrides mass calculation, $kg$                                                                                              |  Option<float> |
| comp_mass_multiplier                 | Component mass multiplier for vehicle mass calculation                                                                                            |  float         |
| fs_max_kw                            | Fuel storage max power output, $kW$                                                                                                               |  float         |
| fs_secs_to_peak_pwr                  | Fuel storage time to peak power, $s$                                                                                                              |  float         |
| fs_kwh                               | Fuel storage energy capacity, $kWh$                                                                                                               |  float         |
| fs_kwh_per_kg                        | Fuel specific energy, $\frac{kWh}{kg}$                                                                                                            |  float         |
| fc_max_kw                            | Fuel converter peak continuous power, $kW$                                                                                                        |  float         |
| fc_pwr_out_perc                      | Fuel converter output power percentage map, x values of fc_eff_map                                                                                |  Array1<float> |
| fc_eff_map                           | Fuel converter efficiency map                                                                                                                     |  Array1<float> |
| fc_eff_type                          | Fuel converter efficiency type, one of [SI, ATKINSON, DIESEL, H2FC, HD_DIESEL] Used for calculating fc_eff_map, and other calculations if H2FC    |  string        |
| fc_sec_to_peak_pwr                   | Fuel converter time to peak power, $s$                                                                                                            |  float         |
| fc_base_kg                           | Fuel converter base mass, $kg$                                                                                                                    |  float         |
| fc_kw_per_kg                         | Fuel converter specific power (power-to-weight ratio), $\frac{kW}{kg}$                                                                            |  float         |
| min_fc_time_on                       | Minimum time fuel converter must be on before shutoff (for HEV, PHEV)                                                                             |  float         |
| idle_fc_kw                           | Fuel converter idle power, $kW$                                                                                                                   |  float         |
| mc_max_kw                            | Peak continuous electric motor power, $kW$                                                                                                        |  float         |
| mc_pwr_out_perc                      | Electric motor output power percentage map, x values of mc_eff_map                                                                                |  Array1<float> |
| mc_eff_map                           | Electric motor efficiency map                                                                                                                     |  Array1<float> |
| mc_sec_to_peak_pwr                   | Electric motor time to peak power, $s$                                                                                                            |  float         |
| mc_pe_kg_per_kw                      | Motor power electronics mass per power output, $\frac{kg}{kW}$                                                                                    |  float         |
| mc_pe_base_kg                        | Motor power electronics base mass, $kg$                                                                                                           |  float         |
| ess_max_kw                           | Traction battery maximum power output, $kW$                                                                                                       |  float         |
| ess_max_kwh                          | Traction battery energy capacity, $kWh$                                                                                                           |  float         |
| ess_kg_per_kwh                       | Traction battery mass per energy, $\frac{kg}{kWh}$                                                                                                |  float         |
| ess_base_kg                          | Traction battery base mass, $kg$                                                                                                                  |  float         |
| ess_round_trip_eff                   | Traction battery round-trip efficiency                                                                                                            |  float         |
| ess_life_coef_a                      | Traction battery cycle life coefficient A, see reference                                                                                          |  float         |
| ess_life_coef_b                      | Traction battery cycle life coefficient B, see reference                                                                                          |  float         |
| min_soc                              | Traction battery minimum state of charge                                                                                                          |  float         |
| max_soc                              | Traction battery maximum state of charge                                                                                                          |  float         |
| ess_dischg_to_fc_max_eff_perc        | ESS discharge effort toward max FC efficiency                                                                                                     |  float         |
| ess_chg_to_fc_max_eff_perc           | ESS charge effort toward max FC efficiency                                                                                                        |  float         |
| wheel_inertia_kg_m2                  | Mass moment of inertia per wheel, $kg \cdot m^2$                                                                                                  |  float         |
| num_wheels                           | Number of wheels                                                                                                                                  |  float         |
| wheel_rr_coef                        | Rolling resistance coefficient                                                                                                                    |  float         |
| wheel_radius_m                       | Wheel radius, $m$                                                                                                                                 |  float         |
| wheel_coef_of_fric                   | Wheel coefficient of friction                                                                                                                     |  float         |
| max_accel_buffer_mph                 | Speed where the battery reserved for accelerating is zero                                                                                         |  float         |
| max_accel_buffer_perc_of_useable_soc | Percent of usable battery energy reserved to help accelerate                                                                                      |  float         |
| perc_high_acc_buf                    | Percent SOC buffer for high accessory loads during cycles with long idle time                                                                     |  float         |
| mph_fc_on                            | Speed at which the fuel converter must turn on, $mph$                                                                                             |  float         |
| kw_demand_fc_on                      | Power demand above which to require fuel converter on, $kW$                                                                                       |  float         |
| max_regen                            | Maximum brake regeneration efficiency                                                                                                             |  float         |
| stop_start                           | Stop/start micro-HEV flag                                                                                                                         |  bool          |
| force_aux_on_fc                      | Force auxiliary power load to come from fuel converter                                                                                            |  bool          |
| alt_eff                              | Alternator efficiency                                                                                                                             |  float         |
| chg_eff                              | Charger efficiency                                                                                                                                |  float         |
| aux_kw                               | Auxiliary load power, $kW$                                                                                                                        |  float         |
| trans_kg                             | Transmission mass, $kg$                                                                                                                           |  float         |
| trans_eff                            | Transmission efficiency                                                                                                                           |  float         |
| ess_to_fuel_ok_error                 | Maximum acceptable ratio of change in ESS energy to expended fuel energy (used in hybrid SOC balancing), $\frac{\Delta E_{ESS}}{\Delta E_{fuel}}$ |  float         |
| fc_peak_eff_override                 | Fuel converter efficiency peak override, scales entire curve                                                                                      |  Option<float> |
| mc_peak_eff_override                 | Motor efficiency peak override, scales entire curve                                                                                               |  Option<float> |