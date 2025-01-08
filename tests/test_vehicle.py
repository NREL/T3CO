import pandas as pd
import pytest
from pathlib import Path
from t3co.input_data.config import Config
from t3co.input_data.vehicle import Vehicle

@pytest.fixture
def config():
    # Create a mock Config object
    config = Config()
    config.selections_list = [1,1]
    config.vehicle_file = Path(__file__).parent / "mock_vehicle_db.csv"
    return config

@pytest.fixture
def mock_vehicle_db(tmp_path):
    # Create a mock vehicle database CSV file
    data = """selection,veh_pt_type,fc_eff_type,fc_max_kw,fs_kwh,mc_max_kw,ess_max_kwh,chg_eff,glider_kg,trans_kg,cargo_kg,fc_base_kg,fs_kwh_per_kg,fc_kw_per_kg,mc_pe_kg_per_kw,mc_pe_base_kg,ess_kg_per_kwh,ess_base_kg,veh_override_kg
1,BEV,Type1,100,50,200,75,0.9,1000,500,200,300,0.5,0.1,0.05,50,0.2,100,0
2,HEV,Type2,150,60,250,80,0.85,1100,550,250,350,0.6,0.15,0.06,55,0.25,110,0
"""
    mock_file = tmp_path / "mock_vehicle_db.csv"
    mock_file.write_text(data)
    return mock_file

def test_from_config(config, mock_vehicle_db):
    config.vehicle_file = mock_vehicle_db
    vehicle = Vehicle.from_config(selection=1, config=config)
    assert vehicle.selection == 1
    assert vehicle.veh_pt_type == "BEV"
    assert vehicle.fc_eff_type == "Type1"
    assert vehicle.fc_max_kw == 100
    assert vehicle.fs_kwh == 50
    assert vehicle.mc_max_kw == 200
    assert vehicle.ess_max_kwh == 75
    assert vehicle.chg_eff == 0.9
    assert vehicle.glider_kg == 1000
    assert vehicle.trans_kg == 500
    assert vehicle.cargo_kg == 200
    assert vehicle.fc_base_kg == 300
    assert vehicle.fs_kwh_per_kg == 0.5
    assert vehicle.fc_kw_per_kg == 0.1
    assert vehicle.mc_pe_kg_per_kw == 0.05
    assert vehicle.mc_pe_base_kg == 50
    assert vehicle.ess_kg_per_kwh == 0.2
    assert vehicle.ess_base_kg == 100
    assert vehicle.veh_override_kg == 0

def test_set_veh_kg(config, mock_vehicle_db):
    config.vehicle_file = mock_vehicle_db
    vehicle = Vehicle.from_config(selection=1, config=config)
    vehicle.set_veh_kg()
    expected_veh_kg = (
        vehicle.glider_kg
        + vehicle.trans_kg
        + vehicle.cargo_kg
        + (vehicle.fs_kwh / vehicle.fs_kwh_per_kg if vehicle.fs_kwh else 0)
        + (vehicle.fc_base_kg + vehicle.fc_kw_per_kg / vehicle.fc_max_kw if vehicle.fc_max_kw else 0)
        + (vehicle.mc_pe_base_kg + vehicle.mc_pe_kg_per_kw / vehicle.mc_max_kw if vehicle.mc_max_kw else 0)
        + (vehicle.ess_base_kg + vehicle.ess_kg_per_kwh / vehicle.ess_max_kwh if vehicle.ess_max_kwh else 0)
    )
    assert vehicle.veh_kg == expected_veh_kg

def test_delete_dataframes(config, mock_vehicle_db):
    config.vehicle_file = mock_vehicle_db
    vehicle = Vehicle.from_config(selection=1, config=config)
    vehicle.df_attr = pd.DataFrame({"A": [1, 2, 3]})
    vehicle.delete_dataframes()
    assert not hasattr(vehicle, "df_attr")