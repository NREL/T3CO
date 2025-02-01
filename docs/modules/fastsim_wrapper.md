# Table of Contents

* [t3co/energy\_models/fastsim\_model/fastsim\_wrapper](#t3co/energy_models/fastsim_model/fastsim_wrapper)
  * [RunFastsim](#t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim)
    * [\_\_new\_\_](#t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim.__new__)
    * [load\_vehicle](#t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim.load_vehicle)
    * [load\_design\_cycle\_from\_scenario](#t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim.load_design_cycle_from_scenario)
    * [load\_design\_cycle\_from\_path](#t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim.load_design_cycle_from_path)
    * [get\_simdrive](#t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim.get_simdrive)
    * [get\_range](#t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim.get_range)

<a id="t3co/energy_models/fastsim_model/fastsim_wrapper"></a>

# t3co/energy\_models/fastsim\_model/fastsim\_wrapper

<a id="t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim"></a>

## RunFastsim Objects

```python
class RunFastsim()
```

<a id="t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the RunFastsim class.

<a id="t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim.load_vehicle"></a>

#### load\_vehicle

```python
def load_vehicle(veh_no: int,
                 veh_input_path: Union[str, Path],
                 use_rust: bool = True) -> fastsim.vehicle.Vehicle
```

Loads vehicle object from vehicle number and input CSV filepath.

**Arguments**:

- `veh_no` _int_ - Vehicle selection number.
- `veh_input_path` _Union[str, Path]_ - Vehicle model assumptions input CSV file path.
  

**Returns**:

- `fastsim.vehicle.Vehicle` - FASTSim vehicle object.

<a id="t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim.load_design_cycle_from_scenario"></a>

#### load\_design\_cycle\_from\_scenario

```python
def load_design_cycle_from_scenario(
    scenario: Scenario,
    cyc_file_path: Union[str, Path] = gl.CYCLES_FOLDER,
    return_rustcycle: bool = True
) -> Union[fastsim.cycle.Cycle, List[fastsim.cycle.Cycle]]
```

Loads the design cycle used for mpgge and range determination.

**Arguments**:

- `scenario` _Scenario_ - Scenario object for current selection.
- `cyc_file_path` _Union[str, Path], optional_ - Drive cycle input file path. Defaults to gl.CYCLES_FOLDER.
  

**Returns**:

  Union[fastsim.cycle.Cycle, List[fastsim.cycle.Cycle]]: FASTSim cycle object for current Scenario object.

<a id="t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim.load_design_cycle_from_path"></a>

#### load\_design\_cycle\_from\_path

```python
def load_design_cycle_from_path(
    cyc_file_path: Union[str, Path],
    return_rustcycle: bool = True
) -> Union[fastsim.cycle.RustCycle, fastsim.cycle.Cycle]
```

Loads the Cycle object from the drive cycle filepath.

**Arguments**:

- `cyc_file_path` _Union[str, Path]_ - Drive cycle input file path.
  

**Returns**:

- `fastsim.cycle.Cycle` - FASTSim cycle object for current Scenario object.

<a id="t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim.get_simdrive"></a>

#### get\_simdrive

```python
def get_simdrive(
        cycle: fastsim.cycle.Cycle) -> fastsim.fastsimrust.RustSimDrive
```

Creates a SimDrive object for the given cycle and vehicle.

**Arguments**:

- `cycle` _fastsim.cycle.Cycle_ - The drive cycle.
  

**Returns**:

- `fastsim.fastsimrust.RustSimDrive` - The RustSimDrive object.

<a id="t3co/energy_models/fastsim_model/fastsim_wrapper.RunFastsim.get_range"></a>

#### get\_range

```python
def get_range() -> None
```

Calculates the range of the vehicle based on its type and energy storage.

