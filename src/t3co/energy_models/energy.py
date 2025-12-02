from dataclasses import dataclass
from pathlib import Path
from typing import Union

try:
    from t3co.energy_models.fastsim_model.fastsim_wrapper import RunFastsim

    fastsim_installed = True
except ImportError:
    fastsim_installed = False
except AttributeError:
    fastsim_installed = False

from t3co.constants import Global as gl
from t3co.input_data.scenario import Scenario


@dataclass
class Energy:
    mpgge: float = None
    primary_fuel_range_mi: float = None

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the Energy class.
        """
        instance = super(Energy, cls).__new__(cls)
        return instance

    def __init__(self, mpgge: float = None, primary_fuel_range_mi: float = None):
        """
        Initializes the Energy instance.

        Args:
            mpgge (float, optional): Miles per gallon gasoline equivalent. Defaults to None.
            primary_fuel_range_mi (float, optional): Primary fuel range in miles. Defaults to None.
        """
        if mpgge and primary_fuel_range_mi:
            self.mpgge = mpgge
            self.primary_fuel_range_mi = primary_fuel_range_mi

    def run_fastsim_model(
        self,
        veh_no: int,
        scenario: Scenario,
        vehicle_file: Union[str, Path] = gl.RESOURCES_FOLDERPATH
        / "inputs"
        / "Demo_FY22_vehicle_model_assumptions.csv",
    ) -> None:
        """
        Runs the FASTSim model to calculate mpgge and primary fuel range.

        Args:
            veh_no (int): Vehicle selection number.
            scenario (Scenario): Scenario instance containing configuration data.
            vehicle_file (Union[str, Path], optional): Vehicle model assumptions input CSV file path. Defaults to gl.RESOURCES_FOLDERPATH / "inputs" / "Demo_FY22_vehicle_model_assumptions.csv".
        """
        if not fastsim_installed:
            raise ImportError(
                "FASTSim is not installed or could not be imported. Cannot run FASTSim model."
            )

        fastsim_run = RunFastsim(
            veh_no=veh_no,
            scenario=scenario,
            veh_input_path=vehicle_file,
        )
        self.mpgge = fastsim_run.mpgge
        self.primary_fuel_range_mi = fastsim_run.range_mi
