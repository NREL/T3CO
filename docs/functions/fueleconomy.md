# Table of Contents

* [t3co/objectives/fueleconomy](#t3co/objectives/fueleconomy)
  * [get\_range\_mi](#t3co/objectives/fueleconomy.get_range_mi)
  * [get\_sim\_drive](#t3co/objectives/fueleconomy.get_sim_drive)
  * [get\_mpgge](#t3co/objectives/fueleconomy.get_mpgge)

<a id="t3co/objectives/fueleconomy"></a>

# t3co/objectives/fueleconomy

Module containing functions for calculating fuel economy objectives.

<a id="t3co/objectives/fueleconomy.get_range_mi"></a>

#### get\_range\_mi

```python
def get_range_mi(mpgge_info: dict, vehicle: fastsim.vehicle.Vehicle,
                 scenario: run_scenario.Scenario) -> dict
```

This funcion computes range [miles] from mpgge using vehicle powertrain type and energy (or fuel) store size.

Considerations:
- at some point each vehicle powertrain type could employ the concept
of a "first fuel" or "primary fuel" - so return a primary fuel-based range for all
powertrains.
- PHEVs have two fuels (generally diesel and electricity). So return two ranges:
-- One for determining range during optimization
i.e. the CD range that PHEVs are commonly specified with
(e.g. PHEV-50 = PHEV with 50 mi AER "All-Electric Range" ~= CD range)
-- One that represents the "true" total PHEV range (CD + CS using both ESS and FS)

**Arguments**:

- `mpgge_info` _dict_ - Dictionary containing MPGGE breakdown
- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
  

**Returns**:

- `range_dict` _dict_ - Dictionary containing different range results

<a id="t3co/objectives/fueleconomy.get_sim_drive"></a>

#### get\_sim\_drive

```python
def get_sim_drive(erc, v, scenario)
```

This helper method returns a FASTSim SimDrive object using the vehicle, drive cycle and scenario

**Arguments**:

- `erc` _fastsim.cycle.Cycle| List[Tuple[fastsim.cycle.Cycle, float_ - FASTSim range cycle object or list of tuples of cycles
- `v` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object for current selection
  

**Returns**:

- `sim_drive` _fastsim.simdrive.SimDrive_ - FASTSim SimDrive object

<a id="t3co/objectives/fueleconomy.get_mpgge"></a>

#### get\_mpgge

```python
def get_mpgge(
    eff_range_cyc: fastsim.cycle.Cycle
    | List[Tuple[fastsim.cycle.Cycle, float]],
    v: fastsim.vehicle.Vehicle,
    scenario,
    diagnostic=False
) -> Tuple[dict, List[fastsim.simdrive.SimDrive], List[dict]]
```

This helper method gets the composite mpgge fuel efficiency of vehicle for each efficiency_range Drive Cycle and weight.
It runs the vehicle using efficiency range cycle(s) and returns mpgge based on the powertrain type

Method computes a composite mpgge from multiple drive cycles and weights for each cycle.
If the user passes in a single Drive Cycle rather than a list of tuples, the base case of
a composite mpgge from a single Drive Cycle and a single weight, 1, is computed.

Also updates the vehicle's corresponding scenario object

**Arguments**:

- `eff_range_cyc` _fastsim.cycle.Cycle | List[Tuple[fastsim.cycle.Cycle, float]]_ - efficiency range cycle
- `v` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object for current selection
- `diagnostic` _bool, optional_ - if True, returns all mpgge dicts. Defaults to False.
  

**Raises**:

- `ValueError` - unknown vehicle powertrain type
  

**Returns**:

- `mpgge_comp` _dict_ - Dictionary containing MPGGE breakdowns
- `sim_drives` _List[fastsim.simdrive.SimDrive]_ - List of simdrives for charge depleting and charge sustaining cycles
- `mpgges` _List[dict], optional_ - if diagnostic==True, returns additional

