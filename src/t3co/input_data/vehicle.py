from dataclasses import dataclass, field
from pathlib import Path
from typing_extensions import Self

import pandas as pd

from t3co.input_data.config import Config


@dataclass
class Vehicle:
    selection: int|str = None
    veh_pt_type: str = ""
    fc_eff_type: str = ""
    fc_max_kw: float = None
    fs_kwh: float = None
    mc_max_kw: float = None
    ess_max_kwh: float = None
    has_plugin: bool = False
    glider_kg: float = None
    trans_kg: float = None
    cargo_kg: float = None
    fc_base_kg: float = None
    fs_kwh_per_kg: float = None
    fc_kw_per_kg: float = None
    mc_pe_kg_per_kw: float = None
    mc_pe_base_kg: float = None
    ess_kg_per_kwh: float = None
    ess_base_kg: float = None
    veh_override_kg: float = None

    @classmethod
    def from_config(cls, config:Config):
        return cls.from_db(selection = config.selections, vehicle_db_file=config.vehicle_file)
    
    @classmethod
    def from_db(cls, selection: int, vehicle_db_file: str|Path)->Self:
        vehicle_db_df = pd.read_csv(vehicle_db_file, usecols = cls.__annotations__.keys())
        vehicle_dict = vehicle_db_df.loc[vehicle_db_df['selection']==selection].to_dict('records')[0]
        return cls(**vehicle_dict)
    
    def set_veh_kg(self):
        self.veh_kg = (
            self.glider_kg
            + self.trans_kg
            + self.cargo_kg
            + (self.fs_kwh/self.fs_kwh_per_kg if self.fs_kwh else 0)
            + (self.fc_base_kg + self.fc_kw_per_kg/self.fc_max_kw if self.fc_max_kw else 0)
            + (self.mc_pe_base_kg + self.mc_pe_kg_per_kw/self.mc_max_kw if self.mc_max_kw else 0)
            + (self.ess_base_kg + self.ess_kg_per_kwh/self.ess_max_kwh if self.ess_max_kwh else 0)
        )