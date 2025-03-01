# Table of Contents

* [t3co/input\_data/toggles](#t3co/input_data/toggles)
  * [Toggles](#t3co/input_data/toggles.Toggles)
    * [from\_json](#t3co/input_data/toggles.Toggles.from_json)

<a id="t3co/input_data/toggles"></a>

# t3co/input\_data/toggles

<a id="t3co/input_data/toggles.Toggles"></a>

## Toggles Objects

```python
@dataclass
class Toggles()
```

Class object that contains various toggles for TCO calculations.

<a id="t3co/input_data/toggles.Toggles.from_json"></a>

#### from\_json

```python
@classmethod
def from_json(
    cls,
    cost_toggles_file: Path | str = gl.RESOURCES_FOLDERPATH /
    "cost_toggles.json"
) -> Self
```

Creates a Toggles instance from a JSON file.

**Arguments**:

- `cost_toggles_file` _Union[Path, str]_ - Path to the JSON file containing toggle settings.
  

**Returns**:

- `Toggles` - An instance of the Toggles class.

