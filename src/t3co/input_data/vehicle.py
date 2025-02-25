from dataclasses import dataclass, field
from pathlib import Path
from typing import Union
try:
    from typing import Self  # Python 3.11+
except ImportError:
    from typing_extensions import Self  # Older versions of Python
    
import pandas as pd

from t3co.input_data.config import Config
from t3co.utils.print_class_objects import handle_nan, remove_df_attrs


@dataclass
class Vehicle:
    selection: Union[int, str] = None
    veh_pt_type: str = ""
    fc_eff_type: str = ""
    fc_max_kw: float = 0.0
    fs_kwh: float = 0.0
    mc_max_kw: float = 0.0
    ess_max_kwh: float = 0.0
    chg_eff: float = 0.0
    glider_kg: float = 0.0
    trans_kg: float = 0.0
    cargo_kg: float = 0.0
    fc_base_kg: float = 0.0
    fs_kwh_per_kg: float = 0.0
    fc_kw_per_kg: float = 0.0
    mc_pe_kg_per_kw: float = 0.0
    mc_pe_base_kg: float = 0.0
    ess_kg_per_kwh: float = 0.0
    ess_base_kg: float = 0.0
    veh_override_kg: float = 0.0

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the OpportunityCosts class.
        """
        instance = super(Vehicle, cls).__new__(cls)
        return instance

    @classmethod
    def from_config(cls, selection: int, config: Config) -> Self:
        """
        Creates a Vehicle instance from the configuration.

        Args:
            selection (int): The selection index.
            config (Config): The configuration instance.

        Returns:
            Self: An instance of the Vehicle class.
        """
        return cls.from_db(selection=selection, vehicle_db_file=config.vehicle_file)

    @classmethod
    def from_db(cls, selection: int, vehicle_db_file: Union[str, Path]) -> Self:
        """
        Creates a Vehicle instance from the vehicle database file.

        Args:
            selection (int): The selection index.
            vehicle_db_file (Union[str, Path]): The vehicle database file path.

        Returns:
            Self: An instance of the Vehicle class.
        """
        vehicle_db_df = pd.read_csv(
            (
                Path(vehicle_db_file).resolve(strict=True)
                if Path(vehicle_db_file).is_absolute()
                else Path(__file__).parents[1] / "resources" / vehicle_db_file
            ),
            usecols=lambda x: x in cls.__annotations__.keys(),
        )
        vehicle_dict = vehicle_db_df.loc[
            vehicle_db_df["selection"] == selection
        ].to_dict("records")[0]
        return cls(**handle_nan(vehicle_dict))

    def set_veh_kg(self) -> None:
        """
        Sets the vehicle weight in kilograms.
        """
        if self.veh_override_kg:
            self.veh_kg = self.veh_override_kg
        else:
            self.veh_kg = (
                self.glider_kg
                + self.trans_kg
                + self.cargo_kg
                + (self.fs_kwh / self.fs_kwh_per_kg if self.fs_kwh_per_kg != 0 else 0)
                + (
                    self.fc_base_kg + self.fc_kw_per_kg / self.fc_max_kw
                    if self.fc_max_kw != 0
                    else 0
                )
                + (
                    self.mc_pe_base_kg + self.mc_pe_kg_per_kw / self.mc_max_kw
                    if self.mc_max_kw != 0
                    else 0
                )
                + (
                    self.ess_base_kg + self.ess_kg_per_kwh / self.ess_max_kwh
                    if self.ess_max_kwh != 0
                    else 0
                )
            )

    def delete_dataframes(self) -> None:
        """
        Deletes DataFrame attributes from the Vehicle instance.
        """
        remove_df_attrs(self)
