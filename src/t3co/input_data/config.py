import ast
from dataclasses import dataclass, field
from pathlib import Path
import sys

from t3co.input_data.toggles import Toggles

try:
    from typing import Self  # Python 3.11+
except ImportError:
    from typing_extensions import Self  # Older versions of Python

from typing import Union
import numpy as np
import pandas as pd
from t3co.constants import Global as gl
from t3co.utils.print_class_objects import get_path_object, remove_df_attrs


@dataclass
class Config:
    analysis_id: int = 0
    analysis_name: str = ""
    vehicle_file: Union[str, Path] = (
        gl.RESOURCES_FOLDERPATH / "inputs" / "Demo_FY22_vehicle_model_assumptions.csv"
    )
    scenario_file: Union[str, Path] = (
        gl.RESOURCES_FOLDERPATH / "inputs" / "Demo_FY22_scenario_assumptions.csv"
    )
    dst_dir: str = ""
    resfile_suffix: str = None
    selections: Union[str, list] = ""
    vehicle_life_yr: float = 0
    drive_cycle: str = None

    # Fueling
    ess_max_charging_power_kw: float = 0
    fs_fueling_rate_kg_per_min: float = 0
    fs_fueling_rate_gasoline_gpm: float = 0
    fs_fueling_rate_diesel_gpm: float = 0

    insurance_rates_file: str = ""
    energy_file: str = None
    fuel_prices_file: str = ""
    plf_weight_dist_file: str = None
    cost_toggles_file: str = gl.RESOURCES_FOLDERPATH / "inputs" / "cost_toggles.json"

    TCO_method: str = gl.DIRECT_TCO_METHOD
    purchasing_method: str = "cash"

    # Optimization
    algorithms: str = ""
    lw_imp_curves: str = ""
    eng_eff_imp_curves: str = ""
    aero_drag_imp_curves: str = ""
    lw_imp_curve_sel: str = ""
    eng_eff_imp_curve_sel: str = ""
    aero_drag_imp_curve_sel: str = ""
    skip_all_opt: bool = True
    constraint_range: bool = False
    constraint_accel: bool = False
    constraint_grade: bool = False
    objective_tco: bool = False
    constraint_c_rate: bool = False
    constraint_trace_miss_dist_percent_on: bool = False

    # Opportunity Cost
    activate_tco_payload_cap_cost_multiplier: bool = False
    activate_tco_fueling_dwell_time_cost: bool = False
    fdt_frac_full_charge_bounds: list = field(default_factory=list)
    activate_mr_downtime_cost: bool = False

    n_processes: int = 9
    parallel: bool = True

    selections_list: list[str] = None
    dc_files: list[str] = None

    vehicle_df: pd.DataFrame = None
    scenario_df: pd.DataFrame = None
    energy_df: pd.DataFrame = None
    fuel_prices_df: pd.DataFrame = None
    config_filename: Union[str, Path] = gl.RESOURCES_FOLDERPATH / "T3COConfig.csv"
    vehicle_db_df: pd.DataFrame = None
    scenario_df: pd.DataFrame = None

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the Config class.
        """
        instance = super(Config, cls).__new__(cls)
        return instance

    def from_csv(
        self,
        analysis_id: int = 0,
        filename: str = gl.RESOURCES_FOLDERPATH / "T3COConfig.csv",
    ) -> Self:
        """
        Generates a Config dictionary from CSV file and calls Config.from_dict.

        Args:
            filename (str): Path of input T3CO Config file.
            analysis_id (int): Analysis ID selections.

        Returns:
            Self: Config instance containing all values from T3CO Config CSV file.
        """
        self.config_filename = Path(filename)
        self.analysis_id = analysis_id
        config_df = self.validate_analysis_id()
        config_dict = config_df.to_dict()

        return self.from_dict(config_dict=config_dict)

    def from_dict(self, config_dict: dict) -> Self:
        """
        Generates a Config instance from config_dict.

        Args:
            config_dict (dict): Dictionary containing fields from T3CO Config input CSV file.

        Returns:
            Self: Config instance containing all values from T3CO Config CSV file.
        """
        try:
            config_dict["selections"] = ast.literal_eval(config_dict["selections"])
        except:
            config_dict["selections"] = int(config_dict["selections"])
        self.__dict__.update(config_dict)

        self.read_vehicle_and_scenario_db_files()
        return self

    def read_vehicle_and_scenario_db_files(self) -> None:
        """
        Reads vehicle and scenario database files into DataFrame attributes.
        """
        if not Path(self.vehicle_file).is_absolute():
            self.vehicle_file = Path(self.config_filename).parent / self.vehicle_file
        if not Path(self.scenario_file).is_absolute():
            self.scenario_file = Path(self.config_filename).parent / self.scenario_file

        self.vehicle_db_df = pd.read_csv(get_path_object(self.vehicle_file))
        self.scenario_df = pd.read_csv(get_path_object(self.scenario_file))

    def validate_analysis_id(self) -> pd.DataFrame:
        """
        Validates that the correct analysis ID is input.

        Returns:
            pd.DataFrame: DataFrame containing the configuration data for the given analysis ID.

        Raises:
            Exception: If analysis_id is not found or config file does not exist.
        """
        try:
            if (
                self.config_filename.exists()
                and self.config_filename.suffix.lower() == ".csv"
            ):
                config_df = pd.read_csv(self.config_filename, index_col="analysis_id")
            else:
                raise FileExistsError

            config_df = config_df.loc[self.analysis_id].replace({np.nan: None})
            return config_df

        except FileExistsError:
            print(f"Config file ({self.config_filename}) does not exist")
            sys.exit(1)

        except:
            print(
                f"T3CO terminated. Analysis ID not available. Try these analysis_id's instead: {config_df.index.to_list()}"
            )
            sys.exit(1)

    def check_drivecycles_and_create_selections(self) -> None:
        """
        Checks if the config.drive_cycle input is a file or a folder. If a folder is provided, creates a list of all selections for each drive cycle in the folder as config.dc_files.
        """
        if self.drive_cycle:
            self.drive_cycle = (
                Path(self.drive_cycle).resolve(strict=True)
                if Path(self.drive_cycle).is_absolute()
                else Path(self.config_filename).parents[0] / self.drive_cycle
            )
            if Path(self.drive_cycle).is_dir():
                self.dc_files = [
                    p.absolute() for p in Path(self.drive_cycle).rglob("*.csv")
                ]
                self.selections_list = []
                for selection in self.selections:
                    for i in range(len(self.dc_files)):
                        self.selections_list.append(
                            str(selection) + "_" + str(i).zfill(4)
                        )

            else:
                self.selections_list = self.selections

        elif self.energy_file:
            self.energy_df = pd.read_csv(get_path_object(self.energy_file))
            self.dc_files = self.energy_df["drive_cycle"].tolist()
            self.selections_list = []
            for selection in self.selections:
                for i in range(len(self.dc_files)):
                    self.selections_list.append(str(selection) + "_" + str(i).zfill(4))
        elif (
            self.selections == -1 or self.selections == [-1]
        ) and self.vehicle_db_df is not None:
            self.selections_list = self.vehicle_db_df["selection"].tolist()
        else:
            self.selections_list = self.selections

    def read_auxiliary_files(self) -> None:
        """
        Reads auxiliary files such as fuel prices and residual rates.
        """

        self.vehicle_df = pd.read_csv(get_path_object(self.vehicle_file))
        self.scenario_df = pd.read_csv(get_path_object(self.scenario_file))
        self.fuel_prices_df = pd.read_csv(get_path_object(self.fuel_prices_file))

        self.fuel_prices_df = self.fuel_prices_df.set_index("Fuel")
        self.cost_toggles = Toggles.from_json(get_path_object(self.cost_toggles_file))

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove unpicklable DataFrames
        keys_to_remove = [
            "vehicle_db_df",
            "scenario_df",
            "energy_df",
            "fuel_prices_df",
        ]
        for key in keys_to_remove:
            if key in state:
                del state[key]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Reload DataFrames
        self.read_vehicle_and_scenario_db_files()
        self.read_auxiliary_files()
        # Reload energy_df if needed
        if self.energy_file:
            self.energy_df = pd.read_csv(get_path_object(self.energy_file))

    def delete_dataframes(self) -> None:
        """
        Deletes DataFrame attributes from the Config instance.
        """
        if self.dc_files:
            delattr(self, "dc_files")
        if self.selections_list:
            delattr(self, "selections_list")
        remove_df_attrs(self)
