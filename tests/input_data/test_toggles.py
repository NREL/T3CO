import json
import pytest
from pathlib import Path
from t3co.input_data.toggles import Toggles
from t3co.constants import Global as gl

@pytest.fixture
def mock_toggles_file(tmp_path):
    # Create a mock toggles JSON file
    data = {
        "msrp": True,
        "purchase_tax": True,
        "purchasing_downpayment": True,
        "mark_up": True,
        "residual_cost": True,
        "fuel_cost": True,
        "maintenance_oper_cost": True,
        "insurance_cost": True,
        "purchasing_cost": True,
        "fueling_dwell_labor": True,
        "payload_oppy_cost": True,
        "fueling_dwell_oppy_cost": True,
        "mr_downtime_oppy_cost": True,
        "run_fastsim": True
    }
    mock_file = tmp_path / "mock_toggles.json"
    mock_file.write_text(json.dumps(data))
    return mock_file

def test_from_json(mock_toggles_file):
    toggles = Toggles.from_json(cost_toggles_file=mock_toggles_file)
    assert toggles.msrp is True
    assert toggles.purchase_tax is True
    assert toggles.purchasing_downpayment is True
    assert toggles.mark_up is True
    assert toggles.residual_cost is True
    assert toggles.fuel_cost is True
    assert toggles.maintenance_oper_cost is True
    assert toggles.insurance_cost is True
    assert toggles.purchasing_cost is True
    assert toggles.fueling_dwell_labor is True
    assert toggles.payload_oppy_cost is True
    assert toggles.fueling_dwell_oppy_cost is True
    assert toggles.mr_downtime_oppy_cost is True
    assert toggles.run_fastsim is True

def test_default_values():
    toggles = Toggles()
    assert toggles.msrp is True
    assert toggles.purchase_tax is True
    assert toggles.purchasing_downpayment is True
    assert toggles.mark_up is True
    assert toggles.residual_cost is True
    assert toggles.fuel_cost is True
    assert toggles.maintenance_oper_cost is True
    assert toggles.insurance_cost is True
    assert toggles.purchasing_cost is True
    assert toggles.fueling_dwell_labor is True
    assert toggles.payload_oppy_cost is True
    assert toggles.fueling_dwell_oppy_cost is True
    assert toggles.mr_downtime_oppy_cost is True
    assert toggles.run_fastsim is True