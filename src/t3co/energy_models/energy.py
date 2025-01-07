from dataclasses import dataclass
from pathlib import Path

import numpy as np
from t3co.energy_models.fastsim_model.fastsim_wrapper import RunFastsim
from t3co.input_data.config import Config
from t3co.input_data.scenario import Scenario
from t3co.constants import Global as gl


@dataclass
class Energy:
    mpgge: float = None
    primary_fuel_range_mi: float = None

    def __init__(self, mpgge: float = None, primary_fuel_range_mi: float = None):
        if mpgge and primary_fuel_range_mi:
            self.mpgge = mpgge
            self.primary_fuel_range_mi = primary_fuel_range_mi

    def run_fastsim_model(
        self,
        veh_no: int,
        scenario: Scenario,
        vehicle_file: str | Path = gl.RESOURCES_FOLDERPATH
        / "inputs"
        / "Demo_FY22_vehicle_model_assumptions.csv",
    ):
        fastsim_run = RunFastsim(
            veh_no=veh_no,
            scenario=scenario,
            veh_input_path=vehicle_file,
        )
        self.mpgge = fastsim_run.mpgge
        self.primary_fuel_range_mi = fastsim_run.range_mi
