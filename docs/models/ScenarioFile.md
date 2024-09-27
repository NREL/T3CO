# T3CO Scenario File

Below is an example of a scenario file contents, in columnar format for readability. Usually the input CSV is in row form. **Scenario** selections become a `selection` [object](https://github.com/NREL/T3CO/blob/9c0b19327fb60672185f087bea195a059e919cf2/t3co/run_scenario.py#L113) in **T3CO**. **Scenario** files are one of two fundamental units of **T3CO**. The other is the **FASTSim** `Vehicle`. To put it in plain English, if **FASTSim** `Vehicles` are the peanut butter, `Scenarios` are the jelly. These two objects literally flow through the code in a pair, in tandem. Most methods in **T3CO** have arguments for a `Vehicle` object and its accompanying `Scenario` object. If using row-based sources for vehicles and scenarios, the `selection` value in the scenario file should correspond with the `selection` value in the FASTSim input file. The `Vehicle` of selection should correspond with `Scenario` of selection 21 and they should flow through the code together. This is how we pair a vehicle with operating and economic conditions from the scenario to create total cost of ownership and performance results; as well as optimization targets and constraints.

|column name| description |example value| type/bounds |
|---|---|----|----|
|`selection`|<  >| `110`| NA |
|`scenario_name`|<  >| `Class 8 Sleeper cab mid roof (PHEV, 2050, no program)`| NA |
|`drive_cycle`|<  >| `[("EPA_Ph2_rural_interstate_65mph.csv", .86), ("EPA_Ph2_urban_highway_55mph.csv", .09), ("EPA_Ph2_transient.csv", .05)]`| Strings are drive cycle names or full paths to drive cycle. If using only one drive cycle,can be a single string. If using a composite set of cycles, must be a list of tuples. First tuple element is drive cycle string, second element is a float between 0 and 1:`string or [(string,float),...]` |
|`vmt_reduct_per_yr`| < > |`nan`| `[0, inf]` |
|`vmt`| < > |`[108010,117983,114998,104732]`| Should have a vmt entry in the list for every year the vehicle is operational based on `vehicle_life_yr`: `[int,...]` |
|`constant_trip_distance_mi`| < > |`0`| `int` |
|`vehicle_life_yr`| < > |`4`| `int` |
|`discount_rate_pct_per_yr`| < > |`0.03`| `float [0,1]` |
|`ess_cost_dol_per_kw`| < > |`0`| `float` |
|`ess_cost_dol_per_kwh`| < > |`85`| `float`|
|`ess_base_cost_dol`| < > |`0`| `float`|
|`ess_cost_reduction_dol_per_yr`| < > |`0`| `float`|
|`ess_salvage_value_dol`| < > |`0`| `float`|
|`pe_mc_cost_dol_per_kw`| < > |`11`| `float`|
|`pe_mc_base_cost_dol`| < > |`350`| `float`|
|`fc_ice_cost_dol_per_kw`| < > |`50`| `float`|
|`fc_ice_base_cost_dol`| < > |`6250`| `float`|
|`fc_fuelcell_cost_dol_per_kw`| < > |`85`| `float`|
|`fs_cost_dol_per_kwh`| < > |`0.07`| `float`|
|`fs_h2_cost_dol_per_kwh`| < > |`9.5`| `float`|
|`plug_base_cost_dol`| < > |`500`| `float`|
|`markup_pct`| < > |`1.2`| `float`|
|`tax_rate_pct`| < > |`0.035`| `float`|
|`fc_cng_ice_cost_dol_per_kw`| < > |`55`|`float` |
|`fs_cng_cost_dol_per_kwh`| < > |`7.467735503`|`float` |
|`vehicle_glider_cost_dol`| < > |`112759`| `float`|
|`segment_name`| < > |`HDTC8`| `string`|
|`gvwr_kg`| < > |`36287.43275`| `float`|
|`gvwr_credit_kg`| < > |`0`| amount [kg] vehicle can exceed GVWR[kg], applies during component sizing during optimization `int`|
|`fuel`| < > |`["cd_electricity", "cd_diesel", "cs_diesel"]`| multiple fuel types are permissible, or a single type can be input. For PHEVs, there *must* be specified two Charge Depleting and on Charge Sustaining as shown`string or [string,...]` |
|`maint_oper_cost_dol_per_mi`|< > |`[0.15,0.16,...0.19]`| `float list`|
|`vocation`|< > |`Long haul`| `string`|
|`model_year`|< > |`2050`| `int` |
|`region`|< > |`FY21NoProgram`| `string`|
|`target_range_mi`|< > |`500`|`float` Note: for PHEVs, T3CO will meet this requirement in CD mode |
|`min_speed_at_6pct_grade_in_5min_mph`|< > |`30`|`float` |
|`min_speed_at_1p25pct_grade_in_5min_mph`|< > |`65`|`float` |
|`max_time_0_to_60mph_at_gvwr_s`|< > |`80`|`float` |
|`max_time_0_to_30mph_at_gvwr_s`|< > |`20`|`float` |
|`lw_imp_curve_sel`|< > |`MDHD_noprogram_2050`| `string` Optimization "knob" handling. For certain knobs, there are curves that apply. This value references a column in the light-weighting curves file. Example: [light weighting curves](https://github.com/NREL/T3CO/blob/master/run_scripts/external_resources/tda_example/matlltwt_imp_cost_curves_for_tda_in_t3co.csv). Referenced in `sweep.py` [here](https://github.com/NREL/T3CO/blob/934dc4718c8a3aeef296bdf39abd6952d65c88f6/run_scripts/sweep.py#L537) |
|`eng_eff_imp_curve_sel`| < > |`MDHD_large_noprogram_2050`| `string` Optimization "knob" handling. For certain knobs, there are curves that apply. This value references a column in the engine efficiency improvement curves file. Example: [engine efficiency curves](https://github.com/NREL/T3CO/blob/master/run_scripts/external_resources/tda_example/eng_imp_cost_curves_for_tda_in_t3co.csv). Referenced in `sweep.py` [here](https://github.com/NREL/T3CO/blob/934dc4718c8a3aeef296bdf39abd6952d65c88f6/run_scripts/sweep.py#L537) |
|`aero_drag_imp_curve_sel`| < > |`SleeperTractorMidRoof_noprogram_2050`|  `string` Optimization "knob" handling. For certain knobs, there are curves that apply. This value references a column in the drag coefficient improvement curves file. Example: [drag coefficient curves](https://github.com/NREL/T3CO/blob/master/run_scripts/external_resources/tda_example/aero_imp_cost_curves_for_tda_in_t3co.csv). Referenced in `sweep.py` [here](https://github.com/NREL/T3CO/blob/934dc4718c8a3aeef296bdf39abd6952d65c88f6/run_scripts/sweep.py#L537) |
|`skip_opt`| < > |`True`| Important column! Though it's a bit buried, this column will designate whether this scenario and vehicle combination should be optimized or not. If `True`, then optimization is skipped.`True or False`|
|`knob_min_ess_kwh`| < > | `300`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_max_ess_kwh`| < > | `1500`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_min_motor_kw`| < > | `200`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_max_motor_kw`| < > | `400`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_min_fc_kw`| < > | `100`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_max_fc_kw`| < > | `300`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_min_fs_kwh`| < > | `100`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_max_fs_kwh`| < > | `600`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`constraint_range`| < > | `nan`| `True or False` Optimization setting. If True, then the constraint is applied and tests for range must be met or exceeded. Test threshold designated by value in `target_range_mi`|
|`constraint_accel`| < > |`nan`| `True or False` Optimization setting. If True, then the constraint is applied and tests for acceleratiion. must be met or exceeded Test threshold designated by value in `max_time_0_to_60mph_at_gvwr_s and max_time_0_to_30mph_at_gvwr_s`|
|`constraint_grade`| < > |`nan`| `True or False` Optimization setting. If True, then the constraint is applied and tests for grade must be met or exceeded Test threshold designated by value in `min_speed_at_6pct_grade_in_5min_mph and min_speed_at_1p25pct_grade_in_5min_mph`|
|`objective_tco`|  < > | `nan`| `True or False` Optimization setting. If True, then the objective to minimize Total Cost of Ownership is applied. |
|`constraint_c_rate`|  < > | `True`| `True or False` Optimization setting. If True, then the constraint for c rate is applied|
|`shifts_per_year`|  < > | `260`| PHEVs only! See [PHEV Docs](./PHEVs.md#phev-special-inputs)|
|`phev_utility_factor_override`|  < > | `.6`| PHEVs only! See [PHEV Docs](./PHEVs.md#phev-special-inputs)|
|`soc_norm_init_for_grade_pct`|  < > | `.8`| PHEVs only! See [PHEV Docs](./PHEVs.md#phev-special-inputs)|
|`soc_norm_init_for_accel_pct`|  < > | `.85`| PHEVs only! See [PHEV Docs](./PHEVs.md#phev-special-inputs)|
|`motor_power_override_kw_fc_demand_on_pct`|  < > | `.95`| PHEV specific inputs. See [PHEV Docs](./PHEVs.md#phev-special-inputs)|
|`ess_init_soc_grade`|  < > | `.8`|`[0,1]` For BEV or HEV, during grade test, if initial SOC override is desired, rather than using the [FASTSim + T3CO intial SOC regime](acceleration_and_grade_tests.md#default-socs)|
|`ess_init_soc_accel`| < > |`.85`|`[0,1]`  For BEV or HEV, during grade test, if initial SOC override is desired, rather than using the [FASTSim + T3CO intial SOC regime](acceleration_and_grade_tests.md#default-socs)|
