# Table of Contents

* [t3co/energy\_models/energy](#t3co/energy_models/energy)
  * [Energy](#t3co/energy_models/energy.Energy)
    * [\_\_new\_\_](#t3co/energy_models/energy.Energy.__new__)
    * [\_\_init\_\_](#t3co/energy_models/energy.Energy.__init__)
    * [run\_fastsim\_model](#t3co/energy_models/energy.Energy.run_fastsim_model)

<a id="t3co/energy_models/energy"></a>

# t3co/energy\_models/energy

<a id="t3co/energy_models/energy.Energy"></a>

## Energy Objects

```python
@dataclass
class Energy()
```

<a id="t3co/energy_models/energy.Energy.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the Energy class.

<a id="t3co/energy_models/energy.Energy.__init__"></a>

#### \_\_init\_\_

```python
def __init__(mpgge: float = None, primary_fuel_range_mi: float = None)
```

Initializes the Energy instance.

**Arguments**:

- `mpgge` _float, optional_ - Miles per gallon gasoline equivalent. Defaults to None.
- `primary_fuel_range_mi` _float, optional_ - Primary fuel range in miles. Defaults to None.

<a id="t3co/energy_models/energy.Energy.run_fastsim_model"></a>

#### run\_fastsim\_model

```python
def run_fastsim_model(
    veh_no: int,
    scenario: Scenario,
    vehicle_file: Union[str, Path] = gl.RESOURCES_FOLDERPATH / "inputs" /
    "Demo_FY22_vehicle_model_assumptions.csv"
) -> None
```

Runs the FASTSim model to calculate mpgge and primary fuel range.

**Arguments**:

- `veh_no` _int_ - Vehicle selection number.
- `scenario` _Scenario_ - Scenario instance containing configuration data.
- `vehicle_file` _Union[str, Path], optional_ - Vehicle model assumptions input CSV file path. Defaults to gl.RESOURCES_FOLDERPATH / "inputs" / "Demo_FY22_vehicle_model_assumptions.csv".

