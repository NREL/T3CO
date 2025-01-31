# Table of Contents

* [t3co/utils/print\_class\_objects](#t3co/utils/print_class_objects)
  * [obj\_to\_string](#t3co/utils/print_class_objects.obj_to_string)
  * [handle\_nan](#t3co/utils/print_class_objects.handle_nan)
  * [custom\_default](#t3co/utils/print_class_objects.custom_default)
  * [to\_flat\_dict](#t3co/utils/print_class_objects.to_flat_dict)
  * [remove\_df\_attrs](#t3co/utils/print_class_objects.remove_df_attrs)

<a id="t3co/utils/print_class_objects"></a>

# t3co/utils/print\_class\_objects

<a id="t3co/utils/print_class_objects.obj_to_string"></a>

#### obj\_to\_string

```python
def obj_to_string(obj: Union[object, List[object]],
                  extra: str = "    ") -> str
```

Converts an object or list of objects to a formatted string representation.

**Arguments**:

- `obj` _Union[object, List[object]]_ - The object or list of objects to convert.
- `extra` _str, optional_ - Indentation string for nested objects. Defaults to "    ".
  

**Returns**:

- `str` - Formatted string representation of the object.

<a id="t3co/utils/print_class_objects.handle_nan"></a>

#### handle\_nan

```python
def handle_nan(
        obj: Union[float, dict, list]) -> Union[None, dict, list, float]
```

Replaces NaN values in an object with None.

**Arguments**:

- `obj` _Union[float, dict, list]_ - The object to process.
  

**Returns**:

  Union[None, dict, list, float]: The processed object with NaN values replaced by None.

<a id="t3co/utils/print_class_objects.custom_default"></a>

#### custom\_default

```python
def custom_default(obj: object) -> Union[None, dict, str]
```

Custom default function for JSON serialization.

**Arguments**:

- `obj` _object_ - The object to serialize.
  

**Returns**:

  Union[None, dict, str]: The serialized object.

<a id="t3co/utils/print_class_objects.to_flat_dict"></a>

#### to\_flat\_dict

```python
def to_flat_dict(obj: object,
                 include_predix: bool = True,
                 prefix: str = "",
                 delimiter: str = "_") -> dict
```

Flattens a nested object into a dictionary.

**Arguments**:

- `obj` _object_ - The object to flatten.
- `include_predix` _bool, optional_ - Whether to include the prefix in the keys. Defaults to True.
- `prefix` _str, optional_ - The prefix for the keys. Defaults to "".
- `delimiter` _str, optional_ - The delimiter for the keys. Defaults to "_".
  

**Returns**:

- `dict` - The flattened dictionary.

<a id="t3co/utils/print_class_objects.remove_df_attrs"></a>

#### remove\_df\_attrs

```python
def remove_df_attrs(obj: object) -> None
```

Removes DataFrame attributes from an object.

**Arguments**:

- `obj` _object_ - The object to process.

