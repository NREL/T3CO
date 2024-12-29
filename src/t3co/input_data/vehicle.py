from dataclasses import dataclass, field

from t3co.input_data.config import Config


@dataclass
class Vehicle:
    selection: int|str = None
    veh_pt_type: str = ""
    fuel_type: str = ""
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

    def from_df(cls):
        pass