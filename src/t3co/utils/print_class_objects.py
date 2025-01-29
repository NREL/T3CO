import json
from pathlib import Path
from typing import List, Union

import pandas as pd


def obj_to_string(obj: Union[object, List[object]], extra: str = "    ") -> str:
    """
    Converts an object or list of objects to a formatted string representation.

    Args:
        obj (Union[object, List[object]]): The object or list of objects to convert.
        extra (str, optional): Indentation string for nested objects. Defaults to "    ".

    Returns:
        str: Formatted string representation of the object.
    """
    if isinstance(obj, list) or isinstance(obj, List):
        return (
            "[\n"
            + ",\n".join(
                extra + obj_to_string(item, extra + "    ")
                if hasattr(item, "__dict__")
                else extra + str(item)
                for item in obj
            )
            + "\n"
            + extra[:-4]
            + "]"
        )

    elif hasattr(obj, "__dict__"):
        return (
            str(obj.__class__)
            + "\n"
            + "\n".join(
                (
                    extra
                    + (
                        str(item)
                        + " = "
                        + obj_to_string(obj.__dict__[item], extra + "    ")
                    )
                )
                for item in sorted(obj.__dict__)
            )
        )
    else:
        return str(obj)


def handle_nan(obj: Union[float, dict, list]) -> Union[None, dict, list, float]:
    """
    Replaces NaN values in an object with None.

    Args:
        obj (Union[float, dict, list]): The object to process.

    Returns:
        Union[None, dict, list, float]: The processed object with NaN values replaced by None.
    """
    if isinstance(obj, float) and obj != obj:
        return None
    elif isinstance(obj, dict):
        return {k: handle_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [handle_nan(v) for v in obj]
    else:
        return obj


def custom_default(obj: object) -> Union[None, dict, str]:
    """
    Custom default function for JSON serialization.

    Args:
        obj (object): The object to serialize.

    Returns:
        Union[None, dict, str]: The serialized object.
    """
    if isinstance(obj, float) and obj != obj:
        return None
    elif isinstance(obj, Path):
        return str(obj)
    elif isinstance(obj, pd.DataFrame):
        return None
    else:
        return obj.__dict__


def to_flat_dict(obj: object, include_predix: bool = True, prefix: str = "", delimiter: str = "_") -> dict:
    """
    Flattens a nested object into a dictionary.

    Args:
        obj (object): The object to flatten.
        include_predix (bool, optional): Whether to include the prefix in the keys. Defaults to True.
        prefix (str, optional): The prefix for the keys. Defaults to "".
        delimiter (str, optional): The delimiter for the keys. Defaults to "_".

    Returns:
        dict: The flattened dictionary.
    """
    flat_dict = {}

    def flatten(item, current_prefix):
        if isinstance(item, dict):
            for key, value in item.items():
                flatten(
                    value,
                    f"{current_prefix}{(key if include_predix else '')}{delimiter}",
                )
        elif hasattr(item, "__dict__"):
            flatten(item.__dict__, current_prefix)
        else:
            flat_dict[current_prefix[:-1]] = item

    flatten(json.loads(json.dumps(obj, default=custom_default)), prefix)

    return flat_dict


def remove_df_attrs(obj: object) -> None:
    """
    Removes DataFrame attributes from an object.

    Args:
        obj (object): The object to process.
    """
    for attr_name in dir(obj):
        if isinstance(getattr(obj, attr_name), pd.DataFrame):
            delattr(obj, attr_name)