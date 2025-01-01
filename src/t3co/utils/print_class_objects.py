import json
from pathlib import Path
from typing import List


def obj_to_string(obj, extra="    "):
    if isinstance(obj, list) or isinstance(obj, List):  # Check if the object is a list
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
        )  # Match the indentation level

    elif hasattr(obj, "__dict__"):  # Check if the object has __dict__ attribute
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
    else:  # For other data types
        return str(obj)


def handle_nan(obj):
    if isinstance(obj, float) and obj != obj:  # Check for NaN
        return None
    elif isinstance(obj, dict):
        return {k: handle_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [handle_nan(v) for v in obj]
    else:
        return obj


def custom_default(obj):
    if (isinstance(obj, float)) and obj != obj:
        return None  
    elif (isinstance(obj, Path)):
        return str(obj)
    else:
        return obj.__dict__


def to_flat_dict(obj, include_predix=True, prefix="", delimiter="_"):
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
            flat_dict[current_prefix[:-1]] = item  # Remove the trailing dot

    flatten(json.loads(json.dumps(obj, default=custom_default)), prefix)

    return flat_dict
