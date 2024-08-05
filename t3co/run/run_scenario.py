"""Module for loading vehicles, scenarios, running them and managing them"""


import ast
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from fastsim import cycle, simdrive, vehicle
import os
# for debugging convenience
from typing_extensions import Self

from t3co.objectives import accel, fueleconomy, gradeability
from t3co.run import Global as gl
from t3co.tco import tco_analysis

# import importlib
# tco_analysis = importlib.reload(tco_analysis)

# ---------------------------------- powertrain adjustment methods ---------------------------------- #


def set_test_weight(vehicle, scenario):
    """
    assign standardized vehicle mass for accel and grade test using GVWR and GVWR Credit

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object
        scenario (t3co.run_scenario.Scenario): T3CO scenario object
    """
    # June 15,16 confirming that the test weight of vehicle should be GVWRKg + gvwr_credit_kg
    vehicle.veh_override_kg = scenario.gvwr_kg + scenario.gvwr_credit_kg
    vehicle.set_veh_mass()
    assert (
        vehicle.veh_kg > 0
    ), "vehicle weight [kg] cannot be zero, check Scenario values for gvwr_kg and gvwr_credit_kg"


def reset_vehicle_weight(vehicle):
    """
    This function resets vehicle mass after loaded weight tests are done for accel and grade

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object
    """
    vehicle.veh_override_kg = 0
    vehicle.set_veh_mass()


def limit_cargo_kg_for_moo_hev_bev(opt_scenario, mooadvancedvehicle):
    """
    This helper method is used within T3COProblem to assign limited cargo capacity based on GVWR + GVWRCredit and optimization vehicle mass for advanced vehicles

    Args:
        opt_scenario (t3co.run_scenario.Scenario): T3CO scenario object
        mooadvancedvehicle (fastsim.vehicle.Vehicle): pymoo optimization vehicle
    """
    # limit cargo to a value <= its original mass, decrease it if vehicle is overweight
    max_allowable_weight_kg = opt_scenario.gvwr_kg + opt_scenario.gvwr_credit_kg
    cargo_limited = max_allowable_weight_kg - (
        mooadvancedvehicle.veh_kg - mooadvancedvehicle.cargo_kg
    )
    cargo_limited = max(cargo_limited, 0)
    # TODO socialize the fact that this next line makes it impossible to add cargo capacity relative to baseline
    # lightweighting and such can improve energy efficiency but not increase cargo
    mooadvancedvehicle.cargo_kg = min(cargo_limited, opt_scenario.originalcargo_kg)
    mooadvancedvehicle.set_veh_mass()


# helper methods to ensure users call proper vehicle initialization methods to adjust vehicle powertrain and mass
def set_max_motor_kw(analysis_vehicle, scenario, max_motor_kw):
    """
    This helper method is used within T3COProblem to set max_motor_kw to optimization vehicle and set kw_demand_fc_on if PHEV

    Args:
        analysis_vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object
        scenario (t3co.run_scenario.Scenario): T3CO Scenarion object
        max_motor_kw (float): max motor power /kW
    """
    # old comments that may be needed again:
    # Scaling motor and ESS power with ESS capacity results in more reasonable
    # zero-to-sixty response to battery capacity and is generally consistent
    # with how things are done.  We need to firm up the functional form of this,
    # which came from Aaron Brooker for light duty.
    # veh.mc_max_kw = 24.46 * (veh.ess_max_kwh ** (-.475) * veh.ess_max_kwh)
    analysis_vehicle.mc_max_kw = max_motor_kw
    # TODO: for HEV (at least), battery power could be significantly lower than motor power,
    # and the following variable assignment will be pretty far off

    analysis_vehicle.ess_max_kw = (
        analysis_vehicle.mc_max_kw / analysis_vehicle.get_mcPeakEff()
    )

    # PHEV adjustment
    if analysis_vehicle.veh_pt_type == gl.PHEV:
        if scenario.motor_power_override_kw_fc_demand_on_pct != -1:
            analysis_vehicle.kw_demand_fc_on = (
                max_motor_kw * scenario.motor_power_override_kw_fc_demand_on_pct
            )

    analysis_vehicle.set_derived()


def set_max_battery_kwh(analysis_vehicle, max_ess_kwh):
    """
    This helper method is used within T3COProblem to set max_ess_kwh to optimization vehicle

    Args:
        analysis_vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object
        max_ess_kwh (float): max energy storage system energy capacity /kWh
    """
    analysis_vehicle.ess_max_kwh = max_ess_kwh
    analysis_vehicle.set_derived()


def set_max_battery_power_kw(analysis_vehicle, max_ess_kw):
    """
    This helper method is used within T3COProblem to set max_ess_kwx to optimization vehicle

    Args:
        analysis_vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object
        max_ess_kw (float): max energy storage system power /kW
    """
    analysis_vehicle.ess_max_kw = max_ess_kw
    analysis_vehicle.set_derived()


def set_max_fuel_converter_kw(analysis_vehicle, fc_max_out_kw):
    """
    This helper method is used within T3COProblem to set fc_max_out_kw to optimization vehicle

    Args:
        analysis_vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object
        fc_max_out_kw (float): max fuel converter power /kW
    """
    analysis_vehicle.fc_max_kw = fc_max_out_kw
    analysis_vehicle.set_derived()


def set_fuel_store_kwh(analysis_vehicle, fs_kwh):
    """
    This helper method is used within T3COProblem to set fs_kwh to optimization vehicle

    Args:
        analysis_vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object
        fs_kwh (float): fuel storage energy capacity /kWh
    """
    analysis_vehicle.fs_kwh = fs_kwh
    analysis_vehicle.set_derived()


def set_cargo_kg(analysis_vehicle, cargo_kg):
    """
    This helper method is used within T3COProblem to set cargo_kg to optimization vehicle

    Args:
        analysis_vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object
        cargo_kg (float): vehicle cargo capacity /kg
    """
    analysis_vehicle.cargo_kg = cargo_kg
    analysis_vehicle.set_veh_mass()


# --------------------------------- \\ powertrain adjustment methods --------------------------------- #
@dataclass
class Config:
    """
    New class to read T3COConfig file containing analysis attributes like vehicle and scenario paths, and scenario attribute overrides

    """

    analysis_id: int = 0
    analysis_name: str = ""
    vehicle_file: str = ""
    scenario_file: str = ""
    dst_dir: str = ""
    write_tsv: bool = False
    selections: str = ""
    # selections: list = field(default_factory=list)
    vehicle_life_yr: float = 0

    # Fueling
    ess_max_charging_power_kw: float = 0
    fs_fueling_rate_kg_per_min: float = 0
    fs_fueling_rate_gasoline_gpm: float = 0
    fs_fueling_rate_diesel_gpm: float = 0

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

    def __init__(self):
        pass

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

        config_df = pd.read_csv(filename, index_col="analysis_id").loc[analysis_id]
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
        # config_dict['selections'] = np.array(ast.literal_eval(config_dict['selections']))
        try:
            config_dict["selections"] = ast.literal_eval(config_dict["selections"])
        except:  # noqa: E722
            config_dict["selections"] = int(config_dict["selections"])
        self.__dict__.update(config_dict)

    def validate_analysis_id(self, filename: str, analysis_id: int = 0):
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


@dataclass
class Scenario:
    """
    Class object that contains all TCO parameters and performance target (range, grade, accel) information \
        for a vehicle such that performance and TCO can be computed during optimization
    """

    selection: float = 0
    drive_cycle: str = ""
    use_config: bool = True
    vmt_reduct_per_yr: float = 0
    vmt: list = field(default_factory=list)
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
    fuel_type: list = field(default_factory=list)
    maint_oper_cost_dol_per_mi: list = field(default_factory=list)
    vocation: str = ""
    vehicle_class: str = ""
    model_year: float = 0
    region: str = ""
    target_range_mi: float = 0
    min_speed_at_6pct_grade_in_5min_mph: float = 0
    min_speed_at_125pct_grade_in_5min_mph: float = 0
    max_time_0_to_60mph_at_gvwr_s: float = 0
    max_time_0_to_30mph_at_gvwr_s: float = 0
    # TDA vars
    lw_imp_curve_sel: str = ""
    eng_eff_imp_curve_sel: str = ""
    aero_drag_imp_curve_sel: str = ""
    # computed vars
    # scenario_gge_regional_temporal_fuel_price: str = ""
    originalcargo_kg: float = (
        -1.0
    )  # if needed, should be assigned immediately after vehicle read in
    # For adding mass from CdA during optimization. veh_kg = glider_kg + powertrainKg, where
    # glider_kg is assigned the value of originalglider_kg + CdAKg
    originalglider_kg: float = -1.0
    # for adding incremental cost to glider from different CdA guesses in moo loop
    originalGliderPrice: float = -1.0
    # for adding percent improvemnt cost to engine efficiency when optimizing CONV
    originalIceDolPerKw: float = -1.0
    # for adjusting fuel converter efficiency based on new peak eff
    origfc_eff_map: list = field(default_factory=list)
    # for adjusting drag coefficient of vehicle
    originaldrag_coef: float = -1

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
    # payload loss factor vars, PLF
    activate_tco_payload_cap_cost_multiplier: bool = True
    plf_ref_veh_empty_mass_kg: float = 0
    plf_scenario_vehicle_empty_kg: float = 0
    plf_reference_vehicle_cargo_capacity_kg: float = 0
    plf_scenario_vehicle_cargo_capacity_kg: float = 0  # includes cargo credit kg
    estimated_lost_payload_kg: float = 0

    # Dwell time factors, DLF
    activate_tco_fueling_dwell_time_cost: bool = False
    dlf_min_charge_time_hr: float = 0
    fdt_oppy_cost_dol_per_hr: float = 0
    dlf_dwell_efficiency_pct: float = 0
    dlf_time_available_charge_hr: float = 0
    fdt_dwpt_fraction_power_pct: float = 0
    fdt_avg_overhead_hr_per_dwell_hr: float = 0
    fdt_frac_full_charge_bounds: float = 0
    fdt_num_free_dwell_trips: float = 0
    fdt_available_freetime_hr: float = 0
    # Insurance factors
    insurance_rates_pct_per_yr: list = field(default_factory=list)

    # M&R Downtime factors
    activate_mr_downtime_cost: bool = False
    mr_planned_downtime_hr_per_yr: float = 0
    mr_unplanned_downtime_hr_per_mi: list = field(default_factory=list)
    mr_avg_tire_life_mi: float = 0
    mr_tire_replace_downtime_hr_per_event: float = 0

    def from_config(self, config: Config = None):
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
        self.fields_overriden = []
        if self.use_config == True and config != None:
            for field_select in fields_override:
                if (config.__dict__[field_select] is not None) and (
                    not self.__dict__[field_select]
                ):
                    setattr(self, field_select, config.__getattribute__(field_select))
                    # print(f'field: {field}, type: {type(self.__getattribute__(field))}, value: {self.__getattribute__(field)}')
                    self.fields_overriden.append(field_select)
            print(f"Scenario Fields overridden from config: {self.fields_overriden}")
        else:
            print(
                f"Config file not attached or scenario.use_config set to False: {config}"
            )

        return self


# PHEV utility methods
def check_phev_init_socs(a_vehicle: vehicle.Vehicle, scenario: Scenario):
    """
    This function checks that soc_norm_init_for_grade_pct and soc_norm_init_for_accel_pct are present only for PHEVs

    Args:
        a_vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object
        scenario (Scenario): T3CO scenario object
    """
    # these override ess_init_soc_grade and ess_init_soc_accel
    # these should ONLY be used for PHEV, for now, until discussed for use for HEV, BEV
    # init_soc = min_soc + (soc_norm_init_for_accel_pct * (max_soc - min_soc))
    if (
        np.isnan(scenario.soc_norm_init_for_grade_pct) == False
        and scenario.soc_norm_init_for_grade_pct != -1
    ):
        assert (
            a_vehicle.veh_pt_type == gl.PHEV
        ), "soc_norm_init_for_grade_pct only available for PHEVs"
        assert (
            scenario.ess_init_soc_grade == -1
        ), f"INPUT ERROR, user specifed ess_init_soc_grade {scenario.ess_init_soc_grade}, & soc_norm_init_for_grade_pct {scenario.soc_norm_init_for_grade_pct} for PHEV; the question of which one to use is ambiguous"
    if (
        np.isnan(scenario.soc_norm_init_for_accel_pct) == False
        and scenario.soc_norm_init_for_accel_pct != -1
    ):
        assert (
            a_vehicle.veh_pt_type == gl.PHEV
        ), "soc_norm_init_for_accel_pct only available for PHEVs"
        assert (
            scenario.ess_init_soc_accel == -1
        ), f"INPUT ERROR, user specifed ess_init_soc_accel {scenario.ess_init_soc_accel}, & soc_norm_init_for_accel_pct {scenario.soc_norm_init_for_accel_pct} for PHEV; the question of which one to use is ambiguous"


def get_phev_util_factor(scenario, v, mpgge):
    """
    This function gets the PHEV utility factor derived from the computed range of the
    vehicle and the operational day range computed from shifts per year and the first vmt year

    Args:
        scenario (Scenario): T3CO scenario object
        v (fastsim.Vehicle.vehicle): FASTSim vehicle object
        mpgge (dict): Miles per Gallon Gasoline Equivalent dictionary

    Returns:
        uf (float): PHEV computed utility factor
    """
    uf = scenario.phev_utility_factor_override
    assert type(scenario.phev_utility_factor_override) in [
        int,
        float,
    ], "should be -1 or some float"
    cd_range_mi = fueleconomy.get_range_mi(mpgge, v, scenario)["cd_aer_phev_range_mi"]

    if uf == -1:
        shift_range_mi = scenario.vmt[0] / scenario.shifts_per_year
        scenario.phev_utility_factor_computed = round(
            min(shift_range_mi, cd_range_mi) / shift_range_mi, 3
        )
        uf = scenario.phev_utility_factor_computed
    return uf


# utility methods sim drives
def get_objective_simdrive(analysis_vehicle: vehicle.Vehicle, cycle):
    """
    This function obtains the SimDrive for accel and grade test

    Args:
        analysis_vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object
        cycle (fastsim.cycle.Cycle): FASTSim Cycle object

    Returns:
        sd (fastsim.simdrive.SimDrive): FASTSim SimDrive object containing vehicle inputs and simulation output attributes
    """
    sd = simdrive.SimDrive(cycle, analysis_vehicle)
    sd = sd.to_rust()
    sim_params = sd.sim_params
    sim_params.reset_orphaned()
    sim_params.missed_trace_correction = False
    # accel and grade traces are not achievable for our vehicles in the way we've constructed the tests, so suppress this warning with large tolerance
    sim_params.trace_miss_speed_mps_tol = np.inf
    sim_params.energy_audit_error_tol = np.inf
    sim_params.trace_miss_dist_tol = np.inf
    sd.sim_params = sim_params

    return sd


def run_grade_or_accel(test, analysis_vehicle, sim_drive, ess_init_soc):
    """
    This function handles initial SOC considerations for grade and accel tests

    If ess_init_soc override is passed, use that
    Else if the vehicle is an HEV, use the standard HEV init SOC values for accel and grade
    Else, let FASTSim determine init SOC in sim_drive()
        BEVs use max_soc
        PHEVs use max_soc
        Conv init_soc doesn't matter
        HEVs attempt SOC balancing but that is overrident by HEV test init SOC

    Args:
        test (str): 'accel' or 'grade' test
        analysis_vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object
        sim_drive (fastsim.simdrive.SimDrive): FASTSim SimDrive object
        ess_init_soc (float): ESS initial state of charge (SOC)

    Raises:
        Exception: if test not in ['accel', 'grade']
    """

    if test == "accel":
        # this is what SimAccelTest object was doing in previous version (non-Rust JIT)
        hev_init_soc = (analysis_vehicle.max_soc + analysis_vehicle.min_soc) / 2.0
    elif test == "grade":
        hev_init_soc = analysis_vehicle.min_soc
    else:
        raise Exception("this should not have happened")

    if ess_init_soc is not None:
        sim_drive.sim_drive_walk(ess_init_soc)
    elif analysis_vehicle.veh_pt_type == gl.HEV:
        sim_drive.sim_drive_walk(hev_init_soc)
    else:
        sim_drive.sim_drive()


# utility methods to create fastsim vehicles
def create_fastsim_vehicle(veh_dict=None):
    """
    This function creates and returns an empty FASTSim vehicle object with no attributes or

    Args:
        veh_dict (dict, optional): Vehicle attributes dict. Defaults to None.

    Returns:
        v (fastsim.vehicle.Vehicle): FASTSim vehicle object
    """

    if not veh_dict:
        veh_dict = {"DELETEME": 0}
    v = vehicle.Vehicle(veh_dict=veh_dict)
    try:
        if not veh_dict:
            del v.DELETEME
    except AttributeError:
        pass
    return v


def get_vehicle(veh_no, veh_input_path):
    """
    This function loads vehicle object from vehicle number and input csv filepath

    Args:
        veh_no (int): vehicle selection number
        veh_input_path (str): vehicle model assumptions input CSV file path

    Returns:
        veh (fastsim.vehicle.Vehicle): FASTSim vehicle object
    """
    veh = vehicle.Vehicle.from_vehdb(veh_no, veh_input_path, to_rust=True)
    veh.set_derived()
    veh.set_veh_mass()

    return veh


# \\ end \\ utility methods to create fastsim vehicles


def get_scenario_and_cycle(veh_no, scenario_inputs_path, a_vehicle=None, config=None):
    """
    This function uses helper methods load_scenario and load_design_cycle_from_scenario \
        to get scenario object and cycle object corresponding to selected vehicle (by veh_no)

    Args:
        veh_no (int): vehicle selection number
        scenario_inputs_path (str): input file path for scenario assumptions CSV
        a_vehicle (fastsim.vehicle.Vehicle, optional): FASTSim vehicle object for given selection. Defaults to None.
        config (Config, optional): Config object for current analysis. Defaults to None.

    Returns:
        scenario (Scenario): T3CO scenario object selected
        cyc (fastsim.cycle.Cycle): FASTSim cycle object selected
    """
    scenario = load_scenario(veh_no, scenario_inputs_path, a_vehicle, config)
    cyc = load_design_cycle_from_scenario(scenario, gl.OPTIMIZATION_DRIVE_CYCLES)

    return scenario, cyc


def load_scenario(veh_no, scenario_inputs_path, a_vehicle=None, config=None):
    """
    This function gets the Scenario object from scenario input CSV filepath, initializes some fields,\
          and overrides some fields based on Config object

    Args:
        veh_no (int): vehicle selection number
        scenario_inputs_path (str): input file path for scenario assumptions CSV
        a_vehicle (fastsim.vehicle.Vehicle, optional): FASTSim vehicle object for given selection. Defaults to None.
        config (Config, optional): Config object for current analysis. Defaults to None.

    Returns:
        scenario (Scenario): Scenario object for given selection
    """
    scenarios = pd.read_csv(scenario_inputs_path)
    assert (
        len(scenarios[scenarios["selection"] == veh_no]) == 1
    ), f"conflict in {__file__}get_scenario(_): Scenario numbers in {scenario_inputs_path} are not unique "
    scenario_dict = scenarios[scenarios["selection"] == veh_no].to_dict("list")
    scenario_dict = {k: v[0] for k, v in scenario_dict.items()}
    scenario_dict["vehicle_class"] = " "
    scenario_dict["vehicle_class"] = (
        scenario_dict["vehicle_class"]
        .join(scenario_dict["scenario_name"].split()[:3])
        .lower()
    )

    if "scenario_name" in scenario_dict:
        del scenario_dict["scenario_name"]

    # handle PHEV fuels list and UF list, convert to lists
    fuels = scenario_dict["fuel_type"]
    if "[" in fuels and "]" in fuels:
        fuels = ast.literal_eval(
            fuels
        )  # PHEV ["CD electricity", "CD diesel", "CS diesel"]
    else:
        fuels = [fuels]
    scenario_dict["fuel_type"] = fuels

    # handle vmt, turn into list
    scenario_dict["vmt"] = ast.literal_eval(scenario_dict["vmt"])
    scenario_dict["mr_unplanned_downtime_hr_per_mi"] = ast.literal_eval(
        scenario_dict["mr_unplanned_downtime_hr_per_mi"]
    )
    # if config: scenario_dict['config'] = config
    scenario = Scenario(**scenario_dict)
    scenario = scenario.from_config(config)

    # convert insurance rates string into float list
    scenario.insurance_rates_pct_per_yr = list(
        np.float_(scenario.insurance_rates_pct_per_yr.strip(" ][").split(","))
    )

    # validate some inputs, assign as -1 if not provided by user in input file
    if np.isnan(scenario.ess_init_soc_grade):
        scenario.ess_init_soc_grade = -1
    if np.isnan(scenario.ess_init_soc_accel):
        scenario.ess_init_soc_accel = -1
    if np.isnan(scenario.soc_norm_init_for_accel_pct):
        scenario.soc_norm_init_for_accel_pct = -1
    if np.isnan(scenario.soc_norm_init_for_grade_pct):
        scenario.soc_norm_init_for_grade_pct = -1

    # PHEV settings and checks
    if (
        np.isnan(scenario.phev_utility_factor_override)
        or scenario.phev_utility_factor_override is None
    ):
        scenario.phev_utility_factor_override = -1
        # we need non-None vmt and shifts_per_year since there is no phev_utility_factor_override provided
        assert (
            scenario.shifts_per_year not in [False, None, np.nan]
        ), f"invalid shifts_per_year value {scenario.shifts_per_year}, need a valid shifts_per_year (positive integer) value to compute utility factor since there is no phev_utility_factor_override provided"
        assert (
            scenario.vmt[0] is not None
        ), "we need non-None vmt since there is no phev_utility_factor_override provided"
    if (
        np.isnan(scenario.motor_power_override_kw_fc_demand_on_pct)
        or scenario.motor_power_override_kw_fc_demand_on_pct is None
    ):
        scenario.motor_power_override_kw_fc_demand_on_pct = -1
    elif scenario.motor_power_override_kw_fc_demand_on_pct != -1:
        assert (
            scenario.motor_power_override_kw_fc_demand_on_pct < 1
            and scenario.motor_power_override_kw_fc_demand_on_pct > 0
        ), f"motor_power_override_kw_fc_demand_on_pct {scenario.motor_power_override_kw_fc_demand_on_pct}"
    if a_vehicle is not None and a_vehicle.veh_pt_type == gl.PHEV:
        if scenario.motor_power_override_kw_fc_demand_on_pct != 1:
            assert (
                a_vehicle.kw_demand_fc_on != None
                and np.isnan(a_vehicle.kw_demand_fc_on) != True
            )
    assert (
        scenario.phev_utility_factor_computed == -1
    ), "this should never be populated in input files, only computed if user does not populate phev_utility_factor_override"

    return scenario


def load_design_cycle_from_scenario(
    scenario, cyc_file_path=gl.OPTIMIZATION_DRIVE_CYCLES
):
    """
    This helper method loads the design cycle used for mpgge and range determination.
    It can also be used standalone to get cycles not in standard gl.OPTIMIZATION_DRIVE_CYCLES location,
    but still needs cycle name from scenario object, carried in scenario.drive_cycle.
    If the drive cycles are a list of tuples, handle accordingly with eval.

    Args:
        scenario (Scenario): Scenario object for current selection
        cyc_file_path (str, optional): drivecycle input file path. Defaults to gl.OPTIMIZATION_DRIVE_CYCLES.

    Returns:
        range_cyc (fastsim.cycle.Cycle): FASTSim cycle object for current Scenario object
    """
    # determine if scenario.drive_cycle is a simple string path or a list of tuples as a string
    sdc = scenario.drive_cycle
    if "[" in sdc and "]" in sdc and "(" in sdc and ")" in sdc:
        scenario.drive_cycle = ast.literal_eval(sdc)
        range_cyc = []
        for dc_weight in scenario.drive_cycle:
            cycle_file_name = Path(dc_weight[0]).name
            dc = load_design_cycle_from_path(
                cyc_file_path=Path(cyc_file_path) / dc_weight[0]
            )
            dc.name = cycle_file_name
            weight = dc_weight[1]
            range_cyc.append((dc, weight))
    else:
        cycle_file_name = Path(scenario.drive_cycle).name
        range_cyc = load_design_cycle_from_path(
            cyc_file_path=Path(cyc_file_path) / scenario.drive_cycle
        )
        range_cyc.name = cycle_file_name

    return range_cyc


def load_design_cycle_from_path(cyc_file_path):
    """
    This helper method loads the Cycle object from the drivecycle filepath

    Args:
        cyc_file_path (str): drivecycle input file path

    Returns:
        range_cyc (fastsim.cycle.Cycle): FASTSim cycle object for current Scenario object
    """
    if Path(cyc_file_path).exists() == False:
        finalized_path = gl.OPTIMIZATION_DRIVE_CYCLES
        print(f"drive cycle not found in {cyc_file_path} trying {finalized_path}")
    else:
        finalized_path = cyc_file_path
    range_cyc = cycle.Cycle.from_file(finalized_path)
    range_cyc = range_cyc.to_rust()
    return range_cyc


def vehicle_scenario_sweep(vehicle, scenario, range_cyc, verbose=False, **kwargs):
    """
    This function contains helper methods such as get_tco_of_vehicle, check_phev_init_socs, get_accel, and get_gradeability\
    and returns a dictionary of all TCO related outputs

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object for current selection
        scenario (Scenario): Scenario object for current selection
        range_cyc (fastsim.cycle.Cycle): FASTSim cycle object for current scenario
        verbose (bool, optional): if selected, prints out the TCO calculation process. Defaults to False.

    Returns:
        out (dict): output dictionary containing TCO elements
    """
    get_accel = kwargs.get("get_accel", True)
    get_accel_loaded = kwargs.get("get_accel_loaded", True)
    get_gradability = kwargs.get("get_gradability", True)
    write_tsv = kwargs.get("write_tsv", False)

    # run the vehicle through TCO calculations
    if verbose:
        print("Running `tco_analysis.get_tco_of_vehicle`")
    (
        tot_cost_Dol,
        discounted_TCO_Dol,
        oppy_cost_set,
        ownership_costs_df,
        discounted_costs_df,
        mpgge,
        veh_cost_set,
        design_cycle_sdr,
        veh_oper_cost_set,
        veh_opp_cost_set,
        tco_files,
    ) = tco_analysis.get_tco_of_vehicle(
        vehicle, range_cyc, scenario, write_tsv=write_tsv
    )

    # tco_analysis.get_operating_costs(scenario, ownership_costs_df, veh_opp_cost_set)

    vehicle_mass = {
        "glider_kg": vehicle.glider_kg,
        "cargo_kg": vehicle.cargo_kg,
        "transKg": vehicle.trans_kg * vehicle.comp_mass_multiplier,
        "ess_mass_kg": vehicle.ess_mass_kg,
        "mc_mass_kg": vehicle.mc_mass_kg,
        "fc_mass_kg": vehicle.fc_mass_kg,
        "fs_mass_kg": vehicle.fs_mass_kg,
        "veh_kg": vehicle.veh_kg,
        "gliderLb": gl.kg_to_lbs(vehicle.glider_kg),
        "cargoLb": gl.kg_to_lbs(vehicle.cargo_kg),
        "transLb": gl.kg_to_lbs(vehicle.trans_kg * vehicle.comp_mass_multiplier),
        "essMasLb": gl.kg_to_lbs(vehicle.ess_mass_kg),
        "mcMassLb": gl.kg_to_lbs(vehicle.mc_mass_kg),
        "fcMassLb": gl.kg_to_lbs(vehicle.fc_mass_kg),
        "fsMassLb": gl.kg_to_lbs(vehicle.fs_mass_kg),
        "vehLb": gl.kg_to_lbs(vehicle.veh_kg),
    }
    grade_sdr_6 = None
    grade_sdr_125 = None
    accel_sdr = None
    accel_loaded_sdr = None
    zero_to_60 = None
    zero_to_30 = None
    zero_to_60_loaded = None
    zero_to_30_loaded = None
    grade_6_mph_ach = None
    grade_1_25_mph_ach = None
    ess_init_soc_accel = None
    ess_init_soc_grade = None

    # init SOC overrides for grade and accel, for any vehicle that is not a PHEV
    if scenario.ess_init_soc_grade != -1:
        ess_init_soc_grade = scenario.ess_init_soc_grade
    if scenario.ess_init_soc_accel != -1:
        ess_init_soc_accel = scenario.ess_init_soc_accel

    check_phev_init_socs(vehicle, scenario)

    if scenario.soc_norm_init_for_grade_pct != -1:
        ess_init_soc_grade = vehicle.min_soc + (
            scenario.soc_norm_init_for_grade_pct * (vehicle.max_soc - vehicle.min_soc)
        )
    if scenario.soc_norm_init_for_accel_pct != -1:
        ess_init_soc_accel = vehicle.min_soc + (
            scenario.soc_norm_init_for_accel_pct * (vehicle.max_soc - vehicle.min_soc)
        )

    if get_accel:
        if verbose:
            print(f"{gl.SWEEP_PATH.name}:: Running accel.get_accel")
        zero_to_60, zero_to_30, accel_sdr = accel.get_accel(
            vehicle,
            scenario,
            set_weight_to_max_kg=False,
            ess_init_soc=ess_init_soc_accel,
            verbose=verbose,
        )
    if get_accel_loaded:
        if verbose:
            print(f"{gl.SWEEP_PATH.name}:: Running accel.get_accel loaded")
        zero_to_60_loaded, zero_to_30_loaded, accel_loaded_sdr = accel.get_accel(
            vehicle,
            scenario,
            set_weight_to_max_kg=True,
            ess_init_soc=ess_init_soc_accel,
            verbose=verbose,
        )
    if get_gradability:
        if verbose:
            print(f"{gl.SWEEP_PATH.name}:: Running gradeability.get_gradeability")
        (
            grade_6_mph_ach,
            grade_1_25_mph_ach,
            grade_sdr_6,
            grade_sdr_125,
        ) = gradeability.get_gradeability(
            vehicle,
            scenario,
            ess_init_soc=ess_init_soc_grade,
            set_weight_to_max_kg=True,
        )

    range_dict = fueleconomy.get_range_mi(mpgge, vehicle, scenario)

    out = {
        "discounted_costs_df": discounted_costs_df,
        "veh_oper_cost_set": veh_oper_cost_set,
        "veh_opp_cost_set": veh_opp_cost_set,
        "mpgge": mpgge,
        "veh_msrp_set": veh_cost_set,
        "vehicle": vehicle,
        "vehicle_mass": vehicle_mass,
        "zero_to_60": zero_to_60,
        "zero_to_30": zero_to_30,
        "zero_to_60_loaded": zero_to_60_loaded,
        "zero_to_30_loaded": zero_to_30_loaded,
        "grade_6_mph_ach": grade_6_mph_ach,
        "grade_1_25_mph_ach": grade_1_25_mph_ach,
        "scenario": scenario,
        "design_cycle_sim_drive_record": design_cycle_sdr,
        "accel_sim_drive_record": accel_sdr,
        "accel_loaded_sim_drive_record": accel_loaded_sdr,
        "grade_6_sim_drive_record": grade_sdr_6,
        "grade_125_sim_drive_record": grade_sdr_125,
        "disc_cost": discounted_TCO_Dol,
        "opportunity_cost_set": oppy_cost_set,
        "tot_cost": tot_cost_Dol,
        "tco_files": tco_files,
    }
    out.update(range_dict)
    return out


def run(
    veh_no,
    vocation="blank",
    vehicle_input_path=gl.FASTSIM_INPUTS,
    scenario_inputs_path=gl.OTHER_INPUTS,
):
    """
    This function runs vehicle_scenario_sweep based on vehicle and scenario objects read from input file paths

    Args:
        veh_no (int): vehicle selection number
        vocation (str, optional): vocation description of selected vehicle. Defaults to "blank".
        vehicle_input_path (str, optional): input file path for vehicle assumptions CSV. Defaults to gl.FASTSIM_INPUTS.
        scenario_inputs_path (str, optional): input file path for scenario assumptions CSV. Defaults to gl.OTHER_INPUTS.

    Returns:
        out (dict): output dictionary containing TCO results
    """

    # set up tco results directories for the vocation-scenario
    gl.vocation_scenario = vocation
    gl.set_tco_intermediates()
    gl.set_tco_results()

    # load the generated file of vehicles, drive cycles, and tech targets
    vehicle = get_vehicle(veh_no, vehicle_input_path)
    scenario, range_cyc = get_scenario_and_cycle(veh_no, scenario_inputs_path)

    out = vehicle_scenario_sweep(vehicle, scenario, range_cyc)

    return out


def rerun(vehicle, vocation, scenario):
    """
    This function runs vehicle_scenario_sweep when given the vehicle and scenario objects

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object
        vocation (str): vocation description
        scenario (Scenario): Scenario object

    Returns:
        out (dict): output dictionary containing TCO outputs
    """
    # set up tco results directories for the vocation-scenario
    gl.vocation_scenario = vocation
    gl.set_tco_intermediates()
    gl.set_tco_results()

    range_cyc = load_design_cycle_from_scenario(scenario)

    out = vehicle_scenario_sweep(vehicle, scenario, range_cyc)

    return out
