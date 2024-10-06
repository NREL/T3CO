# Contents

- [Optimization Overview](#optOverview)
- [Optimization from Sweep Module](#optsweepmodule)
- [Optimization Inputs](#optInputs)
- [Conventional Considerations](#ConventionalConsiderations)
- [BEV Considerations](#bevsConsiderations)
- [HEV/FCEV Considerations](#HEVFCEVConsiderations)
- [PHEV Considerations](#PHEVConsiderations)

## Optimization Overview <a name="optOverview"></a>

By default, T3CO uses pymoo to minimize TCO while meeting constraints on required performance metrics (range, acceleration, grade). 

```
Objective (minimized):
TCO, PHEV_MINIMIZE_FUEL_USE_OBJECTIVE

Constraints (met):
RANGE, ACCEL, GRADE
```

In general, all knobs that apply to each powertrain will be active.

A blank in either min or max of the knob will disable that knob. (use value from vehicle input)
A blank in eng_eff_imp_curve_sel, aero_drag_imp_curve_sel, and ltwt_imp_curve will turn those off. (set to cda imp and ltwt redux to zeros, and leave fuel converter peak efficiency unchanged)

```
# Decision variables / "knobs":
fs_kwh     (liquid fuel tank or hydrogen tank)
fc_max_kw (engine or fuel cell size kw) 
ess_max_kwh  (battery size kwh)
mc_max_kw (motor size kw)
CdA_perc_imp (aerodynamic drag coefficient)
fc_peak_eff (engine peak efficiency - adjusts the entire engine efficiency curve. Power on x axis, y axis is efficiency)
wt_delta_perc (light weighting percent off of baseline vehicle mass)

BEV: {wt_delta_perc, CdA_perc_imp, ess_max_kwh, mc_max_kw}
HEV: {wt_delta_perc, CdA_perc_imp, fc_peak_eff, ess_max_kwh, mc_max_kw, fc_max_kw, fs_kwh}
CONV: {wt_delta_perc, CdA_perc_imp, fc_peak_eff, fc_max_kw, fs_kwh}
FCEV: {wt_delta_perc, CdA_perc_imp, fc_peak_eff, ess_max_kwh, mc_max_kw, fc_max_kw, fs_kwh}
```
### All applicable constraint targets for each powertrain

```
BEV: RANGE, ACCEL, GRADE, TCO
HEV: ACCEL, GRADE, TCO
CONV: ACCEL, GRADE, TCO
FCEV: RANGE, ACCEL, GRADE, TCO ??? < verify
```

## Optimization from Sweep Module <a name="optsweepmodule"></a>

One way to activate optimization, and the general code flow, is to use [sweep.py](https://github.com/NREL/T3CO/blob/master/run_scripts/sweep.py). The optimization algorithms available are enumerated in the [moo module](https://github.com/NREL/T3CO/blob/a27b575d71fa64adc746a20a7f6ba65d09f987da/t3co/moopack/moo.py#L76).

An example use, employing both [**NSGA2** and **PatternSearch**](https://pymoo.org/algorithms/list.html) in an ensemble optimization approach:

        python sweep.py  -algorithms "['NSGA2', 'PatternSearch']" -dir_mark "multi-algo-test" -dst_dir C:\Users\users\Documents\testruns\multialgo-test3 -selections "range(0,140)"


## Optimization Inputs <a name="optInputs"></a>

### example means of specifying targets in **scenario** file
target_range_mi | min_speed_at_6pct_grade_in_5min_mph | min_speed_at_1p25pct_grade_in_5min_mph | max_time_0_to_60mph_at_gvwr_s | max_time_0_to_30mph_at_gvwr_s
-- | -- | -- | -- | --
750 | 30 | 65 | 80 | 20
750 | 30 | 65 | 80 | 20
750 | 30 | 65 | 80 | 20


### example means of specifying improvement cost curves in **scenario** file
lw_imp_curve_sel | eng_eff_imp_curve_sel | aero_drag_imp_curve_sel
-- | -- | --
MDHD_xyz | MDHD_large_noprogram_2025 | MDHD_abcdef

See: [EngineEffImprovementCostCurve.csv](https://github.com/NREL/T3CO/blob/7b56eb37bf5a57e6cd0ce761fc1708ee151c956f/t3co/resources/auxiliary/EngineEffImprovementCostCurve.csv)

where small medium large engine sizes refers to 
6.7 L,   <250 kW
11 L
15 L 250-375 kW
according to the LD MDHD Benefits Analysis Assumptions FY2021 spreadsheet

-  | L | hp | kW
-- | -- | -- | --
class 4,5 all applications | 7 | 200 | 149
class 6,7 all applications | 7 | 270 | 201
class 8 urban | 11 | 350 | 261
class 8 regional & multipurpose | 11 or 15 | 350 or 455 | 261 or 339
class 7 day cabs | 11 | 350 | 261
class 8 day and sleeper cabs | 15 | 455 | 339

In the scenario file: specify the following variables with the appropriate improvement cost curve, with the available options being in: [AeroDragImprovementCostCurve](https://github.com/NREL/T3CO/blob/7b56eb37bf5a57e6cd0ce761fc1708ee151c956f/t3co/tests/tco_tests/test_cycles/accel.csv)

The improvement cost curve files include optimizer knob bounds specified for CdA and engine efficiency (dependent on vehicle type and scenario and year, based on the Technology Manager inputs and Alicia Birky), and lightweighting (allowed to lightweight over full curve).

For the other decision variables / knobs, the scenario file will need to specify reasonable (i.e. physically feasible and sensible) optimizer knob bounds for:
`knob_min_ess_kwh, knob_min_motor_kw, knob_min_fc_kw, knob_max_ess_kwh, knob_max_motor_kw, knob_max_fc_kw`
(code will use the appropriate combinations of fc/motor/ess for each powertrain)


### example of **engine cost curves input**, referred to via **scenario file** selection in `eng_eff_imp_curve_sel` column

name | MDHD_large_noprogram_2020 | MDHD_large_noprogram_2025
-- | -- | --
eng_cost | [0,0.35,6,13.25,14.15,30.7,39.8] | [0,0.35,7.35,25.65,32.45]
eng_pctpt | [0.45,0.49,0.52,0.52,0.53,0.53,0.59] | [0.45,0.49,0.53,0.53,0.59]
fc_peak_eff_knob_max | 0.481405 | 0.492
fc_peak_eff_knob_min | 0.45 | 0.45


### Drive Cycles for Optimization
**design cycle** will be a composite of the 3 standard **EPA** drive cycles

#### initial/default weights
rural | urban | transient
-- | -- | --
86  |  9  |   5

These are the EPA weights for Sleeper cabs. From EPA_RIA_Inputs, we will input appropriate cycle weights for each size class.

rural     = EPA_Ph2_rural_interstate_65mph.csv
urban     = EPA_Ph2_urban_highway_55mph.csv
transient = EPA_Ph2_transient.csv

#### vehicle input file example for drive_cycle


selection | scenario_name | drive_cycle | …
-- | -- | -- | --
1 | Class 8 Sleeper cab (Diesel, 2021, program success) | [(EPA_Ph2_rural_interstate_65mph.csv, .86),   (EPA_Ph2_urban_highway_55mph.csv, .09), (EPA_Ph2_transient.csv, .05)] | …
2 | Class 8 Sleeper cab (Diesel, 2027, program success) | [(EPA_Ph2_rural_interstate_65mph.csv, .86),   (EPA_Ph2_urban_highway_55mph.csv, .09), (EPA_Ph2_transient.csv, .05)] | …






## Conventional Considerations <a name="ConventionalConsiderations"></a>

## BEV Considerations <a name="bevsConsiderations"></a>

## HEV/FCEV Considerations <a name="HEVFCEVConsiderations"></a>

## PHEV Considerations <a name="PHEVConsiderations"></a>

#### `motor_power_override_kw_fc_demand_on_pct`
During PHEV optimization, an adjustment for PHEVs that is not made for any other powertrain types to the value of `kw_demand_fc_on` for the vehicle. `kw_demand_fc_on` is a vehicle file input and a type of hyrbid vehicle controls parameter. This parameter is the kW threshold of power demand from the drive cycle at which the fuel converter is activated to meet trace. In order to have the kW threshold float along with the sizing of the motor during optimization, **T3CO** sets the value of `kw_demand_fc_on` based on a set percentage of the motor size, `motor_power_override_kw_fc_demand_on_pct`. This percentage is specified in the **T3CO** scenario file. 

If this percentage is not specified in the **T3CO** scenario file, then `kw_demand_fc_on` is not adjusted and remains the static value from the vehicle input file. `motor_power_override_kw_fc_demand_on_pct` overrides `kw_demand_fc_on`. If neither are provided then T3CO will error out.

This adjustment happens in `t3co.run_scenario.set_max_motor_kw(vehicle, new_kw_value)` when the optimization loop calls `set_max_motor_kw`
    
    if vehicle.veh_pt_type == PHEV:
        vehicle.mc_max_kw = optimization_function(TCO, grade and acceleration performance)
        kw_demand_fc_on = motor_power_override_kw_fc_demand_on_pct * vehicle.mc_max_kw
