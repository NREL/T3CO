from pathlib import Path

import pandas as pd
import pytest

from t3co.cli.sweep import (
    create_results_filepath,
    export_results_to_csv,
    generate_ledger,
    load_vehicle_scenario_energy,
    run_t3co,
)
from t3co.constants import Global as gl
from t3co.energy_models.energy import Energy
from t3co.input_data.config import Config
from t3co.input_data.scenario import Scenario
from t3co.input_data.toggles import Toggles
from t3co.input_data.vehicle import Vehicle


@pytest.fixture
def vehicle(config):
    vehicle = Vehicle().from_config(selection=1, config=config)
    vehicle.set_veh_kg()
    return vehicle


@pytest.fixture
def toggles():
    return Toggles(
        msrp=True,
        purchase_tax=True,
        purchasing_downpayment=True,
        mark_up=True,
        residual_cost=True,
        fuel_cost=True,
        maintenance_oper_cost=True,
        insurance_cost=True,
        purchasing_cost=True,
        fueling_dwell_labor=True,
        payload_oppy_cost=True,
        fueling_dwell_oppy_cost=True,
        mr_downtime_oppy_cost=True,
        run_fastsim=False,
    )


@pytest.fixture
def scenario(config, toggles):
    scenario = Scenario.from_file(selection=1)

    scenario.fuel_prices_df = pd.DataFrame(
        {
            "Fuel": ["dieselDolPerGal"],
            "Region": ["US"],
            "2020": [0.1],
            "2021": [0.1],
            "2022": [0.1],
            "2023": [0.1],
            "2024": [0.1],
            "2025": [0.1],
            "2026": [0.1],
            "2027": [0.1],
            "2028": [0.1],
            "2029": [0.1],
        }
    )
    scenario.region = "US"
    scenario.vehicle_class = "class8"
    # scenario.override_from_config(config=config)
    scenario.vehicle_life_yr = 4
    scenario.fuel_prices_df.set_index("Fuel", inplace=True)
    scenario.cost_toggles = toggles
    return scenario


@pytest.fixture
def energy(scenario, config):
    energy = Energy(mpgge=6.03, primary_fuel_range_mi=2035.70)
    return energy


@pytest.fixture
def config(toggles):
    config = Config()
    config.from_file()
    config.check_drivecycles_and_create_selections()
    config.read_auxiliary_files()
    config.vehicle_file = gl.RESOURCES_FOLDERPATH / config.vehicle_file
    config.scenario_file = gl.RESOURCES_FOLDERPATH / config.scenario_file
    config.eng_eff_imp_curves = gl.RESOURCES_FOLDERPATH / config.eng_eff_imp_curves
    config.lw_imp_curves = gl.RESOURCES_FOLDERPATH / config.lw_imp_curves
    config.aero_drag_imp_curves = gl.RESOURCES_FOLDERPATH / config.aero_drag_imp_curves
    config.resfile_suffix = "_test_suffix"
    config.selections_list = [1]
    config.cost_toggles = toggles
    return config


def test_load_vehicle_scenario_energy(mocker, config, vehicle, scenario, energy):
    mocker.patch("t3co.input_data.vehicle.Vehicle.from_config", return_value=vehicle)
    mocker.patch("t3co.input_data.scenario.Scenario.from_file", return_value=scenario)
    mocker.patch(
        "t3co.energy_models.energy.Energy.run_fastsim_model", return_value=None
    )

    veh, scen, en = load_vehicle_scenario_energy(
        selection="1", config=config, vehicle=vehicle, scenario=scenario, energy=energy
    )
    assert veh == vehicle
    assert scen == scenario
    assert en.mpgge == pytest.approx(6.03, 0.01)
    assert en.primary_fuel_range_mi == pytest.approx(2035.70, 0.01)


def test_generate_ledger(mocker, config, vehicle, scenario, energy):
    mocker.patch(
        "t3co.cli.sweep.load_vehicle_scenario_energy",
        return_value=(vehicle, scenario, energy),
    )
    mocker.patch("t3co.tco.ledger.Ledger.to_dict", return_value={"key": "value"})

    result = generate_ledger(selection=1, config=config)
    assert result == {"key": "value"}


def test_create_results_filepath(config):
    result_filepath = create_results_filepath(config=config)
    assert result_filepath.name.startswith("results_")
    assert result_filepath.name.endswith("_test_suffix.csv")


def test_export_results_to_csv(config):
    reports_list = [{"selection": 1, "value": 100}, {"selection": 2, "value": 200}]
    output_path, reports_df = export_results_to_csv(
        reports_list=reports_list,
        config=config,
        return_filepath=True,
        return_df=True,
        sort_values=True,
    )
    assert output_path.exists()
    assert isinstance(reports_df, pd.DataFrame)
    assert reports_df.iloc[0]["selection"] == 1
    assert reports_df.iloc[1]["selection"] == 2
    assert reports_df.iloc[0]["value"] == pytest.approx(100, 0.01)
    assert reports_df.iloc[1]["value"] == pytest.approx(200, 0.01)


def test_run_t3co(mocker, config):
    mocker.patch(
        "t3co.cli.sweep.generate_ledger", return_value={"selection": 1, "value": 100}
    )
    mocker.patch(
        "t3co.cli.sweep.export_results_to_csv",
        return_value=(
            Path("results.csv"),
            pd.DataFrame([{"selection": 1, "value": 100}]),
        ),
    )
    mocker.patch("builtins.print")

    run_t3co(config=config, save_results=True)
    assert mocker.patch("t3co.cli.sweep.generate_ledger").called != None
    assert mocker.patch("t3co.cli.sweep.export_results_to_csv").called != None
