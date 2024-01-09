# T3CO Scenario File

Below is an example of a scenario file contents, in columnar format for readability. Usually the input CSV is in row form. **Scenario** selections become a `selection` [object](https://github.com/NREL/T3CO-private/blob/9c0b19327fb60672185f087bea195a059e919cf2/t3co/run_scenario.py#L113) in **T3CO**. **Scenario** files are one of two fundamental units of **T3CO**. The other is the **FASTSim** `Vehicle`. To put it in plain English, if **FASTSim** `Vehicles` are the peanut butter, `Scenarios` are the jelly. These two objects literally flow through the code in a pair, in tandem. Most methods in **T3CO** have arguments for a `Vehicle` object and its accompanying `Scenario` object. If using row-based sources for vehicles and scenarios, the `selection` value in the scenario file should correspond with the `selection` value in the FASTSim input file. The `Vehicle` of selection should correspond with `Scenario` of selection 21 and they should flow through the code together. This is how we pair a vehicle with operating and economic conditions from the scenario to create total cost of ownership and performance results; as well as optimization targets and constraints.

|column name| description |example value| type/bounds |
|---|---|----|----|
|`selection`|<  >| `110`| NA |
|`scenario_name`|<  >| `Class 8 Sleeper cab mid roof (PHEV, 2050, no program)`| NA |
|`driveCycle`|<  >| `[("EPA_Ph2_rural_interstate_65mph.csv", .86), ("EPA_Ph2_urban_highway_55mph.csv", .09), ("EPA_Ph2_transient.csv", .05)]`| Strings are drive cycle names or full paths to drive cycle. If using only one drive cycle,can be a single string. If using a composite set of cycles, must be a list of tuples. First tuple element is drive cycle string, second element is a float between 0 and 1:`string or [(string,float),...]` |
|`vmtReductPerYear`| < > |`nan`| `[0, inf]` |
|`VMT`| < > |`[108010,117983,114998,104732]`| Should have a VMT entry in the list for every year the vehicle is operational based on `vehLifeYears`: `[int,...]` |
|`constTripDistMiles`| < > |`0`| `int` |
|`vehLifeYears`| < > |`4`| `int` |
|`discRate`| < > |`0.03`| `float [0,1]` |
|`essDolPerKw`| < > |`0`| `float` |
|`essDolPerKwh`| < > |`85`| `float`|
|`essPackageCost`| < > |`0`| `float`|
|`essCostRedPerYear`| < > |`0`| `float`|
|`essSalvageVal`| < > |`0`| `float`|
|`peAndMcDolPerKw`| < > |`11`| `float`|
|`peAndMcBaseCost`| < > |`350`| `float`|
|`iceDolPerKw`| < > |`50`| `float`|
|`iceBaseCost`| < > |`6250`| `float`|
|`fuelCellDolPerKw`| < > |`85`| `float`|
|`fuelStorDolPerKwh`| < > |`0.07`| `float`|
|`fuelStorH2DolPerKwh`| < > |`9.5`| `float`|
|`plugCost`| < > |`500`| `float`|
|`markup`| < > |`1.2`| `float`|
|`tax`| < > |`0.035`| `float`|
|`cngIceDolPerKw`| < > |`55`|`float` |
|`fuelStorCngDolPerKwh`| < > |`7.467735503`|`float` |
|`vehGliderPrice`| < > |`112759`| `float`|
|`segmentName`| < > |`HDTC8`| `string`|
|`GVWRkg`| < > |`36287.43275`| `float`|
|`GVWRCredit_kg`| < > |`0`| amount [kg] vehicle can exceed GVWR[kg], applies during component sizing during optimization `int`|
|`fuel`| < > |`["cd_electricity", "cd_diesel", "cs_diesel"]`| multiple fuel types are permissible, or a single type can be input. For PHEVs, there *must* be specified two Charge Depleting and on Charge Sustaining as shown`string or [string,...]` |
|`maintDolPerMi`|< > |`[0.15,0.16,...0.19]`| `float list`|
|`vocation`|< > |`Long haul`| `string`|
|`modelYear`|< > |`2050`| `int` |
|`region`|< > |`FY21NoProgram`| `string`|
|`TargetRangeMi`|< > |`500`|`float` Note: for PHEVs, T3CO will meet this requirement in CD mode |
|`minSpeed6PercentGradeIn5min`|< > |`30`|`float` |
|`minSpeed1point25PercentGradeIn5min`|< > |`65`|`float` |
|`max0to60secAtGVWR`|< > |`80`|`float` |
|`max0to30secAtGVWR`|< > |`20`|`float` |
|`lw_imp_curve`|< > |`MDHD_noprogram_2050`| `string` Optimization "knob" handling. For certain knobs, there are curves that apply. This value references a column in the light-weighting curves file. Example: [light weighting curves](https://github.com/NREL/T3CO-private/blob/master/run_scripts/external_resources/tda_example/matlltwt_imp_cost_curves_for_tda_in_t3co.csv). Referenced in `sweep.py` [here](https://github.com/NREL/T3CO-private/blob/934dc4718c8a3aeef296bdf39abd6952d65c88f6/run_scripts/sweep.py#L537) |
|`eng_imp_curve`| < > |`MDHD_large_noprogram_2050`| `string` Optimization "knob" handling. For certain knobs, there are curves that apply. This value references a column in the engine efficiency improvement curves file. Example: [engine efficiency curves](https://github.com/NREL/T3CO-private/blob/master/run_scripts/external_resources/tda_example/eng_imp_cost_curves_for_tda_in_t3co.csv). Referenced in `sweep.py` [here](https://github.com/NREL/T3CO-private/blob/934dc4718c8a3aeef296bdf39abd6952d65c88f6/run_scripts/sweep.py#L537) |
|`aero_imp_curve`| < > |`SleeperTractorMidRoof_noprogram_2050`|  `string` Optimization "knob" handling. For certain knobs, there are curves that apply. This value references a column in the drag coefficient improvement curves file. Example: [drag coefficient curves](https://github.com/NREL/T3CO-private/blob/master/run_scripts/external_resources/tda_example/aero_imp_cost_curves_for_tda_in_t3co.csv). Referenced in `sweep.py` [here](https://github.com/NREL/T3CO-private/blob/934dc4718c8a3aeef296bdf39abd6952d65c88f6/run_scripts/sweep.py#L537) |
|`skip_opt`| < > |`True`| Important column! Though it's a bit buried, this column will designate whether this scenario and vehicle combination should be optimized or not. If `True`, then optimization is skipped.`True or False`|
|`knob_min_ess_kwh`| < > | `300`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_max_ess_kwh`| < > | `1500`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_min_motor_kw`| < > | `200`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_max_motor_kw`| < > | `400`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_min_fc_kw`| < > | `100`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_max_fc_kw`| < > | `300`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_min_fs_kwh`| < > | `100`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`knob_max_fs_kwh`| < > | `600`| `nan or float` Optimization settings If this "knob" has a min and max value input from user, it implies that this opimization parameter should be used. |
|`constraint_range`| < > | `nan`| `True or False` Optimization setting. If True, then the constraint is applied and tests for range must be met or exceeded. Test threshold designated by value in `TargetRangeMi`|
|`constraint_accel`| < > |`nan`| `True or False` Optimization setting. If True, then the constraint is applied and tests for acceleratiion. must be met or exceeded Test threshold designated by value in `max0to60secAtGVWR and max0to30secAtGVWR`|
|`constraint_grade`| < > |`nan`| `True or False` Optimization setting. If True, then the constraint is applied and tests for grade must be met or exceeded Test threshold designated by value in `minSpeed6PercentGradeIn5min and minSpeed1point25PercentGradeIn5min`|
|`objective_tco`|  < > | `nan`| `True or False` Optimization setting. If True, then the objective to minimize Total Cost of Ownership is applied. |
|`constraint_c_rate`|  < > | `True`| `True or False` Optimization setting. If True, then the constraint for c rate is applied|
|`shifts_per_year`|  < > | `260`| PHEVs only! See [PHEV Docs](./PHEVs.md#special-inputs)|
|`phev_utility_factor_override`|  < > | `.6`| PHEVs only! See [PHEV Docs](./PHEVs.md#special-inputs)|
|`soc_norm_init_for_grade`|  < > | `.8`| PHEVs only! See [PHEV Docs](./PHEVs.md#special-inputs)|
|`soc_norm_init_for_accel`|  < > | `.85`| PHEVs only! See [PHEV Docs](./PHEVs.md#special-inputs)|
|`perc_motor_power_override_kw_fc_demand_on`|  < > | `.95`| PHEV specific inputs. See [PHEV Docs](./PHEVs.md#special-inputs)|
|`ess_init_soc_grade`|  < > | `.8`|`[0,1]` For BEV or HEV, during grade test, if initial SOC override is desired, rather than using the [FASTSim + T3CO intial SOC regime](acceleration_and_grade_tests.md#default-initial-socs-)|
|`ess_init_soc_accel`| < > |`.85`|`[0,1]`  For BEV or HEV, during grade test, if initial SOC override is desired, rather than using the [FASTSim + T3CO intial SOC regime](acceleration_and_grade_tests.md#default-initial-socs-)|
