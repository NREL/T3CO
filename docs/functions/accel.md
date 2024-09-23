# Table of Contents

* [t3co/objectives/accel](#t3co/objectives/accel)
  * [get\_accel](#t3co/objectives/accel.get_accel)

<a id="t3co/objectives/accel"></a>

# t3co/objectives/accel

Module for simulating acceleration performance.

<a id="t3co/objectives/accel.get_accel"></a>

#### get\_accel

```python
def get_accel(
        analysis_vehicle: fastsim.vehicle.Vehicle,
        scenario: run_scenario.Scenario = None,
        set_weight_to_max_kg: bool = True,
        verbose=False,
        ess_init_soc=None) -> Tuple[float, float, fastsim.vehicle.Vehicle]
```

This function runs a simdrive for getting 0-to-60 and 0-30 mph time with fully laden weight at GVWR (plus gvwr_credit_kg?)


**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for analysis vehicle
- `scenario` _run_scenario.Scenario, optional_ - Scenario object for current selection. Defaults to None.
- `set_weight_to_max_kg` _bool, optional_ - if True, runs run_scenario.set_test_weight(). Defaults to True.
- `verbose` _bool, optional_ - if True, prints the process steps. Defaults to False.
- `ess_init_soc` _float, optional_ - ESS initial SOC override. Defaults to None.
  

**Returns**:

- `zero_to_sixty` _float_ - 0-60 mph acceleration time in sec
- `zero_to_thirty` _float_ - 0-30 mph acceleration time in sec
- `accel_simdrive` _fastsim.simdrive.SimDrive_ - FASTSim.simdrive.SimDrive object for running the acceleration drivecycle

