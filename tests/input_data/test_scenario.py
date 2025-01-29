import pytest
from t3co.input_data.scenario import Scenario
from t3co.input_data.config import Config
from pathlib import Path
import pandas as pd

@pytest.fixture
def config():
    # Create a mock Config object
    config = Config()
    config.scenario_file = Path(__file__).parent / "mock_scenario_db.csv"
    return config

@pytest.fixture
def mock_scenario_db(tmp_path):
    # Create a mock scenario database CSV file
    data = """selection,scenario_name,drive_cycle,use_config,vmt,constant_trip_distance_mi,vehicle_life_yr,discount_rate_pct_per_yr,ess_max_charging_power_kw,ess_cost_dol_per_kwh,ess_base_cost_dol,shifts_per_year,mr_unplanned_downtime_hr_per_mi,maint_oper_cost_dol_per_mi,depreciation_rates_pct_per_yr
1,Scenario1,cycle1,True,"[10000, 9000, 8000]",50,10,0.05,100,300,400,"[2, 2, 2]","[0.1, 0.1, 0.1]","[0.05, 0.05, 0.05]","[0.09, 0.09, 0.09]"
2,Scenario2,cycle2,False,"[20000, 18000, 16000]",60,12,0.06,110,310,410,"[3, 3, 3]","[0.2, 0.2, 0.2]","[0.1, 0.1, 0.1]","[0.09, 0.09, 0.09]"
"""
    mock_file = tmp_path / "mock_scenario_db.csv"
    mock_file.write_text(data)
    return mock_file

def test_scenario_initialization():
    scenario = Scenario(
        selection=1,
        scenario_name="Test Scenario",
        drive_cycle="cycle1",
        use_config=True,
        vmt=[10000, 9000, 8000],
        constant_trip_distance_mi=50,
        vehicle_life_yr=3,
        discount_rate_pct_per_yr=0.05,
        ess_max_charging_power_kw=100,
        ess_cost_dol_per_kwh=300,
        ess_base_cost_dol=400,
        shifts_per_year=[2, 2, 2],
        depreciation_rates_pct_per_yr=[0.09]*3,
        mr_unplanned_downtime_hr_per_mi=[0.1, 0.1, 0.1],
        maint_oper_cost_dol_per_mi=[0.05, 0.05, 0.05],
    )
    assert scenario.selection == 1
    assert scenario.scenario_name == "Test Scenario"
    assert scenario.drive_cycle == "cycle1"
    assert scenario.use_config is True
    assert scenario.vmt == [10000, 9000, 8000]
    assert scenario.constant_trip_distance_mi == 50
    assert scenario.vehicle_life_yr == 3
    assert scenario.discount_rate_pct_per_yr == 0.05
    assert scenario.ess_max_charging_power_kw == 100
    assert scenario.ess_cost_dol_per_kwh == 300
    assert scenario.ess_base_cost_dol == 400
    assert scenario.shifts_per_year == [2, 2, 2]
    assert scenario.mr_unplanned_downtime_hr_per_mi == [0.1, 0.1, 0.1,]
    assert scenario.maint_oper_cost_dol_per_mi == [0.05, 0.05, 0.05]

def test_scenario_from_file(config, mock_scenario_db):
    config.scenario_file = mock_scenario_db
    scenario = Scenario.from_file(selection=1, scenario_file=config.scenario_file)
    assert scenario.selection == 1
    assert scenario.scenario_name == "Scenario1"
    assert scenario.drive_cycle == "cycle1"
    assert scenario.use_config is True
    assert scenario.vmt == [10000, 9000, 8000]
    assert scenario.constant_trip_distance_mi == 50
    assert scenario.vehicle_life_yr == 10
    assert scenario.discount_rate_pct_per_yr == 0.05
    assert scenario.ess_max_charging_power_kw == 100
    assert scenario.ess_cost_dol_per_kwh == 300
    assert scenario.ess_base_cost_dol == 400
    assert scenario.shifts_per_year == [2, 2, 2]
    assert scenario.mr_unplanned_downtime_hr_per_mi == [0.1, 0.1, 0.1]
    assert scenario.maint_oper_cost_dol_per_mi == [0.05, 0.05, 0.05]

def test_scenario_override_from_config(config, mock_scenario_db):
    config.scenario_file = mock_scenario_db
    scenario = Scenario.from_file(selection=1, scenario_file=config.scenario_file)
    scenario.override_from_config(config=config)
    assert scenario.vehicle_life_yr == config.vehicle_life_yr
    assert scenario.fs_fueling_rate_kg_per_min == config.fs_fueling_rate_kg_per_min

def test_get_discounted_value():
    scenario = Scenario(discount_rate_pct_per_yr=0.05)
    discounted_value = scenario.get_discounted_value(value=1000, year_number=2)
    assert discounted_value == pytest.approx(907.03, 0.01)

def test_delete_dataframes():
    scenario = Scenario()
    scenario.df_attr = pd.DataFrame({"A": [1, 2, 3]})
    scenario.delete_dataframes()
    assert not hasattr(scenario, "df_attr")