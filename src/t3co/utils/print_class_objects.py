import json
from collections import OrderedDict
from pathlib import Path
from typing import Any, List, Union

import pandas as pd

import t3co.constants.Global as gl


def obj_to_string(obj: Union[object, List[object]], indent: str = "    ") -> str:
    """
    Converts an object or list of objects to a formatted string representation.

    Args:
        obj (Union[object, List[object]]): The object or list of objects to convert.
        indent (str, optional): Indentation string for nested objects. Defaults to "    ".

    Returns:
        str: Formatted string representation of the object.
    """
    if isinstance(obj, list):
        return (
            "[\n"
            + ",\n".join(
                indent + obj_to_string(item, indent + "    ")
                if hasattr(item, "__dict__")
                else indent + str(item)
                for item in obj
            )
            + "\n"
            + indent[:-4]
            + "]"
        )

    elif hasattr(obj, "__dict__"):
        return f"{obj.__class__.__name__}\n" + "\n".join(
            f"{indent}{attr} = {obj_to_string(value, indent + '    ')}"
            for attr, value in sorted(vars(obj).items())
        )

    return str(obj)


def handle_nan(
    obj: Union[float, dict, list, Any],
) -> Union[None, dict, list, float, Any]:
    """
    Replaces NaN values in an object with None.

    Args:
        obj (Union[float, dict, list, Any]): The object to process.

    Returns:
        Union[None, dict, list, float, Any]: The processed object with NaN values replaced by None.
    """
    if isinstance(obj, float) and pd.isna(obj):
        return None
    elif isinstance(obj, dict):
        return {k: handle_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [handle_nan(v) for v in obj]
    return obj


def custom_default(obj: Any) -> Union[None, dict, str]:
    """
    Custom default function for JSON serialization.

    Args:
        obj (Any): The object to serialize.

    Returns:
        Union[None, dict, str]: The serialized object.
    """
    if isinstance(obj, float) and pd.isna(obj):
        return None
    elif isinstance(obj, Path):
        return str(obj)
    elif isinstance(obj, pd.DataFrame):
        return None
    elif hasattr(obj, "__dict__"):
        return vars(obj)
    return str(obj)


def to_flat_dict(
    obj: object, include_prefix: bool = True, prefix: str = "", delimiter: str = "_"
) -> dict:
    """
    Flattens a nested object into a dictionary while preserving the order of declared attributes.

    Args:
        obj (object): The object to flatten.
        include_prefix (bool, optional): Whether to include the prefix in the keys. Defaults to True.
        prefix (str, optional): The prefix for the keys. Defaults to "".
        delimiter (str, optional): The delimiter for the keys. Defaults to "_".

    Returns:
        dict: The flattened dictionary.
    """
    flat_dict = {}

    def flatten(item, current_prefix):
        """Recursively flattens attributes."""
        if isinstance(item, dict):
            for key, value in item.items():
                new_key = f"{current_prefix}{delimiter}{key}" if current_prefix else key
                flatten(value, (new_key if include_prefix else key))
        elif hasattr(item, "__dict__"):
            flatten(vars(item), current_prefix)
        else:
            flat_dict[current_prefix] = item

    if hasattr(obj, "__dict__"):
        # Extract attributes in the order they were declared
        cls = obj.__class__
        declared_attributes = list(getattr(cls, "__annotations__", {}).keys())
        instance_attributes = list(vars(obj).keys())

        # Maintain order: declared first, then dynamically assigned attributes
        ordered_fields = OrderedDict.fromkeys(declared_attributes + instance_attributes)

        # Create ordered dictionary of attributes
        ordered_obj = OrderedDict(
            (field, getattr(obj, field, None)) for field in ordered_fields
        )

        # Flatten the object
        flatten(ordered_obj, prefix if include_prefix else "")
    else:
        print(f'it is dict: {include_prefix}')
        flatten(obj, current_prefix= (prefix if include_prefix else ""))

    return flat_dict


def remove_df_attrs(obj: object) -> None:
    """
    Removes attributes from an object if they are DataFrame instances.

    Args:
        obj (object): The object to process.
    """
    for attr in list(vars(obj).keys()):  # Use `list()` to avoid modification issues
        if isinstance(getattr(obj, attr), pd.DataFrame):
            delattr(obj, attr)


def get_path_object(filename: str) -> Path:
    return (
        Path(filename).resolve(strict=True)
        if Path(filename).is_absolute()
        else gl.RESOURCES_FOLDERPATH / filename
    )
