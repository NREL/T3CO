import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing_extensions import List, Self

import pandas as pd

from t3co.input_data.config import Config
from t3co.utils.print_class_objects import remove_df_attrs


@dataclass
class Scenario:
    """
    Class object that contains all TCO parameters and performance target (range, grade, accel) information \
        for a vehicle such that performance and TCO can be computed during optimization
    """

    selection: float = 0
    scenario_name: str = ""
    drive_cycle: str = ""
    use_config: bool = True
    vmt_reduct_per_yr: float = 0
    vmt: list = field(default_factory=str)
    constant_trip_distance_mi: float = 0
    vehicle_life_yr: float = 0
    desired_ess_replacements: float = 0
    discount_rate_pct_per_yr: float = 0

    ess_max_charging_power_kw: float = 0
    ess_cost_dol_per_kw: float = 0
    ess_cost_dol_per_kwh: float = 0
    ess_base_cost_dol: float = 0
    ess_cost_reduction_dol_per_yr: float = 0
    ess_salvage_value_dol: float = 0
    ess_charge_rate_kW: float = 0
    pe_mc_cost_dol_per_kw: float = 0
    pe_mc_base_cost_dol: float = 0
    fc_ice_cost_dol_per_kw: float = 0
    fc_ice_base_cost_dol: float = 0
    fc_fuelcell_cost_dol_per_kw: float = 0
    fs_cost_dol_per_kwh: float = 0
    fs_h2_cost_dol_per_kwh: float = 0
    plug_base_cost_dol: float = 0
    markup_pct: float = 0
    tax_rate_pct: float = 0
    fc_cng_ice_cost_dol_per_kw: float = 0
    fs_cng_cost_dol_per_kwh: float = 0
    vehicle_glider_cost_dol: float = 0
    segment_name: str = ""
    gvwr_kg: float = 0
    gvwr_credit_kg: float = 0
    # a list of fuels, basecase fuel is singleton list
    fuel_type: List = field(default_factory=str)
    maint_oper_cost_dol_per_mi: List = field(default_factory=float)
    vocation: str = ""
    vehicle_class: str = ""
    model_year: float = 0
    region: str = ""
    target_range_mi: float = 0
    min_speed_at_6pct_grade_in_5min_mph: float = 0
    min_speed_at_1p25pct_grade_in_5min_mph: float = 0
    max_time_0_to_60mph_at_gvwr_s: float = 0
    max_time_0_to_30mph_at_gvwr_s: float = 0
    # TDA vars
    lw_imp_curve_sel: str = ""
    eng_eff_imp_curve_sel: str = ""
    aero_drag_imp_curve_sel: str = ""

    ess_init_soc_grade: float = -1.0
    ess_init_soc_accel: float = -1.0

    soc_norm_init_for_accel_pct: float = -1
    soc_norm_init_for_grade_pct: float = -1

    # fuel storage
    fs_fueling_rate_gasoline_gpm: float = 0
    fs_fueling_rate_diesel_gpm: float = 0
    fs_fueling_rate_kg_per_min: float = 0

    ### PHEV stuff
    # UF for % of miles in charge depleting mode
    phev_utility_factor_override: float = -1
    phev_utility_factor_computed: float = -1
    # percent (fractional) of motor power for setting kw_fc_demand_on during optimization
    motor_power_override_kw_fc_demand_on_pct: float = -1

    # This will be used to figure out the number of miles travelled before needing to charge
    # must be greater than 0
    shifts_per_year: list = field(default_factory=list)

    missed_trace_correction: bool = False
    max_time_dilation: float = -1
    min_time_dilation: float = -1
    time_dilation_tol: float = -1

    #
    ### Optimization Settings
    #
    skip_opt: bool = False
    knob_min_ess_kwh: list = field(default_factory=list)
    knob_max_ess_kwh: list = field(default_factory=list)
    knob_min_motor_kw: list = field(default_factory=list)
    knob_max_motor_kw: list = field(default_factory=list)
    knob_min_fc_kw: list = field(default_factory=list)
    knob_max_fc_kw: list = field(default_factory=list)
    knob_min_fs_kwh: list = field(default_factory=list)
    knob_max_fs_kwh: list = field(default_factory=list)
    # placeholder for if max_c_rate need to be entered as parameters for each scenario
    # c_rate_kwh_array: list = field(default_factory=list)
    # c_rate_array: list = field(default_factory=list)
    objective_phev_minimize_fuel_use: bool = False
    constraint_c_rate: bool = False
    constraint_range: bool = False
    constraint_accel: bool = False
    constraint_grade: bool = False
    objective_tco: bool = False
    constraint_trace_miss_dist_percent_on: bool = False
    trace_miss_dist_percent: float = 0
    constraint_phev_minimize_fuel_use_on: bool = False
    constraint_phev_minimize_fuel_use_percent: float = 0

    #
    ### TCO Element Activations and vars
    #
    labor_rate_dol_per_hr: float = 0
    downtime_oppy_cost_dol_per_hr: float = 0

    # payload loss factor vars, PLF
    activate_tco_payload_cap_cost_multiplier: bool = True
    plf_ref_veh_empty_mass_kg: float = 0
    plf_scenario_vehicle_empty_kg: float = 0
    plf_reference_vehicle_cargo_capacity_kg: float = 0
    plf_scenario_vehicle_cargo_capacity_kg: float = 0  # includes cargo credit kg
    estimated_lost_payload_kg: float = 0

    # Fueling Dwell time factors, FDT
    activate_tco_fueling_dwell_time_cost: bool = True
    dlf_min_charge_time_hr: float = 0
    fdt_dwpt_fraction_power_pct: float = 0
    fdt_avg_overhead_hr_per_dwell_hr: float = 0
    fdt_frac_full_charge_bounds: str = 0
    fdt_num_free_dwell_trips: float = 0
    fdt_available_freetime_hr: float = 0

    fuel_prices_dol_per_gge: list = field(default_factory=float)
    # Insurance factors
    insurance_rates_pct_per_yr: list = field(default_factory=float)

    # Residual Rate
    residual_rates_file: str = None
    residual_rates_df: pd.DataFrame = None
    residual_rate_pct: float = 0

    # Maintenance and Repair Downtime factors MR
    activate_mr_downtime_cost: bool = True
    mr_planned_downtime_hr_per_yr: float = 0
    mr_unplanned_downtime_hr_per_mi: list = field(default_factory=list)
    mr_avg_tire_life_mi: float = 0
    mr_tire_replace_downtime_hr_per_event: float = 0

    fuel_prices_file: str = ""
    fuel_prices_df: pd.DataFrame = None
    plf_weight_distribution_file: str = ""

    avg_speed_mph: float = None

    @classmethod
    def from_file(cls, selection: int, scenario_file: str | Path):
        scenario_df = pd.read_csv(
            scenario_file, usecols=lambda x: x in cls.__annotations__.keys()
        )
        scenario_dict = scenario_df.loc[scenario_df["selection"] == selection].to_dict(
            "records"
        )[0]
        scenario_dict["vehicle_class"] = " "
        scenario_dict["vehicle_class"] = (
            scenario_dict["vehicle_class"]
            .join(scenario_dict["scenario_name"].split()[:3])
            .lower()
        )
        scenario_dict["vmt"] = ast.literal_eval(scenario_dict["vmt"])[
            : scenario_dict["vehicle_life_yr"]
        ]
        scenario_dict["shifts_per_year"] = ast.literal_eval(
            scenario_dict["shifts_per_year"]
        )[: scenario_dict["vehicle_life_yr"]]
        scenario_dict["mr_unplanned_downtime_hr_per_mi"] = (
            ast.literal_eval(scenario_dict["mr_unplanned_downtime_hr_per_mi"])[
                : scenario_dict["vehicle_life_yr"]
            ]
            if scenario_dict["mr_unplanned_downtime_hr_per_mi"]
            else 0
        )
        scenario_dict["maint_oper_cost_dol_per_mi"] = (
            ast.literal_eval(scenario_dict["maint_oper_cost_dol_per_mi"])[
                : scenario_dict["vehicle_life_yr"]
            ]
            if scenario_dict["maint_oper_cost_dol_per_mi"]
            else -1
        )
        return cls(**scenario_dict)

    def from_config(self, config: Config = None, verbose: bool = False) -> None:
        """
        This method overrides certain scenario fields if use_config is True and config object is not None

        Args:
            config (Config, optional): Config object. Defaults to None.

        """
        fields_override = [
            "vehicle_life_yr",
            "fs_fueling_rate_kg_per_min",
            "fs_fueling_rate_gasoline_gpm",
            "fs_fueling_rate_diesel_gpm",
            "lw_imp_curve_sel",
            "eng_eff_imp_curve_sel",
            "aero_drag_imp_curve_sel",
            "constraint_range",
            "constraint_accel",
            "constraint_grade",
            "objective_tco",
            "constraint_c_rate",
            "constraint_trace_miss_dist_percent_on",
            "objective_phev_minimize_fuel_use",
            "activate_tco_payload_cap_cost_multiplier",
            "activate_tco_fueling_dwell_time_cost",
            "fdt_frac_full_charge_bounds",
            "activate_mr_downtime_cost",
        ]
        try:
            if config.dc_files is None:
                fields_override.append("drive_cycle")
            self.fields_overriden = []
            if self.use_config and config is not None:
                for field_select in fields_override:
                    if config.__dict__[field_select] is not None:
                        setattr(
                            self, field_select, config.__getattribute__(field_select)
                        )
                        self.fields_overriden.append(field_select)
                print(
                    f"Scenario Fields overridden from config: {self.fields_overriden}"
                ) if verbose else None
        except Exception:
            print(
                f"Config file not attached or scenario.use_config set to False: {config}"
            )

        self.residual_rates_df = config.residual_rates_df
        self.insurance_rates_file = config.insurance_rates_file
        self.fuel_prices_df = config.fuel_prices_df

        if self.activate_tco_payload_cap_cost_multiplier and config:
            self.plf_weight_distribution_file = config.plf_weight_dist_file

    def __del_dataframes__(self):
        remove_df_attrs(self)