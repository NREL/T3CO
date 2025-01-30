import pytest
from pathlib import Path
import pandas as pd
from t3co.utils.print_class_objects import (
    obj_to_string,
    handle_nan,
    custom_default,
    to_flat_dict,
    remove_df_attrs,
)


class SampleClass:
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2


def test_obj_to_string():
    obj = SampleClass(attr1="value1", attr2=123)
    expected_output = (
        "<class 'test_print_class_objects.SampleClass'>\n"
        "    attr1 = value1\n"
        "    attr2 = 123"
    )
    assert obj_to_string(obj) == expected_output

    obj_list = [
        SampleClass(attr1="value1", attr2=123),
        SampleClass(attr1="value2", attr2=456),
    ]
    expected_output_list = (
        "[\n"
        "    <class 'test_print_class_objects.SampleClass'>\n"
        "        attr1 = value1\n"
        "        attr2 = 123,\n"
        "    <class 'test_print_class_objects.SampleClass'>\n"
        "        attr1 = value2\n"
        "        attr2 = 456\n"
        "]"
    )
    assert obj_to_string(obj_list) == expected_output_list


def test_handle_nan():
    assert handle_nan(float("nan")) is None
    assert handle_nan({"key": float("nan")}) == {"key": None}
    assert handle_nan([float("nan")]) == [None]


def test_custom_default():
    assert custom_default(float("nan")) is None
    assert custom_default(Path("/path/to/file")) == "/path/to/file"
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    assert custom_default(df) is None
    obj = SampleClass(attr1="value1", attr2=123)
    assert custom_default(obj) == {"attr1": "value1", "attr2": 123}


def test_to_flat_dict():
    obj = SampleClass(
        attr1="value1", attr2=SampleClass(attr1="nested_value1", attr2=456)
    )
    expected_output = {
        "attr1": "value1",
        "attr2_attr1": "nested_value1",
        "attr2_attr2": 456,
    }
    assert to_flat_dict(obj) == expected_output


def test_remove_df_attrs():
    class SampleClassWithDF:
        def __init__(self):
            self.df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
            self.attr = "value"

    obj = SampleClassWithDF()
    remove_df_attrs(obj)
    assert not hasattr(obj, "df")
    assert obj.attr == "value"
