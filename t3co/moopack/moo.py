import copy
import logging
import time
import warnings
from time import gmtime, strftime

import autograd.numpy as anp
import fastsim
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# from pymoo.algorithms.nsga2 import NSGA2 as NSGA2
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.soo.nonconvex.nelder import NelderMead
from pymoo.algorithms.soo.nonconvex.pattern import PatternSearch

# from pymoo.algorithms.so_local_search import LocalSearch
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.core.problem import ElementwiseProblem
from pymoo.operators.sampling.lhs import LatinHypercubeSampling as LHS

# pymoo stuff
from pymoo.optimize import minimize
from pymoo.termination.default import DefaultMultiObjectiveTermination as MODT
from pymoo.termination.ftol import MultiObjectiveSpaceTermination
from pymoo.util.display.output import Output

from t3co.run import Global as gl
from t3co.run import run_scenario

# PyMoo runs a vehicle optimization with POC accounted for that produces 3 designs that
# meet accel and grade targets and are within 1% of target range.  Grant says this is
# about 2x as fast as what the other version did for a single vehicle.  We were working on
# - speed up (got it about 35x faster with ~2 person-hours of work)
# - validation -- check
# - making it callable as python module

# optimization objectives
TCO = "tot_cost"
PHEV_MINIMIZE_FUEL_USE_OBJECTIVE = "objective_phev_minimize_fuel_use"
OBJECTIVES = [TCO, PHEV_MINIMIZE_FUEL_USE_OBJECTIVE]

# optimization constraints
(
    RANGE,
    ACCEL30,
    ACCEL60,
    GRADE125,
    GRADE6,
) = (
    "range_mi",
    "zero_to_30_loaded",
    "zero_to_60_loaded",
    "grade_1_25_mph_ach",
    "grade_6_mph_ach",
)
ACCEL_GRADE_OVERSHOOT = "accel_grade_overshoot_tol_constraint"
TRACE_MISS_DIST_PERCENT = "constraint_trace_miss_dist_percent_on"
C_RATE = "c_rate"
PHEV_MINIMIZE_FUEL_USE_CONSTRAINT = "PHEV_MINIMIZE_CD_FUEL_USE_PERCENTAGE_CONSTRAINT"
CONSTRAINTS = [
    RANGE,
    ACCEL30,
    ACCEL60,
    GRADE125,
    GRADE6,
    ACCEL_GRADE_OVERSHOOT,
    TRACE_MISS_DIST_PERCENT,
    C_RATE,
    PHEV_MINIMIZE_FUEL_USE_CONSTRAINT,
]


# optimization parameters
# scalar powertrain modifers
KNOB_FCMAXKW = "fcMaxOutKw"
KNOB_ess_max_kwh = "ess_max_kwh"
KNOB_mc_max_kw = "mc_max_kw"
KNOB_fs_kwh = "fs_kwh"
# COST:  b * cda_perc^2 + a * cda_perc
# MASS:  b * cda_perc^2 + a * cda_perc
#   (need COST {a,b} and MASS {a,b})
KNOB_CDA = "CdA_perc_imp"
# curves
KNOB_FCPEAKEFF = "fc_peak_eff"
KNOB_WTDELTAPERC = "wt_delta_perc"

# also new variables to refer to light-weighting curve data,
#   fc peak eff curve data, & CdA (need COST {a,b} and MASS {a,b})
# new inputs for TDA/Benefits
# CdA_perc_imp_bounds | (5, 30)
# COST  b * cda_perc^2 + a * cda_perc
# MASS  b * cda_perc^2 + a * cda_perc

# T3CO moo return codes
OPTIMIZATION_SUCCEEDED = 1
OPTIMIZATION_FAILED_TO_CONVERGE = 2
EXCEPTION_THROWN = 3


ALGO_NSGA2 = "NSGA2"
ALGO_NelderMead = "NelderMead"
ALGO_PatternSearch = "PatternSearch"
ALGO_PSO = "PSO"

ALGORITHMS = [
    ALGO_NSGA2,
    ALGO_NelderMead,
    ALGO_PatternSearch,
    ALGO_PSO,
]

KNOBS = [
    KNOB_CDA,
    KNOB_FCMAXKW,
    KNOB_ess_max_kwh,
    KNOB_mc_max_kw,
    KNOB_FCPEAKEFF,
    KNOB_WTDELTAPERC,
    KNOB_fs_kwh,
]


class T3COProblem(ElementwiseProblem):
    """
    Class for creating PyMoo problem.
    """

    moobasevehicle: fastsim.vehicle
    mooadvancedvehicle: fastsim.vehicle
    opt_scenario: run_scenario.Scenario
    designcycle: fastsim.cycle
    config: run_scenario.Config

    def setup_opt_records(self):
        """
        This method sets up the empty optimization record arrays
        """
        #

        # objectives
        self.r_tcos = []
        self.r_cd_fc_kwh_percent = []
        self.r_cd_fc_kwh_used = []
        self.r_cd_elec_kwh_used = []

        self.reporting_vars = None
        self.r_grade_6s = []
        self.r_grade_125s = []
        self.r_accel_30l = []
        self.r_accel_60l = []
        self.r_ranges = []
        self.r_fuel_efficiencies = []
        self.r_wt_delta_perc_guess = []
        self.r_CdA_reduction_perc = []
        self.r_fc_peak_eff_guess = []
        self.r_fc_max_out_kw_guess = []
        self.r_fs_kwh_guess = []
        self.r_max_ess_kwh_guess = []
        self.r_max_motor_kw_guess = []
        # constraint records
        self.accel_30_constraint = []
        self.accel_60_constraint = []
        self.grade_6_constraint = []
        self.grade_125_constraint = []
        self.range_constraint = []
        self.grade_accel_overshoot_tol_constraint = []
        self.c_rate_constraint = []
        self.trace_miss_distance_percent_constraint_record = []
        self.phev_min_fuel_use_prcnt_const_record = []

    def __init__(
        self,
        knobs_bounds,
        vnum,
        optimize_pt=gl.BEV,
        obj_list=None,
        constr_list=None,
        verbose=False,
        config=None,
        **kwargs,
    ):
        """
        This constructor initializes optimization input variables

        Args:
            knobs_bounds (dict): Dictionary containing knobs bounds for optimization
            vnum (float): Vehicle selection number
            optimize_pt (vehicle.veh_pt_type, optional): Vehicle powertrain type - Conv, BEV, HEV, PHEV. Defaults to gl.BEV.
            obj_list (list, optional): List of objectives. Defaults to None.
            constr_list (list, optional): List of constraints. Defaults to None.
            verbose (bool, optional): if True, prints process steps. Defaults to False.
            config (run_scenario.Config, optional): T3CO Config object containing analysis attributes and scenario attribute overrides. Defaults to None.

        """
        self.setup_opt_records()

        # TODO there should probably not be any default values for kwargs

        # TODO: figure out parallelization and then modify the following line accordingly
        _ = kwargs.pop("parallelization", None)

        # possible TODO: make this a dict for grade, accel, and range tolerance
        self.range_overshoot_tol = kwargs.pop("range_overshoot_tol", None)
        self.grade_accel_overshoot_tol = kwargs.pop(
            "grade_accel_overshoot_tol", 0.01
        )  # TODO default of 1% # user should explicitly turn this on and set this outside moo.py

        # MOO optimization interpolation arrays and coefficients
        # engine peak efficiecy percents
        self.fc_eff_array = kwargs.pop(
            "fc_eff_array", np.array([46, 46, 51, 51, 53, 53, 60]) / 100
        )
        # additional $ cost per kw of engine per engine efficiency percent
        self.fc_cost_coeff_array = kwargs.pop(
            "fc_cost_coeff_array", np.array([0, 0, 7, 16, 22, 40, 74])
        )
        # glider_kg light-weighted percents
        self.ltwt_delta_percs = kwargs.pop(
            "ltwt_delta_percs", np.array([0, 5, 5, 10, 10, 25]) / 100
        )
        # additional $ cost per kg light-weighted
        self.ltwt_dol_per_kg_costs = kwargs.pop(
            "ltwt_dol_per_kg_costs", np.array([4.41, 8.82, 13.23, 17.64, 22.05, 35.27])
        )
        # , if you want to keep default values, they should be 52.1 and 6.7
        # To make it like what I sent before, Arthur can recalculate (should be enough decimals):
        # a = 100*a
        # b = 10000*b - Alicia
        self.cda_cost_coeff_a = kwargs.pop("cda_cost_coeff_a", 52.053)
        self.cda_cost_coeff_b = kwargs.pop("cda_cost_coeff_b", 6.7018)
        self.cda_mass_coeff_a = kwargs.pop(
            "cda_mass_coeff_a", 0
        )  # default formula doesn't need a_M coeff, wt = 17967.9*p^2
        self.cda_mass_coeff_b = kwargs.pop("cda_mass_coeff_b", 1.79679)
        self.cda_perc_imp_at_which_wt_penalty_maxes_out = kwargs.pop(
            "cda_perc_imp_at_which_wt_penalty_maxes_out", 9999999999
        )

        # just checker values, knobs_bounds may not actually have all of these populated, so [0,0] is never used beyond the asserts
        max_fc_bound = knobs_bounds.get(KNOB_FCPEAKEFF, (0, 0))[1]
        max_ltwt_bound = knobs_bounds.get(KNOB_WTDELTAPERC, (0, 0))[1]
        CdA_perc_imp_knob_max = knobs_bounds.get(KNOB_CDA, (0, 0))[1]

        self.knobs_bounds = knobs_bounds

        knobs = [key for key in knobs_bounds.keys()]
        lower_bounds = anp.array([val[0] for bound, val in knobs_bounds.items()])
        upper_bounds = anp.array([val[1] for bound, val in knobs_bounds.items()])

        self.write_tsv = kwargs.pop("write_tsv", False)

        self.obj_list = obj_list
        if obj_list is None:
            # create default objective list
            self.obj_list = [TCO]

        self.constr_list = constr_list

        # add acceleration and grade overshoot tolerance constraint implicitly if user is apply grade or acceleration constraints
        if len(set(self.constr_list) & set([ACCEL30, ACCEL60, GRADE125, GRADE6])):
            self.constr_list.append(ACCEL_GRADE_OVERSHOOT)

        n_constr = len(self.constr_list)
        # input (f"moo.py: T3COProblem __init__\n{self.constr_list}, \neffective constraints: {n_constr}")
        # make it so that knobs always need to be specified.
        self.knobs = knobs

        self.verbose = verbose

        self.optimize_pt = optimize_pt

        self.instantiate_moo_vehicles_and_scenario(vnum, config)

        # time dilation options, turned on for fuel efficiency cycle
        if "missed_trace_correction" in kwargs:
            self.opt_scenario.missed_trace_correction = kwargs.pop(
                "missed_trace_correction"
            )
            self.opt_scenario.max_time_dilation = kwargs.pop("max_time_dilation")
            self.opt_scenario.min_time_dilation = kwargs.pop("min_time_dilation")
            self.opt_scenario.time_dilation_tol = kwargs.pop("time_dilation_tol")

        n_obj = len(self.obj_list)

        n_args = len(knobs)

        # asserts
        assert (
            self.optimize_pt == self.mooadvancedvehicle.veh_pt_type
        ), "instantiate_moo_vehicles_and_scenario should have handled this"
        for knob in self.knobs:
            assert knob in KNOBS, f"knob {knob} not in defined parameters: {KNOBS}"
        for constraint in self.constr_list:
            assert (
                constraint in CONSTRAINTS
            ), f"constraint {constraint} not in defined constraints: {CONSTRAINTS}"
            if constraint == PHEV_MINIMIZE_FUEL_USE_CONSTRAINT:
                assert (
                    self.opt_scenario.constraint_phev_minimize_fuel_use_percent > 0
                    and self.opt_scenario.constraint_phev_minimize_fuel_use_percent < 1
                )
        assert len(OBJECTIVES) >= 1, "enable at least one objective"
        for obj in self.obj_list:
            assert (
                obj in OBJECTIVES
            ), f"objective {obj} not in defined objectives: {OBJECTIVES}"
        assert (
            set(self.constr_list) & set(self.obj_list) == set()
        ), f"cannot have constraints and objectives overlap constraints {self.constr_list} & {self.obj_list}"
        if KNOB_fs_kwh in self.knobs:
            assert (
                self.optimize_pt in [gl.CONV, gl.HEV, gl.PHEV]
            ), f"input knob bounds: {knobs_bounds}\naltering fuel store (tank, not battery) kwh size but vehicle powertrain to be optimized is {self.optimize_pt}"
        if KNOB_FCMAXKW in self.knobs:
            assert (
                self.optimize_pt in [gl.CONV, gl.HEV, gl.PHEV]
            ), f"input knob bounds: {knobs_bounds}\naltering fuel converter size but vehicle powertrain is {self.optimize_pt}"
        if KNOB_ess_max_kwh in self.knobs:
            assert (
                self.optimize_pt in [gl.BEV, gl.HEV, gl.PHEV]
            ), f"input knob bounds: {knobs_bounds}\naltering battery size but vehicle powertrain to be optimized is {self.optimize_pt}"
        if KNOB_mc_max_kw in self.knobs:
            assert (
                self.optimize_pt in [gl.BEV, gl.HEV, gl.PHEV]
            ), f"input knob bounds: {knobs_bounds}\naltering motor size but vehicle powertrain to be optimized is {self.optimize_pt}"
        assert (
            max_fc_bound <= max(self.fc_eff_array)
        ), f"max eng eff knob val greater than max of eng eff array {max_fc_bound} > {self.fc_eff_array}, could yield free efficiency"
        assert (
            max_ltwt_bound <= max(self.ltwt_delta_percs)
        ), f"max light-weight knob val greater than max of light-weighting percent array {max_ltwt_bound} > {self.ltwt_delta_percs}, could yield free light-weighting"
        assert (
            max_fc_bound <= 1
        ), f"knob bounds must be decimal format, max_fc_bound: {max_fc_bound}"
        assert (
            max_ltwt_bound <= 1
        ), f"knob bounds must be decimal format, max_ltwt_bound: {max_ltwt_bound}"
        assert (
            CdA_perc_imp_knob_max <= 1
        ), f"knob bounds must be decimal format, CdA_perc_imp_knob_max: {CdA_perc_imp_knob_max}"

        # n_ieq_constr, number of constraints that must yield < 0
        super().__init__(
            n_var=n_args,
            n_obj=n_obj,
            n_ieq_constr=n_constr,
            # lower bounds
            xl=lower_bounds,
            # upper bounds
            xu=upper_bounds,
            **kwargs,
        )

        if len(kwargs) > 0:
            warnings.warn(
                f"Possible unused/invalid kwargs provided:\n {list(kwargs.keys())}"
            )

    def compile_reporting_vars(self):
        """
        This method creates an output dictionary containing optimization results
        """
        d = {
            "objective_TCOs": self.r_tcos,
            "objective_fc_khw_percent": self.r_cd_fc_kwh_percent,
            "objective_fc_khw_used": self.r_cd_fc_kwh_used,
            "objective_elec_khw_used": self.r_cd_elec_kwh_used,
            "r_mph_ach_grade_6s": self.r_grade_6s,
            "r_mph_ach_grade_125s": self.r_grade_125s,
            "r_sec_to_ach_30mph_ldd": self.r_accel_30l,
            "r_sec_to_ach_60mph_ldd": self.r_accel_60l,
            "r_ach_ranges_mi": self.r_ranges,
            "target_mph_grade_6s": [self.opt_scenario.min_speed_at_6pct_grade_in_5min_mph]
            * len(self.r_grade_6s),
            "target_mph_grade_125s": [
                self.opt_scenario.min_speed_at_125pct_grade_in_5min_mph
            ]
            * len(self.r_grade_6s),
            "target_sec_to_30mph_ldd": [self.opt_scenario.max_time_0_to_30mph_at_gvwr_s]
            * len(self.r_grade_6s),
            "target_sec_to_60mph_ldd": [self.opt_scenario.max_time_0_to_60mph_at_gvwr_s]
            * len(self.r_grade_6s),
            "target_range_mi": [self.opt_scenario.target_range_mi] * len(self.r_grade_6s),
            "r_ach_fuel_efficiencies": self.r_fuel_efficiencies,
            "accel_30_constraint_vals": self.accel_30_constraint,
            "accel_60_constraint_vals": self.accel_60_constraint,
            "grade_6_constraint_vals": self.grade_6_constraint,
            "grade_125_constraint_vals": self.grade_125_constraint,
            "range_constraint_vals": self.range_constraint,
            "grade_accel_overshoot_tol_constraint_vals": self.grade_accel_overshoot_tol_constraint,
            "trace_miss_dist_percent_constraint_vals": self.trace_miss_distance_percent_constraint_record,
            "phev_min_fuel_use_pct_constraint_vals": self.phev_min_fuel_use_prcnt_const_record,
            "r_wt_delta_perc_guess": self.r_wt_delta_perc_guess,
            "r_CdA_reduction_perc": self.r_CdA_reduction_perc,
            "r_fc_peak_eff_guess": self.r_fc_peak_eff_guess,
            "r_fc_max_out_kw_guess": self.r_fc_max_out_kw_guess,
            "r_fs_kwh_guess": self.r_fs_kwh_guess,
            "r_max_ess_kwh_guess": self.r_max_ess_kwh_guess,
            "r_max_motor_kw_guess": self.r_max_motor_kw_guess,
        }
        self.reporting_vars = pd.DataFrame(data=d)

    def instantiate_moo_vehicles_and_scenario(self, vnum, config=None):
        """
        This method instantiates the multi-objective optimization problem vehicles and scenarios, starting with the baseline Conventional vehicle.

        Args:
            vnum (float): vehicle selection number
            config (run_scenario.Config, optional): T3CO Config object containing analysis attributes and scenario attribute overrides. Defaults to None.

        Raises:
            TypeError: Invalid optimize_pt selection
        """
        self.moobasevehicle = run_scenario.get_vehicle(
            vnum,
            veh_input_path=gl.FASTSIM_INPUTS,
        )

        self.opt_scenario, self.designcycle = run_scenario.get_scenario_and_cycle(
            vnum, gl.OTHER_INPUTS, config=config
        )

        if (
            self.opt_scenario.fuel_type == "diesel and electricity"
            and self.moobasevehicle.veh_pt_type == gl.HEV
        ):
            self.opt_scenario.fuel_type = "diesel"

        # save baseline values for optimization diffs
        self.opt_scenario.originalGliderPrice = self.opt_scenario.vehicle_glider_cost_dol
        self.opt_scenario.originalglider_kg = self.moobasevehicle.glider_kg
        self.opt_scenario.originalIceDolPerKw = self.opt_scenario.fc_ice_cost_dol_per_kw
        self.opt_scenario.origfc_eff_map = self.moobasevehicle.fc_eff_map.copy()
        self.opt_scenario.originalcargo_kg = self.moobasevehicle.cargo_kg
        self.opt_scenario.originaldrag_coef = self.moobasevehicle.drag_coef

        self.mooadvancedvehicle = copy.copy(self.moobasevehicle)

        if self.optimize_pt == gl.BEV:
            self.mooadvancedvehicle.veh_pt_type = gl.BEV
            run_scenario.set_max_fuel_converter_kw(self.mooadvancedvehicle, 0)
            # change to 0, based on Excel version direction when trying to run as EV
            self.mooadvancedvehicle.fs_max_kw = 0
            run_scenario.set_fuel_store_kwh(self.mooadvancedvehicle, 0)
        elif self.optimize_pt == gl.CONV:
            self.mooadvancedvehicle.veh_pt_type = gl.CONV
            run_scenario.set_max_motor_kw(
                self.mooadvancedvehicle, scenario=None, max_motor_kw=0
            )
            run_scenario.set_max_battery_kwh(self.mooadvancedvehicle, max_ess_kwh=0)
        elif self.optimize_pt == gl.HEV:
            self.mooadvancedvehicle.veh_pt_type = gl.HEV
            # nothing to zero out for HEV/FCEV
        elif self.optimize_pt == gl.PHEV:
            self.mooadvancedvehicle.veh_pt_type = gl.PHEV
        else:
            raise TypeError(f"invalid optimize_pt selection {self.optimize_pt}")

        # establish payload opp cost calc module
        # TODO, this should include FCEV, and this TCO element should be True/False activated
        # if self.opt_scenario.activate_tco_payload_cap_cost_multiplier or self.opt_scenario.activate_tco_fueling_dwell_time_cost or self.opt_scenario.activate_mr_downtime_cost:
        #     self.oppcostobj = opportunity_cost.OpportunityCost(self.opt_scenario)

    # --------- optimizer parameter application methods ---------
    def cda_percent_delta_knob(self, CdA_perc_reduction, optvehicle):
        """
        This method sets the drag_coef based on aero improvement curve and glider_kg based on cda_cost_coeff_a and cda_cost_coeff_b

        Args:
            CdA_perc_reduction (str): Name of aero improvement curve file
            optvehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object for optimization vehicle

        """

        # check value of CdA_reduction
        # print(CdA_perc_reduction)

        # functions that return cost, weight, and possibly other penalties w.r.t. various improvements

        def get_cost_per_CdA_delta(x):
            """
            Returns cost penalty given percent improvement in CdA.
            """
            # COST:  a * cda_perc + b * cda_perc^2
            a_C = self.cda_cost_coeff_a
            b_C = self.cda_cost_coeff_b
            x = x * 100
            return a_C * x + b_C * x**2

        def get_mass_per_CdA_delta(x):
            """
            Returns weight penalty [Lb converted to kg] given % improvement in CdA.
            These formulas are developed in pounds. Converted to kg for FASTSim at the end.
            """
            # MASS: a * cda_perc + b * cda_perc^2
            a_M = (
                self.cda_mass_coeff_a
            )  # default formula doesn't need a_M coeff, wt = 17967.9*p^2
            b_M = self.cda_mass_coeff_b
            x = x * 100
            CdA_perc_imp_at_which_wt_penalty_maxes_out = (
                self.cda_perc_imp_at_which_wt_penalty_maxes_out
            )
            return min(
                gl.lbs_to_kgs(
                    a_M * CdA_perc_imp_at_which_wt_penalty_maxes_out
                    + b_M * CdA_perc_imp_at_which_wt_penalty_maxes_out**2
                ),
                gl.lbs_to_kgs(a_M * x + b_M * x**2),
            )

        # reset drag coefficient based on percent improvement
        optvehicle.drag_coef = max(
            0.01,  # this is an additional hard-coded bound on drag coefficient that should probably be removed (throw error or warning if drag_coef < 0.01 instead of running and replacing with this default value)
            self.opt_scenario.originaldrag_coef * (1 - CdA_perc_reduction),
        )
        # glider cost penalty due to CdA improvement
        CdA_cost = get_cost_per_CdA_delta(CdA_perc_reduction)
        self.opt_scenario.vehicle_glider_cost_dol = self.opt_scenario.vehicle_glider_cost_dol + CdA_cost
        # mass adjustments. Add CdA mass FIRST, if applicable. Then limit cargo_kg if overweight from battery.
        optvehicle.glider_kg = optvehicle.glider_kg + get_mass_per_CdA_delta(
            CdA_perc_reduction
        )
        optvehicle.set_veh_mass()

    def weight_delta_percent_knob(self, wt_perc_reduction, optvehicle):
        """
        This method sets the knob from the lightweighting curve

        Args:
            wt_perc_reduction (float): Weight reduction percentage value from lightweighting curve
            optvehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object of the optimization vehicle
        """
        wt_delta_cost_per_kg = np.interp(
            x=wt_perc_reduction, xp=self.ltwt_delta_percs, fp=self.ltwt_dol_per_kg_costs
        )
        wt_delta_kg = optvehicle.glider_kg * wt_perc_reduction
        # Calculate lightweight cost from curve as an integral
        x_new = (
            self.ltwt_delta_percs[self.ltwt_delta_percs <= wt_perc_reduction]
            * optvehicle.glider_kg
        )
        y_new = self.ltwt_dol_per_kg_costs[self.ltwt_delta_percs <= wt_perc_reduction]
        if wt_delta_kg not in x_new:
            x_new = np.append(x_new, wt_delta_kg)
            y_new = np.append(y_new, wt_delta_cost_per_kg)
        self.opt_scenario.vehicle_glider_cost_dol = self.opt_scenario.vehicle_glider_cost_dol + np.trapz(
            y_new, x_new
        )
        optvehicle.glider_kg = optvehicle.glider_kg - wt_delta_kg
        optvehicle.set_veh_mass()

    def fc_peak_eff_knob(self, fc_peak_eff, optvehicle):
        """
        This method sets the knob from the engine efficiency curve

        Args:
            fc_peak_eff (float): Fuel converter peak effiency override from engine efficiency improvement curve
            optvehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object for optimization vehicle
        """
        fc_eff_array = self.fc_eff_array
        cost_coeff_array = self.fc_cost_coeff_array
        d_eff_dol_per_kw = np.interp(fc_peak_eff, fc_eff_array, cost_coeff_array)
        self.opt_scenario.fc_ice_cost_dol_per_kw = (
            self.opt_scenario.originalIceDolPerKw + d_eff_dol_per_kw
        )
        self.adjust_fc_peak_eff(fc_peak_eff, self.opt_scenario, optvehicle)

    def get_objs(self, x, write_tsv=False):
        """
        This method gets called when PyMoo calls _evaluate. It initializes objectives and constraints and runs vehicle_scenario_sweep
        
        x optimization knobs = [max motor kw, battery kwh, drag coeff % improvement]
        Function for running FE cycles and accel tests then returning
        fuel consumption and zero-to-sixty times.

        x is a set of genes (or parameters), so kwh size is a gene
        chromosome is a full gene, all values in x

        Args:
            x (dict): Dictionary containing optimization knobs - {max motor kw, battery kwh, drag coeff % improvement}
            write_tsv (bool, optional): if True, save intermediate dataframes. Defaults to False.

        Returns:
            obj_arr_F (np.array): Array of objectives - tot_cost and phev_cd_fuel_used_kwh
            constraint_results_G (np.array): Array of constraints
            rs_sweep (dict): Output dictionary from vehicle_scenario_sweep
        """

        # dict for providing mechanism for making sure all knobs get used
        x_dict = {knob: x[self.knobs.index(knob)] for knob in self.knobs}

        # if self.optimize_pt not in [gl.CONV, gl.BEV, gl.HEV]:
        #     raise TypeError(f"optimize_pt is not configured for {self.optimize_pt}")
        designcycle = self.designcycle
        optvehicle = self.mooadvancedvehicle

        # reset glider price and weight for light-weighting and/or CdA percent improvement
        self.opt_scenario.vehicle_glider_cost_dol = self.opt_scenario.originalGliderPrice
        optvehicle.glider_kg = self.opt_scenario.originalglider_kg

        wt_delta_perc_guess = x_dict.pop(KNOB_WTDELTAPERC, None)
        CdA_reduction_perc = x_dict.pop(KNOB_CDA, None)
        fc_peak_eff_guess = x_dict.pop(KNOB_FCPEAKEFF, None)
        fc_max_out_kw_guess = x_dict.pop(KNOB_FCMAXKW, None)
        max_ess_kwh_guess = x_dict.pop(KNOB_ess_max_kwh, None)
        max_motor_kw_guess = x_dict.pop(KNOB_mc_max_kw, None)
        fs_kwh_guess = x_dict.pop(KNOB_fs_kwh, None)
        # set knobs
        if "wt_delta_perc" in self.knobs:
            # confirmed with Alicia and Jason on 8/11/2021 that light-weighting should occur before CdA adjustment
            self.weight_delta_percent_knob(wt_delta_perc_guess, optvehicle)
        if "CdA_perc_imp" in self.knobs:
            self.cda_percent_delta_knob(CdA_reduction_perc, optvehicle)
        if "fc_peak_eff" in self.knobs:
            self.fc_peak_eff_knob(fc_peak_eff_guess, optvehicle)
        if "fcMaxOutKw" in self.knobs:
            run_scenario.set_max_fuel_converter_kw(optvehicle, fc_max_out_kw_guess)
        if KNOB_fs_kwh in self.knobs:
            run_scenario.set_fuel_store_kwh(optvehicle, fs_kwh_guess)
        if "ess_max_kwh" in self.knobs:
            run_scenario.set_max_battery_kwh(optvehicle, max_ess_kwh_guess)
        if "mc_max_kw" in self.knobs:
            run_scenario.set_max_motor_kw(
                optvehicle, self.opt_scenario, max_motor_kw_guess
            )

        # enforce 0 <= cargo kg <= initial cargo kg for BEV and HEV optimizations
        if self.optimize_pt in [gl.BEV, gl.HEV]:
            run_scenario.limit_cargo_kg_for_moo_hev_bev(self.opt_scenario, optvehicle)

        # # TODO, this calculation and application of payload loss is still not finalized.
        # this also needs to be used for FCEV, would be nice if there were an FCEV veh_pt_type!!!
        # also it needs to have a Scenario File on/off activation

        assert len(x_dict) == 0, f"Unapplied knobs: {list(x_dict.keys())}"

        # calculate objectives
        get_accel_loaded = False
        get_grade = False
        obj_arr_F = []
        g6_acvhd, g125_acvhd, z60l_acvhd, z30l_acvhd, tco_acvhd, mpgge, range_achvd = [
            None
        ] * 7
        if GRADE6 in self.constr_list or GRADE125 in self.constr_list:
            get_grade = True
        if ACCEL30 in self.constr_list or ACCEL60 in self.constr_list:
            get_accel_loaded = True

        rs_sweep = run_scenario.vehicle_scenario_sweep(
            optvehicle,
            self.opt_scenario,
            designcycle,
            verbose=self.verbose,
            get_accel=False,  # don't want non-loaded accel values, for now
            get_accel_loaded=get_accel_loaded,
            get_gradeability=get_grade,
            write_tsv=write_tsv,
        )

        mpgge = rs_sweep["mpgge"]
        g6_acvhd, g125_acvhd = (
            rs_sweep["grade_6_mph_ach"],
            rs_sweep["grade_1_25_mph_ach"],
        )
        z60l_acvhd, z30l_acvhd = (
            rs_sweep["zero_to_60_loaded"],
            rs_sweep["zero_to_30_loaded"],
        )
        tco_acvhd = rs_sweep["tot_cost"]
        if optvehicle.veh_pt_type in [gl.BEV, gl.CONV, gl.HEV]:
            range_achvd = rs_sweep["primary_fuel_range_mi"]
        elif optvehicle.veh_pt_type == gl.PHEV:
            # need range from PHEV that is used to compare to target_range_mi
            range_achvd = rs_sweep["cd_aer_phev_range_mi"]

        if self.verbose:
            print(
                f"grade_6_mph_ach {g6_acvhd} grade_1_25_mph_ach {g125_acvhd} zero_to_60_loaded {z60l_acvhd} "
                f"zero_to_30_loaded {z30l_acvhd} tco {tco_acvhd} mpgge {mpgge} range {range_achvd}"
            )

        # PHEV fuel usage stats
        pct_fc_kwh = None
        phev_cd_fuel_used_kwh = None
        phev_cd_battery_used_kwh = None
        if (
            PHEV_MINIMIZE_FUEL_USE_OBJECTIVE in self.obj_list
            or PHEV_MINIMIZE_FUEL_USE_CONSTRAINT in self.constr_list
        ):
            phev_cd_fuel_used_kwh = rs_sweep["mpgge"]["cd_fuel_used_kwh_total"]
            phev_cd_battery_used_kwh = rs_sweep["mpgge"]["cd_battery_used_kwh"]
            pct_fc_kwh = round(
                phev_cd_fuel_used_kwh
                / (phev_cd_battery_used_kwh + phev_cd_fuel_used_kwh),
                2,
            )
        #                                                           #
        # ********************** objectives  ********************** #
        #                                                           #
        if TCO in self.obj_list:
            obj_arr_F.append(tco_acvhd)
        if PHEV_MINIMIZE_FUEL_USE_OBJECTIVE in self.obj_list:
            obj_arr_F.append(phev_cd_fuel_used_kwh)
        #                                                           #
        # ******************** end objectives  ******************** #
        #                                                           #

        #                                                           #
        # ********************** constraints ********************** #
        #
        #                                                           #

        self.accel_30_constraint.append(None)
        self.accel_60_constraint.append(None)
        self.grade_6_constraint.append(None)
        self.grade_125_constraint.append(None)
        self.range_constraint.append(None)
        self.grade_accel_overshoot_tol_constraint.append(None)
        self.c_rate_constraint.append(None)
        self.trace_miss_distance_percent_constraint_record.append(None)
        self.phev_min_fuel_use_prcnt_const_record.append(None)

        constraint_results_G = []
        # calculate constraint violations
        # speed at grade minus target should be negative when constraint is met
        if GRADE6 in self.constr_list:
            constraint_results_G.append(
                self.opt_scenario.min_speed_at_6pct_grade_in_5min_mph - g6_acvhd
            )
        if GRADE125 in self.constr_list:
            constraint_results_G.append(
                self.opt_scenario.min_speed_at_125pct_grade_in_5min_mph - g125_acvhd
            )
        if ACCEL60 in self.constr_list:
            # zero-to-speed time should minus max allowable (target value) should
            # be negative when constraint is met
            # 9 sec achvd - 10 sec target = -1
            constraint_results_G.append(
                z60l_acvhd - self.opt_scenario.max_time_0_to_60mph_at_gvwr_s
            )
        if ACCEL30 in self.constr_list:
            constraint_results_G.append(
                z30l_acvhd - self.opt_scenario.max_time_0_to_30mph_at_gvwr_s
            )

        # calculate limiting grade/accel requirement if all constraints met
        if ACCEL_GRADE_OVERSHOOT in self.constr_list:
            constr_perc = {}
            if GRADE125 in self.constr_list:
                # todo, -abs() for all of these?
                g125c = (
                    -(g125_acvhd - self.opt_scenario.min_speed_at_125pct_grade_in_5min_mph)
                    / self.opt_scenario.min_speed_at_125pct_grade_in_5min_mph
                )
                constr_perc[GRADE125] = g125c
                self.grade_125_constraint[-1] = g125c
            if GRADE6 in self.constr_list:
                g6c = (
                    -(g6_acvhd - self.opt_scenario.min_speed_at_6pct_grade_in_5min_mph)
                    / self.opt_scenario.min_speed_at_6pct_grade_in_5min_mph
                )
                constr_perc[GRADE6] = g6c
                self.grade_6_constraint[-1] = g6c
            if ACCEL60 in self.constr_list:
                z60c = (
                    z60l_acvhd - self.opt_scenario.max_time_0_to_60mph_at_gvwr_s
                ) / self.opt_scenario.max_time_0_to_60mph_at_gvwr_s
                constr_perc[ACCEL60] = z60c
                self.accel_60_constraint[-1] = z60c
            if ACCEL30 in self.constr_list:
                z30c = (
                    z30l_acvhd - self.opt_scenario.max_time_0_to_30mph_at_gvwr_s
                ) / self.opt_scenario.max_time_0_to_30mph_at_gvwr_s
                constr_perc[ACCEL30] = z30c
                self.accel_30_constraint[-1] = z30c

            # if all constraints meet target, then find closest overshoot and ensure it's below tolerance
            if (len(constr_perc) > 0) & (
                np.array(list(constr_perc.values())) < 0
            ).all():
                # say largest negative percent is -.1 (closest to target, 10% exceeding)
                # tolerance is .05
                # -(-.1) - 0.05 = 0.05, >= 0, constraint is violated. Constraints are in bounds if they return < 0
                min_grade_accel_excess = (
                    -constr_perc[max(constr_perc, key=constr_perc.get)]
                    - self.grade_accel_overshoot_tol
                )
            else:
                min_grade_accel_excess = -1  # no constraint to satisfy
            constraint_results_G.append(min_grade_accel_excess)
            self.grade_accel_overshoot_tol_constraint[-1] = min_grade_accel_excess

        if RANGE in self.constr_list:
            # if you fall short of range target
            if self.range_overshoot_tol is None:
                range_mi_cv = (
                    self.opt_scenario.target_range_mi - range_achvd
                )  # pos return, failed
            else:
                if range_achvd <= self.opt_scenario.target_range_mi:
                    range_mi_cv = (
                        self.opt_scenario.target_range_mi - range_achvd
                    )  # pos return, failed
                else:
                    range_mi_cv = range_achvd - (
                        self.opt_scenario.target_range_mi * (1 + self.range_overshoot_tol)
                    )

            constraint_results_G.append(range_mi_cv)
            self.range_constraint[-1] = range_mi_cv

        # c rate constraint
        if C_RATE in self.constr_list:
            self.c_rate_constraint[-1] = (
                self.mooadvancedvehicle.ess_max_kw / self.mooadvancedvehicle.ess_max_kwh
                - np.interp(
                    self.mooadvancedvehicle.ess_max_kwh,
                    # TODO, this 2D array needs to be an input
                    [1.0, 10.0, 188.0, 660.0],  # battery sizes kwh
                    [24.0, 12.0, 2.0, 0.7],  # c rates (kw/kwh)
                )
            )
            constraint_results_G.append(self.c_rate_constraint[-1])

        # # trace miss constraint
        if TRACE_MISS_DIST_PERCENT in self.constr_list:
            assert (
                self.opt_scenario.trace_miss_dist_percent > 0
                and self.opt_scenario.trace_miss_dist_percent < 1
            ), "scenario file input trace_miss_dist_percent must be decimal value greater than 0 and less than 1"
            cycle_records = rs_sweep["design_cycle_sim_drive_record"]
            max_dist_frac_result = max(
                sdr.trace_miss_dist_frac for sdr in cycle_records
            )
            # .1 -> 10%
            max_dist_frac_miss = self.opt_scenario.trace_miss_dist_percent
            constraint_results_G.append(max_dist_frac_result - max_dist_frac_miss)
            self.trace_miss_distance_percent_constraint_record[-1] = (
                max_dist_frac_result - max_dist_frac_miss
            )

        if PHEV_MINIMIZE_FUEL_USE_CONSTRAINT in self.constr_list:
            assert (
                self.opt_scenario.constraint_phev_minimize_fuel_use_percent > 0
            ), "scenario.constraint_phev_minimize_fuel_use_percent must be value > 0 and < 1"
            assert (
                self.opt_scenario.constraint_phev_minimize_fuel_use_percent < 1
            ), "scenario.constraint_phev_minimize_fuel_use_percent must be value > 0 and < 1"
            constraint_results_G.append(
                pct_fc_kwh - self.opt_scenario.constraint_phev_minimize_fuel_use_percent
            )
            self.phev_min_fuel_use_prcnt_const_record[-1] = (
                pct_fc_kwh - self.opt_scenario.constraint_phev_minimize_fuel_use_percent
            )

        #                                                           #
        # ******************** end constraints ******************** #
        #                                                           #

        # append reporting variables
        # obj vars
        self.r_tcos.append(tco_acvhd)
        self.r_cd_fc_kwh_percent.append(pct_fc_kwh)
        self.r_cd_fc_kwh_used.append(phev_cd_fuel_used_kwh)
        self.r_cd_elec_kwh_used.append(phev_cd_battery_used_kwh)

        self.r_grade_6s.append(g6_acvhd)
        self.r_grade_125s.append(g125_acvhd)
        self.r_accel_60l.append(z60l_acvhd)
        self.r_accel_30l.append(z30l_acvhd)
        self.r_fuel_efficiencies.append(mpgge)
        self.r_ranges.append(range_achvd)
        self.r_wt_delta_perc_guess.append(wt_delta_perc_guess)
        self.r_CdA_reduction_perc.append(CdA_reduction_perc)
        self.r_fc_peak_eff_guess.append(fc_peak_eff_guess)
        self.r_fc_max_out_kw_guess.append(fc_max_out_kw_guess)
        self.r_fs_kwh_guess.append(fs_kwh_guess)
        self.r_max_ess_kwh_guess.append(max_ess_kwh_guess)
        self.r_max_motor_kw_guess.append(max_motor_kw_guess)

        return np.array(obj_arr_F), np.array(constraint_results_G), rs_sweep

    def _evaluate(self, x, out, *args, **kwargs):
        """
        This method runs T3COProblem.get_objs() when running Pymoo optimization

        Args:
            x (dict): Dictionary containing optimization knobs
            out (dict): Dictionary containing TCO results for optimization runs
        """
        obj_arr_F, constr_arr, _ = self.get_objs(x)
        out["F"] = obj_arr_F

        if len(constr_arr) > 0:
            out["G"] = constr_arr

    def adjust_fc_peak_eff(self, fc_peak_eff, scenario, optvehicle):
        """
        This method augments an advanced vehicle fc_eff_array based on new fc_peak_eff using baseline fc_eff_array


        Args:
            fc_peak_eff (float): Fuel converter peak efficiency override
            scenario (run_scenario.Scenario): Scenario object of current selection
            optvehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object of optimization vehicle
        """
        old_peak_eff = scenario.origfc_eff_map.max()
        optvehicle.fc_eff_map = scenario.origfc_eff_map * (
            1 + (fc_peak_eff - old_peak_eff) / old_peak_eff
        )
        optvehicle.set_derived()

    # ------------------------------------ utility functions ------------------------------------
    def sweep_knob(self, knob, definition=100, plot=False, optres=None, **kwargs):
        """
        This method sweeps the optimization knob of vehicle from lbound to ubound, return TCO \
            plot optres to see if there's agreement from opt solution and your sweep

        Args:
            knob (list): list of knobs names for optimization
            definition (int, optional): Number of points. Defaults to 100.
            plot (bool, optional): if True, saves plot of bounds and TCOs. Defaults to False.
            optres (float, optional): Optimization resolution. Defaults to None.

        Returns:
            tcos (list): List of TCOs of length=definition
        """
        label = kwargs.get("label", "")
        sweep_knob_accel_test = kwargs.get("sweep_knob_accel_test", False)
        # save knobs and obj list
        temp_obj_list = self.obj_list
        self.knobs = [knob]
        self.obj_list = [TCO]
        lbound, ubound = self.knobs_bounds[knob]
        tcos = [self.get_objs([x])[0] for x in np.linspace(lbound, ubound, definition)]

        if sweep_knob_accel_test:
            opt_res_kw = np.inf
            if optres is not None:
                opt_res_kw = optres
            assert knob in [KNOB_mc_max_kw, KNOB_FCMAXKW]
            self.obj_list = [ACCEL30, ACCEL60]
            # objs.extend([z60l, z30l]) {(60, 30),...(60, 30)}
            thirty_mph_times = []
            sixty_mph_times = []
            largest_infeasible_30s_size = None
            failed_30_s_time = None
            largest_infeasible_60s_size = None
            failed_60_s_time = None
            for x in np.linspace(lbound, ubound, definition):
                z60l, z30l = self.get_objs([x])
                thirty_mph_times.append([z30l, x])
                sixty_mph_times.append([z60l, x])
            for res in sixty_mph_times:
                z60l, x = res
                if z60l > self.opt_scenario.max_time_0_to_60mph_at_gvwr_s and x < opt_res_kw:
                    largest_infeasible_60s_size = x
                    failed_60_s_time = z60l
            for res in sixty_mph_times:
                z30l, x = res
                if z30l > self.opt_scenario.max_time_0_to_30mph_at_gvwr_s and x < opt_res_kw:
                    largest_infeasible_30s_size = x
                    failed_30_s_time = z30l

        # todo, figure out how to get mpgge in the other y axis
        if plot:
            resdir = gl.MOO_KNOB_SWEEP_PLOTS_DIR
            if not resdir.exists():
                resdir.mkdir()
            ts = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
            plt.figure(figsize=(7, 4))
            plt.ylabel("$TCO")
            plt.title(f"{label}_{ts}_{knob}")
            plt.xlabel(f"knob value for {definition} pts")
            plt.plot(
                np.linspace(lbound, ubound, definition),
                tcos,
                label=f"TCO from global optimum, sweeping {knob}",
            )
            if optres is not None:
                plt.vlines(
                    optres,
                    min(tcos),
                    max(tcos),
                    color="red",
                    label=f"MOO {knob} solution: {optres}",
                )
            if sweep_knob_accel_test:
                if largest_infeasible_30s_size is not None:
                    plt.vlines(
                        largest_infeasible_30s_size,
                        min(tcos),
                        max(tcos),
                        color="orange",
                        label=f"failed accel test 0 to 30 res: {failed_30_s_time} target: {self.opt_scenario.max_time_0_to_30mph_at_gvwr_s} {knob} size: {largest_infeasible_30s_size}",
                    )
                if largest_infeasible_60s_size is not None:
                    plt.vlines(
                        largest_infeasible_60s_size,
                        min(tcos),
                        max(tcos),
                        color="yellow",
                        label=f"failed accel test 0 to 60 res: {failed_60_s_time} target: {self.opt_scenario.max_time_0_to_60mph_at_gvwr_s} {knob} size: {largest_infeasible_30s_size}",
                    )
            plt.legend()
            plt.savefig(resdir / f"{knob}_{label}_{ts}.png")
            print(f"saving {knob} results to ", resdir)
            plt.show()
        self.knobs = self.knobs_bounds.keys()
        self.obj_list = temp_obj_list
        return tcos

    def get_tco_from_moo_advanced_result(self, x):
        """
        This method is a utility function to get detailed TCO information from optimized MOO result

        Args:
            x (dict): Dictionary containing optimization knobs - [max motor kw, battery kwh, drag coeff % improvement]

        Returns:
            out (dict): Dictionary containing TCO results for optimization runs
        """
        x_dict = {knob: x[self.knobs.index(knob)] for knob in self.knobs}
        wt_delta_perc_guess = x_dict.pop(KNOB_WTDELTAPERC, None)
        CdA_reduction_perc = x_dict.pop(KNOB_CDA, None)
        fc_peak_eff_guess = x_dict.pop(KNOB_FCPEAKEFF, None)
        fc_max_out_kw_guess = x_dict.pop(KNOB_FCMAXKW, None)
        max_ess_kwh_guess = x_dict.pop(KNOB_ess_max_kwh, None)
        max_motor_kw_guess = x_dict.pop(KNOB_mc_max_kw, None)
        fs_kwh_guess = x_dict.pop(KNOB_fs_kwh, None)

        print("MOO Final Solution:")
        if wt_delta_perc_guess is not None:
            print(KNOB_WTDELTAPERC.rjust(20, " "), f":{round(wt_delta_perc_guess, 4)}")
        if CdA_reduction_perc is not None:
            print(KNOB_CDA.rjust(20, " "), f":{round(CdA_reduction_perc, 4)}")
        if fc_peak_eff_guess is not None:
            print(KNOB_FCPEAKEFF.rjust(20, " "), f":{round(fc_peak_eff_guess, 4)}")
        if fc_max_out_kw_guess is not None:
            print(KNOB_FCMAXKW.rjust(20, " "), f":{round(fc_max_out_kw_guess, 4)}")
        if max_ess_kwh_guess is not None:
            print(KNOB_ess_max_kwh.rjust(20, " "), f":{round(max_ess_kwh_guess, 4)}")
        if max_motor_kw_guess is not None:
            print(KNOB_mc_max_kw.rjust(20, " "), f":{round(max_motor_kw_guess, 4)}")
        if fs_kwh_guess is not None:
            print(KNOB_fs_kwh.rjust(20, " "), f":{round(fs_kwh_guess, 4)}")

        _, _, out = self.get_objs(x, write_tsv=False)

        return out

    # ------------------------------------ end utility functions ------------------------------------


# TODO, needs refactor
class T3CODisplay(Output):
    """
    This class contains the display object for Pymoo optimization printouts - pymoo.util.display.Display

    Args:
        Output (pymoo.util.display.output.Output): Pymoo minimize display object
    """

    def __init__(self, **kwargs):
        """
        This constructor initializes the pymoo.util.display.Display object
        """
        super().__init__(**kwargs)
        self.term = MultiObjectiveSpaceTermination()

    def _do(self, problem, evaluator, algorithm):
        """
        This constructor creates the output printouts

        Args:
            problem (moo.T3COProblem): Pymoo optimization
            evaluator (float): evaluator
            algorithm (str): algorithm name
        """
        super()._do(problem, evaluator, algorithm)
        if problem.n_constr > 0:
            max_cv = np.max(algorithm.pop.get("G"))
            self.output.append("CV max", f"{max_cv:.3g}", width=10)
            # self.output.append("CV key",
            #     problem.constr_list[np.argmax(algorithm.pop.get('G')) % problem.n_constr] if max_cv > 0 else '-----',
            #     width=15
            # )
        if "tot_cost" in problem.obj_list:
            tco_start_idx = problem.obj_list.index("tot_cost")  # noqa: F841
            # tco_min_for_pop = min(algorithm.pop.get('F')[tco_start_idx::len(problem.obj_list)])[0]
            # self.output.append("min(TCO)", f"{tco_min_for_pop:.5g}")
        self.output.append("obj max", f"{np.max(algorithm.pop.get('F')):.5g}", width=10)
        self.output.append("n_nds", len(algorithm.opt), width=7)

        self.term.do_continue(algorithm)

        max_from, eps = "-", "-"
        if len(self.term.metrics) > 0:
            metric = self.term.metrics[-1]
            tol = self.term.tol
            delta_ideal, delta_nadir, delta_f = (
                metric["delta_ideal"],
                metric["delta_nadir"],
                metric["delta_f"],
            )
            if delta_ideal > tol:
                max_from = "ideal"
                eps = delta_ideal
            elif delta_nadir > tol:
                max_from = "nadir"
                eps = delta_nadir
            else:
                max_from = "f"
                eps = delta_f

        self.output.append("eps", eps)
        self.output.append("indicator", max_from)


def run_optimization(
    pop_size,
    n_max_gen,
    knobs_bounds,
    vnum,
    x_tol,
    f_tol,
    nth_gen,
    n_last,
    algo,
    obj_list=None,
    config=None,
    **kwargs,
):
    """
    This method creates and runs T3COProblem minimization

    Args:
        pop_size (int): Population size for optimization
        n_max_gen (int): maximum number of generations for optimization
        knobs_bounds (dict): Dictionary containing knobs and bounds
        vnum (float): vehicle selection number
        x_tol (float): tolerance in parameter space
        f_tol (float): tolerance in objective space
        nth_gen (int): number of generations to evaluate if convergence occurs
        n_last (int): number of generations to look back for termination
        algo (str): algorithm name
        obj_list (list, optional): list of objectives - TCO or PHEV_MINIMIZE_FUEL_USE_OBJECTIVE. Defaults to None.
        config (run_scenario.Config, optional): T3CO Config object containing analysis attributes and scenario attribute overrides. Defaults to None.

    Returns:
        res (pymoo.core.result.Result): Pymoo optimization result object
        problem (moo.T3COProblem): T3COProblem ElementwiseProblem object
        OPTIMIZATION_SUCCEEDED (bool): if True, pymoo.minimize succeeded
    """

    verbose = kwargs.pop("verbose", False)
    optimize_pt = kwargs.pop("optimize_pt", gl.BEV)
    return_least_infeasible = kwargs.pop("optimize_pt", False)
    skip_optimization = kwargs.pop("skip_optimization", False)

    if verbose:
        print("Running optimization.")

    if verbose:
        print(knobs_bounds)

    problem = T3COProblem(
        parallelization=("threads", 1),
        knobs_bounds=knobs_bounds,
        vnum=vnum,
        obj_list=obj_list,
        optimize_pt=optimize_pt,
        verbose=verbose,
        config=config,
        **kwargs,
    )

    if skip_optimization:
        return None, problem, None, None

    print(
        f"moo.run_optimization algo {algo}, x_tol {x_tol}, f_tol {f_tol}, nth_gen {nth_gen}, n_last {n_last}, n_max_gen {n_max_gen}, pop_size {pop_size}"
    )

    assert (
        algo in ALGORITHMS
    ), f"{algo} not in T3CO list of optimization algorithms {str(ALGORITHMS)}"

    if algo == ALGO_NSGA2:
        algorithm = NSGA2(
            pop_size=pop_size,
            eliminate_duplicates=True,
            # sampling=get_sampling(kwargs.pop('sampling', 'real_lhs'))
            sampling=kwargs.pop("sampling", LHS()),
        )
    elif algo == ALGO_NelderMead:
        print("moo.run_optimization Nelder Mead")
        algorithm = NelderMead()
    elif algo == ALGO_PatternSearch:
        print("moo.run_optimization PatternSearch")
        algorithm = PatternSearch()
    elif algo == ALGO_PSO:
        print("moo.run_optimization Particle Swarm")
        algorithm = PSO()
    # elif algo == 'LocalSearch':
    #     print('moo.run_optimization LocalSearch')
    #     algorithm = LocalSearch()
    t0 = time.time()

    termination = MODT(
        xtol=x_tol,
        ftol=f_tol,
        # n_last=n_last, these are expected in MODT... which is weird bc the docs seem to say it is
        # nth_gen=nth_gen,
        n_max_gen=n_max_gen,
        n_max_evals=None,
    )

    # this check no longer works now that kwargs are pass to T3COProblem and dict types are immutable
    # assert len(kwargs) == 0, f'Invalid kwargs: {list(kwargs.keys())}'
    try:
        res = minimize(
            problem,
            algorithm,
            termination=termination,
            seed=1,
            verbose=True,
            save_history=True,
            return_least_infeasible=return_least_infeasible,
            #    display=T3CODisplay()
        )
    except Exception:
        logging.exception(
            f"moo.run_optimization: Optimization errored out for algorithm {algo}"
        )
        res, problem = None, None
        return res, problem, EXCEPTION_THROWN

    t1 = time.time()
    print(f"\nElapsed time for optimization: {t1 - t0} s")
    if verbose:
        print("\nParameter pareto sets:")
    if res.X is None:
        print("moo.run_optimization: moo failed to converge")
        return res, problem, OPTIMIZATION_FAILED_TO_CONVERGE

    # res.X holds results of optimization
    # successful optimization could be 1D (one solution)
    # [1.0, 2.0, 3.0, 4.0, 5.0]
    # or nD, multiple solutions on a pareto front
    # [[1.0, 2.0, 3.0, 4.0, 5.0],
    # [ 6.0, 7.0, 8.0, 9.0, 10.0],
    # [ 11.0,12.0,13.0,14.0,15.0]]
    return res, problem, OPTIMIZATION_SUCCEEDED


# try:
#     ans = 1/0
# except BaseException as ex:
#     # Get current system exception
#     ex_type, ex_value, ex_traceback = sys.exc_info()

#     # Extract unformatter stack traces as tuples
#     trace_back = traceback.extract_tb(ex_traceback)

#     # Format stacktrace
#     stack_trace = list()

#     for trace in trace_back:
#         stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

#     print("Exception type : %s " % ex_type.__name__)
#     print("Exception message : %s" %ex_value)
#     print("Stack trace : %s" %stack_trace)