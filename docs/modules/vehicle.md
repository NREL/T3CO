# Table of Contents

* [t3co/input\_data/vehicle](#t3co/input_data/vehicle)
  * [Vehicle](#t3co/input_data/vehicle.Vehicle)
    * [\_\_new\_\_](#t3co/input_data/vehicle.Vehicle.__new__)
    * [from\_config](#t3co/input_data/vehicle.Vehicle.from_config)
    * [from\_db](#t3co/input_data/vehicle.Vehicle.from_db)
    * [set\_veh\_kg](#t3co/input_data/vehicle.Vehicle.set_veh_kg)
    * [delete\_dataframes](#t3co/input_data/vehicle.Vehicle.delete_dataframes)

<a id="t3co/input_data/vehicle"></a>

# t3co/input\_data/vehicle

<a id="t3co/input_data/vehicle.Vehicle"></a>

## Vehicle Objects

```python
@dataclass
class Vehicle()
```

<a id="t3co/input_data/vehicle.Vehicle.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the OpportunityCosts class.

<a id="t3co/input_data/vehicle.Vehicle.from_config"></a>

#### from\_config

```python
@classmethod
def from_config(cls, selection: int, config: Config) -> Self
```

Creates a Vehicle instance from the configuration.

**Arguments**:

- `selection` _int_ - The selection index.
- `config` _Config_ - The configuration instance.
  

**Returns**:

- `Self` - An instance of the Vehicle class.

<a id="t3co/input_data/vehicle.Vehicle.from_db"></a>

#### from\_db

```python
@classmethod
def from_db(cls, selection: int, vehicle_db_file: Union[str, Path]) -> Self
```

Creates a Vehicle instance from the vehicle database file.

**Arguments**:

- `selection` _int_ - The selection index.
- `vehicle_db_file` _Union[str, Path]_ - The vehicle database file path.
  

**Returns**:

- `Self` - An instance of the Vehicle class.

<a id="t3co/input_data/vehicle.Vehicle.set_veh_kg"></a>

#### set\_veh\_kg

```python
def set_veh_kg() -> None
```

Sets the vehicle weight in kilograms.

<a id="t3co/input_data/vehicle.Vehicle.delete_dataframes"></a>

#### delete\_dataframes

```python
def delete_dataframes() -> None
```

Deletes DataFrame attributes from the Vehicle instance.

