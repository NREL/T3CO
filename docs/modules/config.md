# Table of Contents

* [t3co/input\_data/config](#t3co/input_data/config)
  * [Config](#t3co/input_data/config.Config)
    * [\_\_new\_\_](#t3co/input_data/config.Config.__new__)
    * [from\_file](#t3co/input_data/config.Config.from_file)
    * [from\_dict](#t3co/input_data/config.Config.from_dict)
    * [validate\_analysis\_id](#t3co/input_data/config.Config.validate_analysis_id)
    * [check\_drivecycles\_and\_create\_selections](#t3co/input_data/config.Config.check_drivecycles_and_create_selections)
    * [read\_auxiliary\_files](#t3co/input_data/config.Config.read_auxiliary_files)
    * [delete\_dataframes](#t3co/input_data/config.Config.delete_dataframes)

<a id="t3co/input_data/config"></a>

# t3co/input\_data/config

<a id="t3co/input_data/config.Config"></a>

## Config Objects

```python
@dataclass
class Config()
```

<a id="t3co/input_data/config.Config.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the Config class.

<a id="t3co/input_data/config.Config.from_file"></a>

#### from\_file

```python
def from_file(
        analysis_id: int = 0,
        filename: str = gl.RESOURCES_FOLDERPATH / "T3COConfig.csv") -> Self
```

Generates a Config dictionary from CSV file and calls Config.from_dict.

**Arguments**:

- `filename` _str_ - Path of input T3CO Config file.
- `analysis_id` _int_ - Analysis ID selections.
  

**Returns**:

- `Self` - Config instance containing all values from T3CO Config CSV file.

<a id="t3co/input_data/config.Config.from_dict"></a>

#### from\_dict

```python
def from_dict(config_dict: dict) -> Self
```

Generates a Config instance from config_dict.

**Arguments**:

- `config_dict` _dict_ - Dictionary containing fields from T3CO Config input CSV file.
  

**Returns**:

- `Self` - Config instance containing all values from T3CO Config CSV file.

<a id="t3co/input_data/config.Config.validate_analysis_id"></a>

#### validate\_analysis\_id

```python
def validate_analysis_id() -> pd.DataFrame
```

Validates that the correct analysis ID is input.

**Returns**:

- `pd.DataFrame` - DataFrame containing the configuration data for the given analysis ID.
  

**Raises**:

- `Exception` - If analysis_id is not found or config file does not exist.

<a id="t3co/input_data/config.Config.check_drivecycles_and_create_selections"></a>

#### check\_drivecycles\_and\_create\_selections

```python
def check_drivecycles_and_create_selections() -> None
```

Checks if the config.drive_cycle input is a file or a folder. If a folder is provided, creates a list of all selections for each drive cycle in the folder as config.dc_files.

<a id="t3co/input_data/config.Config.read_auxiliary_files"></a>

#### read\_auxiliary\_files

```python
def read_auxiliary_files() -> None
```

Reads auxiliary files such as fuel prices and residual rates.

<a id="t3co/input_data/config.Config.delete_dataframes"></a>

#### delete\_dataframes

```python
def delete_dataframes() -> None
```

Deletes DataFrame attributes from the Config instance.

