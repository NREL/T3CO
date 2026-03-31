# Table of Contents

* [t3co.cli.sweep](#t3co.cli.sweep)
  * [load\_vehicle\_scenario\_energy](#t3co.cli.sweep.load_vehicle_scenario_energy)
  * [generate\_ledger](#t3co.cli.sweep.generate_ledger)
  * [create\_results\_filepath](#t3co.cli.sweep.create_results_filepath)
  * [export\_results\_to\_csv](#t3co.cli.sweep.export_results_to_csv)
  * [run\_t3co](#t3co.cli.sweep.run_t3co)

<a id="t3co.cli.sweep"></a>

# t3co.cli.sweep

<a id="t3co.cli.sweep.load_vehicle_scenario_energy"></a>

#### load\_vehicle\_scenario\_energy

```python
def load_vehicle_scenario_energy(
        selection: Union[int, str],
        config: Config,
        vehicle: Vehicle = None,
        scenario: Scenario = None,
        energy: Energy = None) -> Tuple[Vehicle, Scenario, Energy]
```

Loads the vehicle, scenario, and energy models based on the selection and config.

**Arguments**:

- `selection` _Union[int, str]_ - The selection index or string.
- `config` _Config_ - The configuration instance.
  

**Returns**:

  Tuple[Vehicle, Scenario, Energy]: The vehicle, scenario, and energy models.

<a id="t3co.cli.sweep.generate_ledger"></a>

#### generate\_ledger

```python
def generate_ledger(selection: int, config: Config) -> Dict
```

Generates the ledger for the given selection and config.

**Arguments**:

- `selection` _int_ - The selection index.
- `config` _Config_ - The configuration instance.
  

**Returns**:

- `Dict` - The ledger as a dictionary.

<a id="t3co.cli.sweep.create_results_filepath"></a>

#### create\_results\_filepath

```python
def create_results_filepath(config: Config) -> Path
```

Creates the results file path based on the config.

**Arguments**:

- `config` _Config_ - The configuration instance.
  

**Returns**:

- `Path` - The path to the results file.

<a id="t3co.cli.sweep.export_results_to_csv"></a>

#### export\_results\_to\_csv

```python
def export_results_to_csv(
    reports_list: List[Dict],
    config: Config,
    output_path: Union[str, Path] = None,
    return_filepath: bool = True,
    return_df: bool = False,
    sort_values: bool = False
) -> Tuple[Union[Path, None], Union[pd.DataFrame, None]]
```

Exports the results to a CSV file.

**Arguments**:

- `reports_list` _List[Dict]_ - The list of reports.
- `config` _Config_ - The configuration instance.
- `output_path` _Union[str, Path], optional_ - The output path for the CSV file. Defaults to None.
- `return_filepath` _bool, optional_ - Whether to return the file path. Defaults to True.
- `return_df` _bool, optional_ - Whether to return the DataFrame. Defaults to False.
- `sort_values` _bool, optional_ - Whether to sort the values by selection. Defaults to False.
  

**Returns**:

  Tuple[Union[Path, None], Union[pd.DataFrame, None]]: The output path and DataFrame if specified.

<a id="t3co.cli.sweep.run_t3co"></a>

#### run\_t3co

```python
def run_t3co(config: Config, save_results: bool = True) -> None
```

Runs the T3CO analysis.

**Arguments**:

- `config` _Config_ - The configuration instance.
- `save_results` _bool, optional_ - Whether to save the results. Defaults to True.

