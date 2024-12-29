import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self
import numpy as np
import pandas as pd
import t3co.constants.Global as gl

@dataclass
class Config:
    """
    This class reads T3COConfig.csv file containing analysis attributes like vehicle and scenario paths, TCO_method, and scenario attribute overrides.

    """

    analysis_id: int = 0
    analysis_name: str = ""
    vehicle_file: str = ""
    scenario_file: str = ""
    dst_dir: str = ""
    resfile_suffix: str = None
    write_tsv: bool = False
    selections: str = ""
    # selections: list = field(default_factory=list)
    vehicle_life_yr: float = 0
    drive_cycle: str = None
    # Fueling
    ess_max_charging_power_kw: float = 0
    fs_fueling_rate_kg_per_min: float = 0
    fs_fueling_rate_gasoline_gpm: float = 0
    fs_fueling_rate_diesel_gpm: float = 0

    insurance_rates_file: str = ""
    residual_rates_file: str = ""
    fuel_prices_file: str = ""

    TCO_method: str = "DIRECT"

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
    objective_phev_minimize_fuel_use: bool = False

    # Opportunity Cost
    activate_tco_payload_cap_cost_multiplier: bool = False
    activate_tco_fueling_dwell_time_cost: bool = False
    fdt_frac_full_charge_bounds: list = field(default_factory=list)
    activate_mr_downtime_cost: bool = False

    def from_file(self, filename: str, analysis_id: int) -> Self:
        """
        This method generates a Config dictionary from CSV file and calls Config.from_dict

        Args:
            filename (str): path of input T3CO Config file
            analysis_id (int): analysis ID selections

        Returns:
            Self.from_dict: method that gets Config instance from config_dict
        """
        filename = str(filename)

        config_df = (
            pd.read_csv(filename, index_col="analysis_id")
            .loc[analysis_id]
            .replace({np.nan: None})
        )
        config_dict = config_df.to_dict()

        return self.from_dict(config_dict=config_dict)

    def from_dict(self, config_dict: dict) -> Self:
        """
        This method generates a Config instance from config_dict

        Args:
            config_dict (dict): dictionary containing fields from T3CO Config input CSV file

        Returns:
            Self: Config instance containining all values from T3CO Config CSV file
        """
        try:
            config_dict["selections"] = ast.literal_eval(config_dict["selections"])
        except:  # noqa: E722
            config_dict["selections"] = int(config_dict["selections"])
        self.__dict__.update(config_dict)

    def validate_analysis_id(self, filename: str, analysis_id: int = 0) -> Self:
        """
        This method validates that correct analysis id is input

        Args:
            filename (str): T3CO Config input CSV file path

        Raises:
            Exception: Error if analysis_id not found
        """
        filename = str(filename)
        config_df = pd.read_csv(filename)
        print(f"Try these analysis IDs instead: {list(config_df['analysis_id'])}")
        assert (
            analysis_id in config_df["analysis_id"]
        ), "Given analysis_id not in config input file"
        raise Exception

    def check_drivecycles_and_create_selections(self, config_file: str | Path):
        """
        This method checks if the config.drive_cycle input is a file or a folder. If a folder is provided, then it creates a list of all selections for each drivecycle in the folders as config.dc_files

        Args:
            config_file (str|Path): File path of config file
        """
        self.dc_files = None
        try:
            if Path(self.drive_cycle).is_absolute():
                dc_folder_path = Path(self.drive_cycle)
            else:
                dc_folder_path = Path(config_file).parent / self.drive_cycle
            if not dc_folder_path.exists():
                try:
                    dc_folder_path = gl.OPTIMIZATION_DRIVE_CYCLES / self.drive_cycle
                except:
                    print(f"Drivecycle folder does not exist: {dc_folder_path}")

            if Path(dc_folder_path).is_dir():
                self.dc_files = [p.absolute() for p in dc_folder_path.rglob("*.csv")]
                selections_list = list(self.selections)
                self.selections = []
                for selection in selections_list:
                    for i in range(len(self.dc_files)):
                        self.selections.append(str(selection) + "_" + str(i).zfill(3))
            else:
                self.dc_files = None
        except:
            Exception
