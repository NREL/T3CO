

# Acceleration and Grade

- [Accel and Grade Test Overview](#overview)
- [Accel and Grade Test Target Inputs](#test-target-inputs)
- [Default Initial SOCs](#default-socs)


## Accel and Grade Test Overview <a name="overview"></a>

The vehicle is tested to determine if its powertrain is powerful enough to achieve or exceed its grade and acceleration targets. 

### Acceleration Test

[**Acceleration Test code**](https://github.com/NREL/T3CO/blob/295ee11c72d6f387f8eb5b60bc35304a0bbfb0db/t3co/objectives/accel.py#L13)

There are two tests:
- **seconds to achieve zero to sixty mph**
- **seconds to achieve zero to thirty mph**

The test is done with the vehicle usually at [`scenario.gvwr_kg + scenario.GvwrCreditK`](https://github.com/NREL/T3CO/blob/295ee11c72d6f387f8eb5b60bc35304a0bbfb0db/t3co/run_scenario.py#L23), or just at normal weight.

The vehicle is given a synthetic drive cycle of 300 seconds of length with zero grade. The vehicle is forced to run at top speed immediately. A test is done to see if the vehicle reaches the target speeds of 30 and 60 mph. If the vehicle reaches those speeds, interpolation is performed to compute the precise second at which the vehicle reaches those target speeds. The test passes, for example, if the second that the vehicle reaches 30 mph is `<= max_time_0_to_30mph_at_gvwr_s`. The test returns the acceleration time for the two tests in seconds.


### Grade Test

[**Grade Test code**](https://github.com/NREL/T3CO/blob/295ee11c72d6f387f8eb5b60bc35304a0bbfb0db/t3co/objectives/gradeability.py#L13)

Likewise, there are two tests for Grade. The grade tests measure the max speed [MPH] reached by the vehicle at 6% grade and 1.25% grade within 5 minutes. The grade test returns the max speed achieved [MPH] for the two tests.

The test is done with the vehicle usually at [`scenario.gvwr_kg + scenario.GvwrCreditK`](https://github.com/NREL/T3CO/blob/295ee11c72d6f387f8eb5b60bc35304a0bbfb0db/t3co/run_scenario.py#L23), or just at normal weight.



## Accel and Grade Test Target Inputs <a name="test-target-inputs"></a>

Inputs from the T3CO input file:

| test | scenario input | value |
|-----|-----|-----|
|Acceleration 0 to 60 |max_time_0_to_60mph_at_gvwr_s| `seconds, int > 0` |
|Acceleration 0 to 30 |max_time_0_to_30mph_at_gvwr_s| `seconds, int > 0` |
|Min speed at 6% grade [MPH] |min_speed_at_6pct_grade_in_5min_mph| `MPH, int > 0` |
|Min speed at 1.25% grade [MPH]|min_speed_at_1p25pct_grade_in_5min_mph| `MPH, int > 0` |


## Default Initial SOCs <a name="default-socs"></a>

The *default* behavior, what the code does for inital SOC for tests in the absense of any input for `ess_init_soc_grade/accel`, or `ess_init_soc_for_grade/accel`, is a mix of **FASTSim's** default behaviors and some overrides that **T3CO** configures. 

    init_soc comes from simdrive()
        BEVs use max_soc
        PHEVs use max_soc
        Conv init_soc doesn't matter
    
    if the vehicle is a HEV
        For accel, initial SOC is (max_soc + min_soc) / 2.0
        For grade, initial SOC is min_soc
    
    or if ess_init_soc is passed to get_gradeability and get_accel
    
    for PHEVs, there is an additional setting for ess_init_soc
        soc_norm_init_for_accel_pct # column in Scenario file
        soc_norm_init_for_grade_pct # column in Scenario file
        These values are in the range 0 to 1 (0 is min_soc)
    
        For example, for the accel test
        init_soc = min_soc + (soc_norm_init_for_accel_pct * (max_soc - min_soc))

