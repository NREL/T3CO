# Table of Contents

* [t3co/run/run\_scenario](#t3co/run/run_scenario)
  * [Config](#t3co/run/run_scenario.Config)
    * [from\_file](#t3co/run/run_scenario.Config.from_file)
    * [from\_dict](#t3co/run/run_scenario.Config.from_dict)
    * [validate\_analysis\_id](#t3co/run/run_scenario.Config.validate_analysis_id)
  * [Scenario](#t3co/run/run_scenario.Scenario)
    * [originalcargo\_kg](#t3co/run/run_scenario.Scenario.originalcargo_kg)
    * [plf\_scenario\_vehicle\_cargo\_capacity\_kg](#t3co/run/run_scenario.Scenario.plf_scenario_vehicle_cargo_capacity_kg)
    * [from\_config](#t3co/run/run_scenario.Scenario.from_config)
  * [check\_phev\_init\_socs](#t3co/run/run_scenario.check_phev_init_socs)
  * [get\_phev\_util\_factor](#t3co/run/run_scenario.get_phev_util_factor)
  * [get\_objective\_simdrive](#t3co/run/run_scenario.get_objective_simdrive)
  * [run\_grade\_or\_accel](#t3co/run/run_scenario.run_grade_or_accel)
  * [create\_fastsim\_vehicle](#t3co/run/run_scenario.create_fastsim_vehicle)
  * [get\_vehicle](#t3co/run/run_scenario.get_vehicle)
  * [get\_scenario\_and\_cycle](#t3co/run/run_scenario.get_scenario_and_cycle)
  * [load\_scenario](#t3co/run/run_scenario.load_scenario)
  * [load\_design\_cycle\_from\_scenario](#t3co/run/run_scenario.load_design_cycle_from_scenario)
  * [load\_design\_cycle\_from\_path](#t3co/run/run_scenario.load_design_cycle_from_path)
  * [set\_test\_weight](#t3co/run/run_scenario.set_test_weight)
  * [reset\_vehicle\_weight](#t3co/run/run_scenario.reset_vehicle_weight)
  * [limit\_cargo\_kg\_for\_moo\_hev\_bev](#t3co/run/run_scenario.limit_cargo_kg_for_moo_hev_bev)
  * [set\_max\_motor\_kw](#t3co/run/run_scenario.set_max_motor_kw)
  * [set\_max\_battery\_kwh](#t3co/run/run_scenario.set_max_battery_kwh)
  * [set\_max\_battery\_power\_kw](#t3co/run/run_scenario.set_max_battery_power_kw)
  * [set\_max\_fuel\_converter\_kw](#t3co/run/run_scenario.set_max_fuel_converter_kw)
  * [set\_fuel\_store\_kwh](#t3co/run/run_scenario.set_fuel_store_kwh)
  * [set\_cargo\_kg](#t3co/run/run_scenario.set_cargo_kg)
  * [vehicle\_scenario\_sweep](#t3co/run/run_scenario.vehicle_scenario_sweep)
  * [run](#t3co/run/run_scenario.run)
  * [rerun](#t3co/run/run_scenario.rerun)

<a id="t3co/run/run_scenario"></a>

# t3co/run/run\_scenario

Module for loading vehicles, scenarios, running them and managing them

<a id="t3co/run/run_scenario.Config"></a>

## Config Objects

```python
@dataclass
class Config()
```

This class reads T3COConfig.csv file containing analysis attributes like vehicle and scenario paths, TCO_method, and scenario attribute overrides.

<a id="t3co/run/run_scenario.Config.from_file"></a>

#### from\_file

```python
def from_file(filename: str, analysis_id: int) -> Self
```

This method generates a Config dictionary from CSV file and calls Config.from_dict

**Arguments**:

- `filename` _str_ - path of input T3CO Config file
- `analysis_id` _int_ - analysis ID selections
  

**Returns**:

- `Self.from_dict` - method that gets Config instance from config_dict

<a id="t3co/run/run_scenario.Config.from_dict"></a>

#### from\_dict

```python
def from_dict(config_dict: dict) -> Self
```

This method generates a Config instance from config_dict

**Arguments**:

- `config_dict` _dict_ - dictionary containing fields from T3CO Config input CSV file
  

**Returns**:

- `Self` - Config instance containining all values from T3CO Config CSV file

<a id="t3co/run/run_scenario.Config.validate_analysis_id"></a>

#### validate\_analysis\_id

```python
def validate_analysis_id(filename: str, analysis_id: int = 0) -> Self
```

This method validates that correct analysis id is input

**Arguments**:

- `filename` _str_ - T3CO Config input CSV file path
  

**Raises**:

- `Exception` - Error if analysis_id not found

<a id="t3co/run/run_scenario.Scenario"></a>

## Scenario Objects

```python
@dataclass
class Scenario()
```

Class object that contains all TCO parameters and performance target (range, grade, accel) information         for a vehicle such that performance and TCO can be computed during optimization

<a id="t3co/run/run_scenario.Scenario.originalcargo_kg"></a>

#### originalcargo\_kg

if needed, should be assigned immediately after vehicle read in

<a id="t3co/run/run_scenario.Scenario.plf_scenario_vehicle_cargo_capacity_kg"></a>

#### plf\_scenario\_vehicle\_cargo\_capacity\_kg

includes cargo credit kg

<a id="t3co/run/run_scenario.Scenario.from_config"></a>

#### from\_config

```python
def from_config(config: Config = None) -> Self
```

This method overrides certain scenario fields if use_config is True and config object is not None

**Arguments**:

- `config` _Config, optional_ - Config object. Defaults to None.

<a id="t3co/run/run_scenario.check_phev_init_socs"></a>

#### check\_phev\_init\_socs

```python
def check_phev_init_socs(a_vehicle: vehicle.Vehicle,
                         scenario: Scenario) -> None
```

This function checks that soc_norm_init_for_grade_pct and soc_norm_init_for_accel_pct are present only for PHEVs

**Arguments**:

- `a_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `scenario` _Scenario_ - T3CO scenario object

<a id="t3co/run/run_scenario.get_phev_util_factor"></a>

#### get\_phev\_util\_factor

```python
def get_phev_util_factor(scenario: Scenario, v: fastsim.vehicle.Vehicle,
                         mpgge: dict) -> float
```

This function gets the PHEV utility factor derived from the computed range of the
vehicle and the operational day range computed from shifts per year and the first vmt year

**Arguments**:

- `scenario` _Scenario_ - T3CO scenario object
- `v` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `mpgge` _dict_ - Miles per Gallon Gasoline Equivalent dictionary
  

**Returns**:

- `uf` _float_ - PHEV computed utility factor

<a id="t3co/run/run_scenario.get_objective_simdrive"></a>

#### get\_objective\_simdrive

```python
def get_objective_simdrive(
        analysis_vehicle: vehicle.Vehicle,
        cycle: fastsim.cycle.Cycle) -> fastsim.simdrive.SimDrive
```

This function obtains the SimDrive for accel and grade test

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `cycle` _fastsim.cycle.Cycle_ - FASTSim Cycle object
  

**Returns**:

- `sd` _fastsim.simdrive.SimDrive_ - FASTSim SimDrive object containing vehicle inputs and simulation output attributes

<a id="t3co/run/run_scenario.run_grade_or_accel"></a>

#### run\_grade\_or\_accel

```python
def run_grade_or_accel(test: str, analysis_vehicle: fastsim.vehicle.Vehicle,
                       sim_drive: fastsim.simdrive.SimDrive,
                       ess_init_soc: float) -> None
```

This function handles initial SOC considerations for grade and accel tests

If ess_init_soc override is passed, use that
Else if the vehicle is an HEV, use the standard HEV init SOC values for accel and grade
Else, let FASTSim determine init SOC in sim_drive()
BEVs use max_soc
PHEVs use max_soc
Conv init_soc doesn't matter
HEVs attempt SOC balancing but that is overrident by HEV test init SOC

**Arguments**:

- `test` _str_ - 'accel' or 'grade' test
- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `sim_drive` _fastsim.simdrive.SimDrive_ - FASTSim SimDrive object
- `ess_init_soc` _float_ - ESS initial state of charge (SOC)
  

**Raises**:

- `Exception` - if test not in ['accel', 'grade']

<a id="t3co/run/run_scenario.create_fastsim_vehicle"></a>

#### create\_fastsim\_vehicle

```python
def create_fastsim_vehicle(veh_dict: dict = None) -> fastsim.vehicle.Vehicle
```

This function creates and returns an empty FASTSim vehicle object with no attributes or

**Arguments**:

- `veh_dict` _dict, optional_ - Vehicle attributes dict. Defaults to None.
  

**Returns**:

- `v` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object

<a id="t3co/run/run_scenario.get_vehicle"></a>

#### get\_vehicle

```python
def get_vehicle(veh_no: int, veh_input_path: str) -> fastsim.vehicle.Vehicle
```

This function loads vehicle object from vehicle number and input csv filepath

**Arguments**:

- `veh_no` _int_ - vehicle selection number
- `veh_input_path` _str_ - vehicle model assumptions input CSV file path
  

**Returns**:

- `veh` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object

<a id="t3co/run/run_scenario.get_scenario_and_cycle"></a>

#### get\_scenario\_and\_cycle

```python
def get_scenario_and_cycle(
        veh_no: int,
        scenario_inputs_path: str,
        a_vehicle: fastsim.vehicle.Vehicle = None,
        config: Config = None) -> Tuple[Scenario, fastsim.cycle.Cycle]
```

This function uses helper methods load_scenario and load_design_cycle_from_scenario         to get scenario object and cycle object corresponding to selected vehicle (by veh_no)

**Arguments**:

- `veh_no` _int_ - vehicle selection number
- `scenario_inputs_path` _str_ - input file path for scenario assumptions CSV
- `a_vehicle` _fastsim.vehicle.Vehicle, optional_ - FASTSim vehicle object for given selection. Defaults to None.
- `config` _Config, optional_ - Config object for current analysis. Defaults to None.
  

**Returns**:

- `scenario` _Scenario_ - T3CO scenario object selected
- `cyc` _fastsim.cycle.Cycle_ - FASTSim cycle object selected

<a id="t3co/run/run_scenario.load_scenario"></a>

#### load\_scenario

```python
def load_scenario(veh_no: int,
                  scenario_inputs_path: str,
                  a_vehicle: fastsim.vehicle.Vehicle = None,
                  config: Config = None) -> Scenario
```

This function gets the Scenario object from scenario input CSV filepath, initializes some fields,          and overrides some fields based on Config object

**Arguments**:

- `veh_no` _int_ - vehicle selection number
- `scenario_inputs_path` _str_ - input file path for scenario assumptions CSV
- `a_vehicle` _fastsim.vehicle.Vehicle, optional_ - FASTSim vehicle object for given selection. Defaults to None.
- `config` _Config, optional_ - Config object for current analysis. Defaults to None.
  

**Returns**:

- `scenario` _Scenario_ - Scenario object for given selection

<a id="t3co/run/run_scenario.load_design_cycle_from_scenario"></a>

#### load\_design\_cycle\_from\_scenario

```python
def load_design_cycle_from_scenario(
        scenario: Scenario,
        cyc_file_path: str = gl.OPTIMIZATION_DRIVE_CYCLES
) -> fastsim.cycle.Cycle
```

This helper method loads the design cycle used for mpgge and range determination.
It can also be used standalone to get cycles not in standard gl.OPTIMIZATION_DRIVE_CYCLES location,
but still needs cycle name from scenario object, carried in scenario.drive_cycle.
If the drive cycles are a list of tuples, handle accordingly with eval.

**Arguments**:

- `scenario` _Scenario_ - Scenario object for current selection
- `cyc_file_path` _str, optional_ - drivecycle input file path. Defaults to gl.OPTIMIZATION_DRIVE_CYCLES.
  

**Returns**:

- `range_cyc` _fastsim.cycle.Cycle_ - FASTSim cycle object for current Scenario object

<a id="t3co/run/run_scenario.load_design_cycle_from_path"></a>

#### load\_design\_cycle\_from\_path

```python
def load_design_cycle_from_path(cyc_file_path: str) -> fastsim.cycle.Cycle
```

This helper method loads the Cycle object from the drivecycle filepath

**Arguments**:

- `cyc_file_path` _str_ - drivecycle input file path
  

**Returns**:

- `range_cyc` _fastsim.cycle.Cycle_ - FASTSim cycle object for current Scenario object

<a id="t3co/run/run_scenario.set_test_weight"></a>

#### set\_test\_weight

```python
def set_test_weight(vehicle: fastsim.vehicle.Vehicle,
                    scenario: Scenario) -> None
```

assign standardized vehicle mass for accel and grade test using GVWR and GVWR Credit

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `scenario` _t3co.run_scenario.Scenario_ - T3CO scenario object

<a id="t3co/run/run_scenario.reset_vehicle_weight"></a>

#### reset\_vehicle\_weight

```python
def reset_vehicle_weight(vehicle: fastsim.vehicle.Vehicle) -> None
```

This function resets vehicle mass after loaded weight tests are done for accel and grade

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object

<a id="t3co/run/run_scenario.limit_cargo_kg_for_moo_hev_bev"></a>

#### limit\_cargo\_kg\_for\_moo\_hev\_bev

```python
def limit_cargo_kg_for_moo_hev_bev(
        opt_scenario: Scenario,
        mooadvancedvehicle: fastsim.vehicle.Vehicle) -> None
```

This helper method is used within T3COProblem to assign limited cargo capacity based on GVWR + GVWRCredit and optimization vehicle mass for advanced vehicles

**Arguments**:

- `opt_scenario` _t3co.run_scenario.Scenario_ - T3CO scenario object
- `mooadvancedvehicle` _fastsim.vehicle.Vehicle_ - pymoo optimization vehicle

<a id="t3co/run/run_scenario.set_max_motor_kw"></a>

#### set\_max\_motor\_kw

```python
def set_max_motor_kw(analysis_vehicle: fastsim.vehicle.Vehicle,
                     scenario: Scenario, max_motor_kw: float) -> None
```

This helper method is used within T3COProblem to set max_motor_kw to optimization vehicle and set kw_demand_fc_on if PHEV

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `scenario` _run_scenario.Scenario_ - T3CO Scenarion object
- `max_motor_kw` _float_ - max motor power /kW

<a id="t3co/run/run_scenario.set_max_battery_kwh"></a>

#### set\_max\_battery\_kwh

```python
def set_max_battery_kwh(analysis_vehicle: fastsim.vehicle.Vehicle,
                        max_ess_kwh: float) -> None
```

This helper method is used within T3COProblem to set max_ess_kwh to optimization vehicle

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `max_ess_kwh` _float_ - max energy storage system energy capacity /kWh

<a id="t3co/run/run_scenario.set_max_battery_power_kw"></a>

#### set\_max\_battery\_power\_kw

```python
def set_max_battery_power_kw(analysis_vehicle: fastsim.vehicle.Vehicle,
                             max_ess_kw: float) -> None
```

This helper method is used within T3COProblem to set max_ess_kwx to optimization vehicle

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `max_ess_kw` _float_ - max energy storage system power /kW

<a id="t3co/run/run_scenario.set_max_fuel_converter_kw"></a>

#### set\_max\_fuel\_converter\_kw

```python
def set_max_fuel_converter_kw(analysis_vehicle: fastsim.vehicle.Vehicle,
                              fc_max_out_kw: float) -> None
```

This helper method is used within T3COProblem to set fc_max_out_kw to optimization vehicle

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `fc_max_out_kw` _float_ - max fuel converter power /kW

<a id="t3co/run/run_scenario.set_fuel_store_kwh"></a>

#### set\_fuel\_store\_kwh

```python
def set_fuel_store_kwh(analysis_vehicle: fastsim.vehicle.Vehicle,
                       fs_kwh: float) -> None
```

This helper method is used within T3COProblem to set fs_kwh to optimization vehicle

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `fs_kwh` _float_ - fuel storage energy capacity /kWh

<a id="t3co/run/run_scenario.set_cargo_kg"></a>

#### set\_cargo\_kg

```python
def set_cargo_kg(analysis_vehicle: fastsim.vehicle.Vehicle, cargo_kg)
```

This helper method is used within T3COProblem to set cargo_kg to optimization vehicle

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `cargo_kg` _float_ - vehicle cargo capacity /kg

<a id="t3co/run/run_scenario.vehicle_scenario_sweep"></a>

#### vehicle\_scenario\_sweep

```python
def vehicle_scenario_sweep(vehicle: fastsim.vehicle.Vehicle,
                           scenario: Scenario,
                           range_cyc,
                           verbose=False,
                           **kwargs)
```

This function contains helper methods such as get_tco_of_vehicle, check_phev_init_socs, get_accel, and get_gradeability    and returns a dictionary of all TCO related outputs

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for current selection
- `scenario` _Scenario_ - Scenario object for current selection
- `range_cyc` _fastsim.cycle.Cycle_ - FASTSim cycle object for current scenario
- `verbose` _bool, optional_ - if selected, prints out the TCO calculation process. Defaults to False.
  

**Returns**:

- `out` _dict_ - output dictionary containing TCO elements

<a id="t3co/run/run_scenario.run"></a>

#### run

```python
def run(veh_no: int,
        vocation: str = "blank",
        vehicle_input_path: str = gl.FASTSIM_INPUTS,
        scenario_inputs_path: str = gl.OTHER_INPUTS)
```

This function runs vehicle_scenario_sweep based on vehicle and scenario objects read from input file paths

**Arguments**:

- `veh_no` _int_ - vehicle selection number
- `vocation` _str, optional_ - vocation description of selected vehicle. Defaults to "blank".
- `vehicle_input_path` _str, optional_ - input file path for vehicle assumptions CSV. Defaults to gl.FASTSIM_INPUTS.
- `scenario_inputs_path` _str, optional_ - input file path for scenario assumptions CSV. Defaults to gl.OTHER_INPUTS.
  

**Returns**:

- `out` _dict_ - output dictionary containing TCO results

<a id="t3co/run/run_scenario.rerun"></a>

#### rerun

```python
def rerun(vehicle: fastsim.vehicle.Vehicle, vocation: str, scenario: Scenario)
```

This function runs vehicle_scenario_sweep when given the vehicle and scenario objects

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `vocation` _str_ - vocation description
- `scenario` _Scenario_ - Scenario object
  

**Returns**:

- `out` _dict_ - output dictionary containing TCO outputs

