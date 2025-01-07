import ast
from dataclasses import dataclass, field
from pathlib import Path
import sys
from typing_extensions import Self
import numpy as np
import pandas as pd
import t3co.constants.Global as gl
from t3co.utils.print_class_objects import remove_df_attrs


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
    dc_files: list[str] = None
    selections_list: list[str] = None

    # Fueling
    ess_max_charging_power_kw: float = 0
    fs_fueling_rate_kg_per_min: float = 0
    fs_fueling_rate_gasoline_gpm: float = 0
    fs_fueling_rate_diesel_gpm: float = 0

    insurance_rates_file: str = ""
    residual_rates_file: str = ""
    fuel_prices_file: str = ""
    plf_weight_dist_file: str = ""

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

    fuel_prices_df: pd.DataFrame = None
    residual_rates_df: pd.DataFrame = None
    config_filename: str | Path = gl.RESOURCES_FOLDERPATH/"T3COConfig.csv"

    def from_file(self, filename: str, analysis_id: int) -> Self:
        """
        This method generates a Config dictionary from CSV file and calls Config.from_dict

        Args:
            filename (str): path of input T3CO Config file
            analysis_id (int): analysis ID selections

        Returns:
            Self.from_dict: method that gets Config instance from config_dict
        """
        self.config_filename = Path(filename)
        self.analysis_id = analysis_id
        config_df = self.validate_analysis_id()
        config_dict = config_df.to_dict()
        
        return self.from_dict(config_dict=config_dict)

    def from_dict(self, config_dict: dict) -> None:
        """
        This method generates a Config instance from config_dict

        Args:
            config_dict (dict): dictionary containing fields from T3CO Config input CSV file

        Returns:
            Self: Config instance containining all values from T3CO Config CSV file
        """
        try:
            config_dict["selections"] = ast.literal_eval(config_dict["selections"])
        except:  
            config_dict["selections"] = int(config_dict["selections"])
        self.__dict__.update(config_dict)

    def validate_analysis_id(self) -> pd.DataFrame | None:
        """
        This method validates that correct analysis id is input

        Args:
            filename (str): T3CO Config input CSV file path

        Raises:
            Exception: Error if analysis_id not found
        """     

        try:
            if self.config_filename.exists() and self.config_filename.suffix.lower() == '.csv':
                config_df = pd.read_csv(self.config_filename, index_col="analysis_id")
            else:
                raise FileExistsError

            config_df = config_df.loc[self.analysis_id].replace({np.nan: None})
            return config_df

        except FileExistsError:
            print(f'Config file ({self.config_filename}) does not exist')
            sys.exit(1)

        except:
            print(f"T3CO terminated. Analysis ID not available. Try these analysis_id's instead: {config_df.index.to_list()}")
            sys.exit(1)

    def check_drivecycles_and_create_selections(self):
        """
        This method checks if the config.drive_cycle input is a file or a folder. If a folder is provided, then it creates a list of all selections for each drivecycle in the folders as config.dc_files

        Args:
            config_file (str|Path): File path of config file
        """

        if self.drive_cycle:
            self.drive_cycle = (
                Path(self.drive_cycle)
                if Path(self.drive_cycle).is_absolute()
                else Path(self.config_filename).parents[0]
                / self.drive_cycle
            )
            if Path(self.drive_cycle).is_dir():
                self.dc_files = [p.absolute() for p in Path(self.drive_cycle).rglob("*.csv")]
                self.selections_list = []
                for selection in self.selections:
                    for i in range(len(self.dc_files)):
                        self.selections_list.append(str(selection) + "_" + str(i).zfill(4))
            else:
                self.selections_list =  self.selections

        else:
            self.selections_list = self.selections

    def read_auxiliary_files(self):
        self.fuel_prices_df = pd.read_csv(
            (
                Path(self.fuel_prices_file)
                if Path(self.fuel_prices_file).is_absolute()
                else gl.RESOURCES_FOLDERPATH / self.fuel_prices_file
            )
        )
        self.fuel_prices_df.set_index("Fuel", inplace=True)

        self.residual_rates_df = pd.read_csv(
            (
                Path(self.residual_rates_file)
                if Path(self.residual_rates_file).is_absolute()
                else gl.RESOURCES_FOLDERPATH / self.residual_rates_file
            )
        )
        
    def delete_dataframes(self):
        remove_df_attrs(self)