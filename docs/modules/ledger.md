# Table of Contents

* [t3co/tco/ledger](#t3co/tco/ledger)
  * [Ledger](#t3co/tco/ledger.Ledger)
    * [\_\_new\_\_](#t3co/tco/ledger.Ledger.__new__)
    * [\_\_init\_\_](#t3co/tco/ledger.Ledger.__init__)
    * [set\_discounted\_costs](#t3co/tco/ledger.Ledger.set_discounted_costs)
    * [set\_discounted\_tco](#t3co/tco/ledger.Ledger.set_discounted_tco)
    * [set\_cost\_components](#t3co/tco/ledger.Ledger.set_cost_components)
    * [to\_dict](#t3co/tco/ledger.Ledger.to_dict)
    * [to\_json](#t3co/tco/ledger.Ledger.to_json)
    * [to\_df](#t3co/tco/ledger.Ledger.to_df)
    * [to\_csv](#t3co/tco/ledger.Ledger.to_csv)
    * [\_\_str\_\_](#t3co/tco/ledger.Ledger.__str__)

<a id="t3co/tco/ledger"></a>

# t3co/tco/ledger

<a id="t3co/tco/ledger.Ledger"></a>

## Ledger Objects

```python
class Ledger()
```

<a id="t3co/tco/ledger.Ledger.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the Ledger class.

<a id="t3co/tco/ledger.Ledger.__init__"></a>

#### \_\_init\_\_

```python
def __init__(vehicle: Vehicle,
             scenario: Scenario,
             energy: Energy = None,
             config: Config = None)
```

Initializes the Ledger instance.

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance.
- `energy` _Energy, optional_ - The energy instance. Defaults to None.
- `config` _Config, optional_ - The configuration instance. Defaults to None.

<a id="t3co/tco/ledger.Ledger.set_discounted_costs"></a>

#### set\_discounted\_costs

```python
def set_discounted_costs()
```

Sets the discounted cost components for the Ledger instance.

<a id="t3co/tco/ledger.Ledger.set_discounted_tco"></a>

#### set\_discounted\_tco

```python
def set_discounted_tco()
```

Sets the discounted TCO for the Ledger instance.

<a id="t3co/tco/ledger.Ledger.set_cost_components"></a>

#### set\_cost\_components

```python
def set_cost_components()
```

Sets the cost components for the Ledger instance.

<a id="t3co/tco/ledger.Ledger.to_dict"></a>

#### to\_dict

```python
def to_dict(include_prefix: bool = True, flatten: bool = True) -> dict
```

Exports the Ledger instance to a dictionary.

**Arguments**:

- `include_prefix` _bool, optional_ - If True, exported column names contain the T3CO submodule names as prefix. Defaults to True.
- `flatten` _bool, optional_ - If True, the nested dict output flattens to a single dictionary. Defaults to True.
  

**Returns**:

- `dict` - The Ledger instance as a dictionary.

<a id="t3co/tco/ledger.Ledger.to_json"></a>

#### to\_json

```python
def to_json(filepath: Union[str, Path],
            include_prefix: bool = True,
            flatten: bool = True) -> None
```

Saves the Ledger instance to a JSON file.

**Arguments**:

- `filepath` _Union[str, Path]_ - The file path where the JSON will be saved.
- `include_prefix` _bool, optional_ - If True, exported column names contain the T3CO submodule names as prefix. Defaults to True.
- `flatten` _bool, optional_ - If True, the nested dict output flattens to a single dictionary. Defaults to True.

<a id="t3co/tco/ledger.Ledger.to_df"></a>

#### to\_df

```python
def to_df() -> pd.DataFrame
```

Converts the Ledger instance to a DataFrame.

**Returns**:

- `pd.DataFrame` - The Ledger instance as a DataFrame.

<a id="t3co/tco/ledger.Ledger.to_csv"></a>

#### to\_csv

```python
def to_csv(filepath: Union[str, Path]) -> None
```

Saves the Ledger instance to a CSV file.

**Arguments**:

- `filepath` _Union[str, Path]_ - The file path where the CSV will be saved.

<a id="t3co/tco/ledger.Ledger.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns a string representation of the Ledger instance.

**Returns**:

- `str` - String representation of the Ledger instance.

