# Table of Contents

* [t3co/input\_data/scenario](#t3co/input_data/scenario)
  * [Scenario](#t3co/input_data/scenario.Scenario)
    * [\_\_new\_\_](#t3co/input_data/scenario.Scenario.__new__)
    * [from\_file](#t3co/input_data/scenario.Scenario.from_file)
    * [override\_from\_config](#t3co/input_data/scenario.Scenario.override_from_config)
    * [get\_discounted\_value](#t3co/input_data/scenario.Scenario.get_discounted_value)
    * [delete\_dataframes](#t3co/input_data/scenario.Scenario.delete_dataframes)

<a id="t3co/input_data/scenario"></a>

# t3co/input\_data/scenario

<a id="t3co/input_data/scenario.Scenario"></a>

## Scenario Objects

```python
@dataclass
class Scenario()
```

Class object that contains all TCO parameters and performance target (range, grade, accel) information
for a vehicle such that performance and TCO can be computed during optimization.

<a id="t3co/input_data/scenario.Scenario.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the Scenario class.

<a id="t3co/input_data/scenario.Scenario.from_file"></a>

#### from\_file

```python
@classmethod
def from_file(
    cls,
    selection: int,
    scenario_file: Union[str, Path] = gl.RESOURCES_FOLDERPATH / "inputs" /
    "Demo_FY22_scenario_assumptions.csv"
) -> Self
```

Creates a Scenario instance from a CSV file.

**Arguments**:

- `selection` _int_ - The selection index to filter the scenario data.
- `scenario_file` _Union[str, Path]_ - Path to the scenario CSV file.
  

**Returns**:

- `Scenario` - An instance of the Scenario class.

<a id="t3co/input_data/scenario.Scenario.override_from_config"></a>

#### override\_from\_config

```python
def override_from_config(config: Config = None, verbose: bool = False) -> Self
```

Overrides certain scenario fields if use_config is True and config object is not None.

**Arguments**:

- `config` _Config, optional_ - Config object containing configuration data. Defaults to None.
- `verbose` _bool, optional_ - If True, prints the overridden fields. Defaults to False.
  

**Raises**:

- `Exception` - If config file is not attached or scenario.use_config is set to False.

<a id="t3co/input_data/scenario.Scenario.get_discounted_value"></a>

#### get\_discounted\_value

```python
def get_discounted_value(value: float, year_number: int) -> float
```

Calculates the discounted value for a given year.

**Arguments**:

- `value` _float_ - The value to be discounted.
- `year_number` _int_ - The year number for discounting.
  

**Returns**:

- `float` - The discounted value.

<a id="t3co/input_data/scenario.Scenario.delete_dataframes"></a>

#### delete\_dataframes

```python
def delete_dataframes() -> None
```

Deletes DataFrame attributes from the Scenario instance.

