#!/usr/bin/env python
# coding: utf-8

# %%
import argparse
import ast
import csv
import logging
import os
import re
import time
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from time import gmtime, strftime
from typing import List, Tuple

import fastsim
import numpy as np
import pandas as pd
import pymoo
import pymoo.core
import pymoo.core.result

from t3co.moopack import moo
from t3co.objectives import fueleconomy as fe
from t3co.run import Global as gl
from t3co.run import run_scenario
from t3co.run import run_scenario as rs


def deug_traces(
    vehicle: fastsim.vehicle.Vehicle,
    cycles: List[fastsim.cycle.Cycle],
    scenario: run_scenario.Scenario,
) -> None:
    """
    This function gets a diagnostic trace of get_mpgge

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim Vehicle object
        cycles (List[fastsim.cycle.Cycle]): List of FASTSim drivecycle objects
        scenario (run_scenario.Scenario): Scenario object
    """
    mpgge_comp, sim_drives, mpgges = fe.get_mpgge(
        cycles, vehicle, scenario, diganostic=True
    )
    # save the sim_drives to file somehow


def save_tco_files(
    tco_files: dict, resdir: str, scenario_name: str, sel: str, ts: str
) -> None:
    """
    This function saves the intermediary files as tsv

    Args:
        tco_files (dict): Contains all TCO calculation dataframes
        resdir (str): result directory strong
        scenario_name (str): scenario name
        sel (str): selection(s)
        ts (str): timestring
    """
    scenario_name = re.sub("s", "-", scenario_name)
    scenario_name = re.sub("[^a-zA-Z0-9 \n.]", "", scenario_name)
    tco_files_path = resdir / f"tco_files_{ts}" / f"{sel}_{scenario_name}"
    tco_files_path.mkdir(parents=True, exist_ok=True)

    veh_eff_df = tco_files["veh_eff_df"]
    veh_exp_df = tco_files["veh_exp_df"]
    veh_txp_df = tco_files["veh_txp_df"]
    veh_shr_df = tco_files["veh_shr_df"]
    veh_fxp_df = tco_files["veh_fxp_df"]
    ann_trv_df = tco_files["ann_trv_df"]
    reg_sls_df = tco_files["reg_sls_df"]
    survivl_df = tco_files["survivl_df"]
    veh_spt_df = tco_files["veh_spt_df"]
    stock = tco_files["stock"]
    ownership_costs_df = tco_files["ownership_costs_df"]
    discounted_costs_df = tco_files["discounted_costs_df"]

    veh_eff_df.to_csv(tco_files_path / gl.FUEL_EFF_TSV, sep="\t", index=False)
    veh_exp_df.to_csv(tco_files_path / gl.VEH_EXP_TSV, index=False, sep="\t")
    veh_txp_df.to_csv(tco_files_path / gl.TRAVEL_EXP_TSV, index=False, sep="\t")
    veh_shr_df.to_csv(tco_files_path / gl.MARKET_SHARE_TSV, index=False, sep="\t")
    veh_fxp_df.to_csv(tco_files_path / gl.FUEL_EXPENSE_TSV, index=False, sep="\t")
    ann_trv_df.to_csv(tco_files_path / gl.ANN_TRAVEL_TSV, index=False, sep="\t")
    reg_sls_df.to_csv(tco_files_path / gl.REGIONAL_SALES_TSV, index=False, sep="\t")
    survivl_df.to_csv(tco_files_path / gl.SURVIVAL_TSV, index=False, sep="\t")
    veh_spt_df.to_csv(tco_files_path / gl.FUEL_SPLIT_TSV, index=False, sep="\t")

    stock.to_csv(tco_files_path / "stock_v01.tsv", sep="\t", index=False)
    # emissions.to_csv(                  tco_files_path / 'emissions_v01.tsv', sep='\t', index=False)
    ownership_costs_df.to_csv(
        tco_files_path / "ownership-costs_v01.tsv", sep="\t", index=False
    )
    discounted_costs_df.to_csv(
        tco_files_path / "discounted-ownership-costs_v01.tsv", sep="\t", index=False
    )


def get_knobs_bounds_curves(
    selection: int,
    vpttype: str,
    sdf: pd.DataFrame,
    lw_imp_curves: pd.DataFrame,
    aero_drag_imp_curves: pd.DataFrame,
    eng_eff_curves: pd.DataFrame,
) -> Tuple[dict, dict]:
    """
    This function fetches the knobs and constraints for running the optimization for a given selection

    Args:
        selection (int): selection number
        vpttype (str): vehicle powertrain type = veh_pt_type
        sdf (pd.DataFrame): scenario dataframe
        lw_imp_curves (pd.DataFrame): light weighting curve dataframe
        aero_drag_imp_curves (pd.DataFrame): aero drag curve dataframe
        eng_eff_curves (pd.DataFrame): engine efficiency curve dataframe

    Returns:
        knobs_bounds (dict): dict of knobs and bounds
        curves (dict): dict of lw, aero, and engine efficiency curve parameters
    """
    lw_imp_curves_file = lw_imp_curves.set_index("name")
    aero_drag_imp_curves_file = aero_drag_imp_curves.set_index("name")
    eng_eff_curves_file = eng_eff_curves.set_index("name")
    sd = dict(sdf.loc[selection, :])
    curves = {}

    knobs_bounds = {
        "ess_max_kwh": [sd.get("knob_min_ess_kwh"), sd.get("knob_max_ess_kwh")],
        "mc_max_kw": [sd.get("knob_min_motor_kw"), sd.get("knob_max_motor_kw")],
        "fcMaxOutKw": [sd.get("knob_min_fc_kw"), sd.get("knob_max_fc_kw")],
        "fs_kwh": [sd.get("knob_min_fs_kwh"), sd.get("knob_max_fs_kwh")],
    }

    if (
        "lw_imp_curve_sel" in sd
        and sd["lw_imp_curve_sel"]
        and not pd.isnull(sd["lw_imp_curve_sel"])
    ):
        lw_curve_selection = sd["lw_imp_curve_sel"]
        ltwt_cost_curve = lw_imp_curves_file.loc["ltwt_cost", lw_curve_selection]
        ltwt_pct_curve = lw_imp_curves_file.loc["ltwt_pct", lw_curve_selection]
        wt_delta_perc_knob_max = float(
            lw_imp_curves_file.loc["wt_delta_perc_knob_max", lw_curve_selection]
        )
        wt_delta_perc_knob_min = float(
            lw_imp_curves_file.loc["wt_delta_perc_knob_min", lw_curve_selection]
        )
        assert (
            wt_delta_perc_knob_max <= 1
        ), f"input invalid, value for wt_delta_perc_knob_max must decimal form, got percentage point value as {wt_delta_perc_knob_max}"

        knobs_bounds["wt_delta_perc"] = (wt_delta_perc_knob_min, wt_delta_perc_knob_max)
        curves.update(
            {
                "ltwt_delta_percs": np.array(ast.literal_eval(ltwt_pct_curve)),
                "ltwt_dol_per_kg_costs": np.array(ast.literal_eval(ltwt_cost_curve)),
            }
        )

    if (
        "aero_drag_imp_curve_sel" in sd
        and sd["aero_drag_imp_curve_sel"]
        and not pd.isnull(sd["aero_drag_imp_curve_sel"])
    ):
        cda_curve_selection = sd["aero_drag_imp_curve_sel"]
        CdA_perc_imp_at_which_wt_penalty_maxes_out = float(
            aero_drag_imp_curves_file.loc[
                "CdA_perc_imp_at_which_wt_penalty_maxes_out", cda_curve_selection
            ]
        )
        CdA_perc_imp_knob_max = float(
            aero_drag_imp_curves_file.loc["CdA_perc_imp_knob_max", cda_curve_selection]
        )
        CdA_perc_imp_knob_min = float(
            aero_drag_imp_curves_file.loc["CdA_perc_imp_knob_min", cda_curve_selection]
        )
        cost_a = float(aero_drag_imp_curves_file.loc["cost_a", cda_curve_selection])
        cost_b = float(aero_drag_imp_curves_file.loc["cost_b", cda_curve_selection])
        mass_a = float(aero_drag_imp_curves_file.loc["mass_a", cda_curve_selection])
        mass_b = float(aero_drag_imp_curves_file.loc["mass_b", cda_curve_selection])
        assert (
            CdA_perc_imp_knob_max <= 1
        ), f"input invalid, value for CdA_perc_imp_knob_max must decimal form, got percentage point value as {CdA_perc_imp_knob_max}"
        assert (
            CdA_perc_imp_at_which_wt_penalty_maxes_out <= 1
        ), f"input invalid, value for CdA_perc_imp_at_which_wt_penalty_maxes_out must decimal form, got percentage point value as {CdA_perc_imp_at_which_wt_penalty_maxes_out}"

        knobs_bounds["CdA_perc_imp"] = (CdA_perc_imp_knob_min, CdA_perc_imp_knob_max)
        curves.update(
            {
                "cda_cost_coeff_a": cost_a,
                "cda_cost_coeff_b": cost_b,
                "cda_mass_coeff_a": mass_a,
                "cda_mass_coeff_b": mass_b,
                "cda_perc_imp_at_which_wt_penalty_maxes_out": CdA_perc_imp_at_which_wt_penalty_maxes_out,
            }
        )

    if (
        "eng_eff_imp_curve_sel" in sd
        and sd["eng_eff_imp_curve_sel"]
        and not pd.isnull(sd["eng_eff_imp_curve_sel"])
        and vpttype != gl.BEV
    ):
        # TODO, FCEV should not get eng imp curve parameter
        eng_imp_curve_selection = sd["eng_eff_imp_curve_sel"]
        fc_peak_eff_knob_min = float(
            eng_eff_curves_file.loc["fc_peak_eff_knob_min", eng_imp_curve_selection]
        )
        fc_peak_eff_knob_max = float(
            eng_eff_curves_file.loc["fc_peak_eff_knob_max", eng_imp_curve_selection]
        )
        eng_pctpt = eng_eff_curves_file.loc["eng_pctpt", eng_imp_curve_selection]
        eng_cost = eng_eff_curves_file.loc["eng_cost", eng_imp_curve_selection]
        assert (
            fc_peak_eff_knob_max <= 1
        ), f"input invalid, value for fc_peak_eff_knob_max must decimal form, got percentage point value as {fc_peak_eff_knob_max}"

        curves.update(
            {
                "fc_eff_array": np.array(ast.literal_eval(eng_pctpt)),
                "fc_cost_coeff_array": np.array(ast.literal_eval(eng_cost)),
            }
        )

        knobs_bounds["fc_peak_eff"] = (fc_peak_eff_knob_min, fc_peak_eff_knob_max)

    # validate knobs bounds and remove inactive knobs (user left blank or NA)
    knobs = list(knobs_bounds.keys())
    print("knobs and bounds")
    for k in knobs:
        print(k, knobs_bounds[k][0], knobs_bounds[k][1])
        nans = np.isnan(knobs_bounds[k][0]) or np.isnan(knobs_bounds[k][1])
        if nans or knobs_bounds[k][0] is None or knobs_bounds[k][1] is None:
            del knobs_bounds[k]
    return knobs_bounds, curves


def get_objectives_constraints(
    selection: int, sdf: pd.DataFrame, verbose: bool = True
) -> Tuple[list, list]:
    """
    This function appends to list of necessary variables based on the constraints and objectives selected

    Args:
        selection (int): selection number
        sdf (DataFrame): scenario dataframe
        verbose (bool, optional): if selected, function will print objectives and constraints. Defaults to True.

    Returns:
        objectives (list): list of selected objective variables
        constraints (list): list of selected constraint variables
    """
    sd = dict(sdf.loc[selection, :])
    objectives = []
    constraints = []
    # constraints
    if sd.get("constraint_range") == True:
        constraints.append(moo.RANGE)
    if sd.get("constraint_accel") == True:
        constraints.extend([moo.ACCEL30, moo.ACCEL60])
    if sd.get("constraint_grade") == True:
        constraints.extend([moo.GRADE125, moo.GRADE6])
    if sd.get("constraint_c_rate") == True:
        constraints.append(moo.C_RATE)
    if sd.get("constraint_trace_miss_dist_percent_on") == True:
        constraints.append(moo.TRACE_MISS_DIST_PERCENT)
    if sd.get("constraint_phev_minimize_fuel_use_on") == True:
        constraints.append(moo.PHEV_MINIMIZE_FUEL_USE_CONSTRAINT)
    # objectives
    if sd.get("objective_phev_minimize_fuel_use") == True:
        objectives.append(moo.PHEV_MINIMIZE_FUEL_USE_OBJECTIVE)
    if sd.get("objective_tco") == True:
        objectives.append(moo.TCO)

    if verbose:
        print("objectives:", objectives)
        print("constraints:", constraints)

    return objectives, constraints


def run_moo(
    sel: int,
    sdf: pd.DataFrame,
    optpt: str,
    algo: str,
    skip_opt: bool,
    pop_size: float,
    n_max_gen: int,
    n_last: int,
    nth_gen: int,
    x_tol: float,
    verbose: bool,
    f_tol: float,
    resdir: str,
    lw_imp_curves_df: pd.DataFrame,
    aero_drag_imp_curves_df: pd.DataFrame,
    eng_eff_imp_curves_df: pd.DataFrame,
    config: run_scenario.Scenario,
    **kwargs,
) -> Tuple[pymoo.core.result.Result, moo.T3COProblem, bool]:
    """
    This function calls get_objectives_constraints and get_knobs_bounds_curves, and then calls run_optimization to perform the multiobjective optimization

    Args:
        sel (int): selection number
        sdf (DataFrame): Scenario dataframe
        optpt (str): FASTSim vehicle powertrain type
        algo (str): algorithm name
        skip_opt (bool): skip optimization boolean
        pop_size (int): population size for optimization
        n_max_gen (int): maximum number of generations for optimization
        n_last (int): number of generations to look back for termination
        nth_gen (int): number of generations to evaluate if convergence occurs
        x_tol (float): tolerance in parameter space
        verbose (book): if selected, function prints the optimization process
        f_tol (float): tolerance in objective space
        resdir (str): results directory
        lw_imp_curves_df (DataFrame): light weighting curves dataframe
        aero_drag_imp_curves_df (DataFrame): aero drag curves dataframe
        eng_eff_imp_curves_df (DataFrame): engine efficiency curve dataframe
        config (Config): Config class object

    Returns:
        moo_results (pymoo.core.result.Result): optimization results object
        moo_problem (T3COProblem): minimization problem that calculates TCO
        moo_code (bool): Error message
    """
    objectives, constraints = get_objectives_constraints(sel, sdf)

    knobs_bounds, curve_settings = get_knobs_bounds_curves(
        sel,
        optpt,
        sdf,
        lw_imp_curves_df,
        aero_drag_imp_curves_df,
        eng_eff_imp_curves_df,
    )

    # moo_reults has res.X, res.F np arrays of opt params & objective space resutls, respectively
    moo_results, moo_problem, moo_code = moo.run_optimization(
        pop_size,
        n_max_gen,
        knobs_bounds,
        sel,
        optimize_pt=optpt,
        skip_optimization=skip_opt,
        obj_list=objectives,
        constr_list=constraints,
        verbose=verbose,
        n_last=n_last,
        algo=algo,
        nth_gen=nth_gen,
        x_tol=x_tol,
        f_tol=f_tol,
        config=config,
        **curve_settings,
        **kwargs,
    )
    # return input_vehicle, report_vehicle, report_scenario, out_dict
    return moo_results, moo_problem, moo_code


def check_input_files(df: pd.DataFrame, filetype: str, filepath: str) -> None:
    """
    This function contains assert statements that make sure input vehicle and scenario dataframes do not contain numm rows

    Args:
        df (DataFrame): vehicle or scenario dataframe
        filetype (str): 'vehicle' or 'scenario'
        filepath (str): filepath of the vehicle or scenario input files
    """
    blank_lines = [i for i in df.index.isnull().cumsum() if i != 0]
    assert (
        df.index.isnull().any() == False
    ), f"\n\n{filetype} file selection column cannot have blank values\nlines: {blank_lines}\npath: {filepath}\n\n\n\n"  # noqa: E712
    assert (
        df["scenario_name"].isnull().any() == False
    ), f"\n\n{filetype} file scenario_name column cannot have blank values\nlines: {blank_lines}\npath: {filepath}\n\n\n\n"  # noqa: E712


def skip_scenario(sel, selections, scenario_name, report_kwargs, verbose=False) -> bool:
    """
    This function checks if given selection is present in exclude or look_for selections

    Args:
        sel (float): _description_
        scenario_name (str): scenario name
        verbose (bool, optional): if selected, prints out scenarios that are skipped. Defaults to False.

    Returns:
        bool: if not present, returns True; Else False
    """
    if any(ex in scenario_name for ex in report_kwargs["exclude"]):
        if verbose:
            print(
                f"skipping {sel} {exclude} has parts in scenario_name {scenario_name}"
            )
        return True
    if not any(lf in scenario_name for lf in report_kwargs["look_for"]):
        if verbose:
            print(f"skipping {sel}, want to run from {look_for}")
        return True
    # print(str(sel))
    # print(list(set([selection_id.split("_")[0] for selection_id in selections])))
    sel_set = list(
        set([str(selection_id).split("_")[0] for selection_id in selections])
    )
    if str(sel) not in sel_set:
        if verbose:
            print(f"skipping {sel} not in desired selections:{selections}")
        return True
    return False


def optimize(
    sel: float,
    sdf: pd.DataFrame,
    vdf: pd.DataFrame,
    algo: str,
    report_kwargs: dict,
    REPORT_COLS: dict,
    skip_opt: bool,
    config: run_scenario.Config,
    write_tsv: bool = False,
) -> dict:
    """
    This function runs the optimization for a given selection if skip_opt = False


    Args:
        sel (float): Selection number
        sdf (pd.DataFrame): Dataframe of input scenario file
        vdf (pd.DataFrame): Dataframe of input vehicle file
        algo (str): Multiobjective optimization Algorithm name
        report_kwargs (dict): arguments related to running T3CO
        REPORT_COLS (dict): Results columns dictionary for sorting the T3CO results
        skip_opt (bool): skip optimization. If true, then optimizer is not run.
        config (run_scenario.Config): Config object
        write_tsv (bool, optional): if selected, intermediary dataframes are saved as tsv files.. Defaults to False.

    Returns:
        report_i (dict): Dictionary of T3CO results for given selection
    """
    print(f"sel: {sel}")
    scenario_name = vdf.loc[int(str(sel).split("_")[0]), "scenario_name"]
    print(
        f"\nRunning selection {sel} for scenario {scenario_name} - skip opt = {skip_opt} -algo = {algo}"
    )

    optpt = vdf.loc[int(str(sel).split("_")[0]), "veh_pt_type"]
    ti = time.time()
    # sel = float(sel)
    algo = report_kwargs["algo"]
    x_tol = report_kwargs["x_tol"]
    f_tol = report_kwargs["f_tol"]
    pop_size = report_kwargs["pop_size"]
    n_max_gen = report_kwargs["n_max_gen"]
    n_last = report_kwargs["n_last"]
    nth_gen = report_kwargs["nth_gen"]
    verbose = report_kwargs["verbose"]
    resdir = report_kwargs["resdir"]
    ts = report_kwargs["ts"]
    file_mark = report_kwargs["file_mark"]
    skip_save_veh = report_kwargs["skip_save_veh"]
    gl.vocation_scenario = scenario_name
    if not skip_opt:
        moo_results, moo_problem, moo_code = run_moo(
            sel,
            sdf,
            optpt,
            algo,
            skip_opt,
            pop_size,
            n_max_gen,
            n_last,
            nth_gen,
            x_tol,
            verbose,
            f_tol,
            resdir,
            config.lw_imp_curves_df,
            config.aero_drag_imp_curves_df,
            config.eng_eff_imp_curves_df,
            config,
        )
        num_results = 1
        if moo_code == moo.OPTIMIZATION_SUCCEEDED:
            if moo_results.X.ndim > 1:
                num_results = moo_results.X.shape[0]
                # ensure we're only showing unique solution set solutions
                moo_results.X = np.array(
                    [list(x) for x in set(tuple(x) for x in moo_results.X)]
                )
        if moo_problem is not None:
            input_vehicle = moo_problem.moobasevehicle
            print(f"optimize: {input_vehicle.veh_pt_type}")

            report_vehicle = moo_problem.mooadvancedvehicle
            report_scenario = moo_problem.opt_scenario
        else:
            input_vehicle = rs.get_vehicle(sel, veh_input_path=config.vehicle_file)
            report_vehicle = None
            print(f"optimize: {input_vehicle.veh_pt_type}")
            report_scenario, design_cycle = rs.get_scenario_and_cycle(
                sel, config.scenario_file, a_vehicle=input_vehicle, config=config
            )

        # update records, moo_problem can always be returned unless an exception is thrown above
        if moo_problem is not None:
            moo_problem.compile_reporting_vars()
            if moo_problem.reporting_vars is not None:
                opt_vars_f_name = (
                    f"{file_mark}_{algo}_var_record_selection_{sel}.csv".strip("_")
                )
                moo_problem.reporting_vars.to_csv(resdir / opt_vars_f_name)

    elif skip_opt == True:
        # TODO, is moo_problem.moobasevehicle really the right vehicle here?
        num_results = 1
        moo_code = "NA"
        input_vehicle = rs.get_vehicle(sel, veh_input_path=config.vehicle_file)
        report_scenario, design_cycle = rs.get_scenario_and_cycle(
            sel, config.scenario_file, a_vehicle=input_vehicle, config=config
        )

        outdict = rs.vehicle_scenario_sweep(
            input_vehicle, report_scenario, design_cycle, write_tsv=write_tsv
        )

    # iterate thru all results from run, num_results can singleton [1] from analysis-only runs
    # or an array or a list of arrays from a parato front result
    # res.X holds results of optimization
    # successful optimization could be 1D (one solution)
    # [1.0, 2.0, 3.0, 4.0, 5.0]
    # or nD, multiple solutions on a pareto front or solution set
    # [[1.0, 2.0, 3.0, 4.0, 5.0],
    # [ 6.0, 7.0, 8.0, 9.0, 10.0],
    # [ 11.0,12.0,13.0,14.0,15.0]]
    for i in range(0, num_results):
        full_report = True

        report_i = {k: "" for k in REPORT_COLS.keys()}

        # important, record sets information: the input vehicle, the scenario, and the optimized vehicle result, if applicable
        for config_key in rs.Config.__dict__["__annotations__"].keys():
            if not isinstance(config.__getattribute__(config_key), pd.DataFrame):
                report_i["config_" + config_key] = config.__getattribute__(config_key)

        for scen_key in rs.Scenario.__dict__["__annotations__"].keys():
            report_i["scenario_" + scen_key] = report_scenario.__getattribute__(
                scen_key
            )
        for v_input_k in input_vehicle.__dict__.keys():
            if "value_props" not in v_input_k:
                report_i["input_vehicle_value_" + v_input_k] = (
                    input_vehicle.__getattribute__(v_input_k)
                )
                # we want place-holder blank values for optimization columns even if we're not optimizing
                report_i["optimized_vehicle_value_" + v_input_k] = None

        # remove value props object
        if "optimized_vehicle_value_props" in report_i:
            del report_i["optimized_vehicle_value_props"]
        if "input_vehicle_value_props" in report_i:
            del report_i["input_vehicle_value_props"]

        opt_time = round(time.time() - ti)

        report_i["selection"] = sel
        veh_selection = int(float(str(sel).split("_")[0]))
        report_i["scenario_name"] = vdf.loc[veh_selection, "scenario_name"]
        try:
            report_i["veh_year"] = vdf.loc[veh_selection, "veh_year"]
        except KeyError:
            report_i["veh_year"] = np.nan
        report_i["veh_pt_type"] = vdf.loc[veh_selection, "veh_pt_type"]

        report_i["run_time_[s]"] = opt_time

        report_i["algorithm"] = algo
        n_gens_used = 0
        if not skip_opt:
            if moo_code in [
                moo.EXCEPTION_THROWN,
                moo.OPTIMIZATION_FAILED_TO_CONVERGE,
            ]:
                if moo_code == moo.EXCEPTION_THROWN:
                    report_i["n_gen"] = (
                        "Code Exception thrown"  # TODO, get stacktrace information and add to this
                    )
                elif moo_code == moo.OPTIMIZATION_FAILED_TO_CONVERGE:
                    report_i["n_gen"] = "Optimization Failed to converge"
                report_i = {k: str(v) for k, v in report_i.items()}
                # reports.append(report_i)
                result = report_i["n_gen"]
                logging.info(f"scenario {sel} failed. {result}")
                full_report = False
                return report_i

            elif moo_code == moo.OPTIMIZATION_SUCCEEDED:
                report_i["opt_result_number"] = i + 1
                if moo_results.X.ndim == 1:
                    x = moo_results.X
                else:
                    x = moo_results.X[i, :]

                outdict = moo_problem.get_tco_from_moo_advanced_result(x)

                # Save resulting vehicle model as YAML file
                if not skip_save_veh:
                    sim_drives = outdict["design_cycle_sim_drive_record"]
                    for sd in sim_drives:
                        # sd_name = sd.name
                        # sd = sd.to_rust()
                        sd_file_path = (
                            resdir
                            / "sim_drives"
                            / f"{file_mark}sim_drive_result_{int(sel)}.yaml".strip("_")
                        )
                        sd_file_path.parent.mkdir(parents=True, exist_ok=True)
                        sd.to_file(str(sd_file_path))

                    veh_result = (
                        report_vehicle.to_rust()
                        if not skip_opt
                        else input_vehicle.to_rust()
                    )
                    veh_filepath = (
                        resdir
                        / "vehicles"
                        / f"{file_mark}vehicle_result_{int(sel)}.yaml".strip("_")
                    )
                    veh_filepath.parent.mkdir(parents=True, exist_ok=True)
                    veh_result.to_file(str(veh_filepath))

                x_dixt = {
                    knob: x[moo_problem.knobs.index(knob)] for knob in moo_problem.knobs
                }
                report_i["final_cda_pct"] = x_dixt.get(moo.KNOB_CDA)
                report_i["final_eng_eff_pct"] = x_dixt.get(moo.KNOB_FCPEAKEFF)
                report_i["final_ltwt_pct"] = x_dixt.get(moo.KNOB_WTDELTAPERC)
                report_i["final_max_motor_kw"] = x_dixt.get(moo.KNOB_mc_max_kw)
                report_i["final_battery_kwh"] = x_dixt.get(moo.KNOB_ess_max_kwh)
                report_i["final_max_fc_kw"] = x_dixt.get(moo.KNOB_FCMAXKW)
                report_i["final_fs_kwh"] = x_dixt.get(moo.KNOB_fs_kwh)
                for v_input_k in report_vehicle.__dict__.keys():
                    if "value_props" not in v_input_k:
                        report_i["optimized_vehicle_value_" + v_input_k] = (
                            report_vehicle.__getattribute__(v_input_k)
                        )

                n_gens_used = moo_results.history[-1].n_gen
                report_i["fvals_over_gens"] = [
                    e.opt.get("F")[0] for e in moo_results.history
                ]
                report_i["n_gen"] = n_gens_used
                report_i["max_n_gen"] = n_max_gen
        if full_report:
            (
                tot_cost,
                disc_cost,
                oppy_cost_set,
                discounted_costs_df,
                mpgge,
                veh_cost_set,
                veh_oper_cost_set,
                veh_opp_cost_set,
            ) = (
                outdict["tot_cost"],
                outdict["disc_cost"],
                outdict["opportunity_cost_set"],
                outdict["discounted_costs_df"],
                outdict["mpgge"],
                outdict["veh_msrp_set"],
                outdict["veh_oper_cost_set"],
                outdict["veh_opp_cost_set"],
            )

            print(
                f"selection {sel} {gl.PT_TYPES_NUM_TO_STR[optpt]} opt time [s]",
                opt_time,
            )
            print(
                f"selection {sel} {gl.PT_TYPES_NUM_TO_STR[optpt]} total cost",
                tot_cost,
            )
            print(f"selection {sel} {gl.PT_TYPES_NUM_TO_STR[optpt]} mpgge", mpgge)
            print(
                f"selection {sel} {gl.PT_TYPES_NUM_TO_STR[optpt]} MSRP breakdown",
                veh_cost_set,
            )
            print(
                f"selection {sel} {gl.PT_TYPES_NUM_TO_STR[optpt]} Operating Costs breakdown",
                veh_oper_cost_set,
            )
            print(
                f"selection {sel} {gl.PT_TYPES_NUM_TO_STR[optpt]} Opportunity costs breakdown",
                veh_opp_cost_set,
            )

            disc_cost_agg = discounted_costs_df.groupby("Category").sum(
                numeric_only=True
            )
            report_i["range_ach_mi"] = outdict["primary_fuel_range_mi"]
            report_i["target_range_mi"] = report_scenario.target_range_mi
            report_i["delta_range_mi"] = (
                outdict["primary_fuel_range_mi"] - report_scenario.target_range_mi
            )

            report_i["min_speed_at_6pct_grade_in_5min_ach_mph"] = outdict[
                "grade_6_mph_ach"
            ]
            report_i["target_min_speed_at_6pct_grade_in_5min_mph"] = (
                report_scenario.min_speed_at_6pct_grade_in_5min_mph
            )
            report_i["delta_min_speed_at_6pct_grade_in_5min_mph"] = (
                outdict["grade_6_mph_ach"]
                - report_scenario.min_speed_at_6pct_grade_in_5min_mph
            )

            report_i["min_speed_at_1p25pct_grade_in_5min_ach_mph"] = outdict[
                "grade_1_25_mph_ach"
            ]
            report_i["target_min_speed_at_1p25pct_grade_in_5min_mph"] = (
                report_scenario.min_speed_at_1p25pct_grade_in_5min_mph
            )
            report_i["delta_min_speed_at_1p25pct_grade_in_5min_mph"] = (
                outdict["grade_1_25_mph_ach"]
                - report_scenario.min_speed_at_1p25pct_grade_in_5min_mph
            )

            report_i["max_time_0_to_60mph_at_gvwr_ach_s"] = outdict["zero_to_60_loaded"]
            report_i["target_max_time_0_to_60mph_at_gvwr_s"] = (
                report_scenario.max_time_0_to_60mph_at_gvwr_s
            )
            if (
                outdict["zero_to_60_loaded"] is not None
            ):  # cannot calculate if it is none (but for some reason, range and grade are handled when none)
                report_i["delta_max_time_0_to_60mph_at_gvwr_s"] = (
                    outdict["zero_to_60_loaded"]
                    - report_scenario.max_time_0_to_60mph_at_gvwr_s
                )

            report_i["max_time_0_to_30mph_at_gvwr_ach_s"] = outdict["zero_to_30_loaded"]
            report_i["target_max_time_0_to_30mph_at_gvwr_s"] = (
                report_scenario.max_time_0_to_30mph_at_gvwr_s
            )
            if (
                outdict["zero_to_30_loaded"] is not None
            ):  # cannot calculate if it is none (but for some reason, range and grade are handled when none)
                report_i["delta_max_time_0_to_30mph_at_gvwr_s"] = (
                    outdict["zero_to_30_loaded"]
                    - report_scenario.max_time_0_to_30mph_at_gvwr_s
                )

            report_i.update(mpgge)
            # report_i["payload_capacity_loss_kg"] = outdict["payload_capacity_loss_kg"] This might be a good var to have
            report_i["payload_cap_cost_multiplier"] = veh_opp_cost_set[
                "payload_cap_cost_multiplier"
            ]
            report_i["total_fueling_dwell_time_hr"] = sum(
                veh_opp_cost_set["net_fueling_dwell_time_hr_per_yr"]
            )
            report_i["total_mr_downtime_hr"] = sum(
                veh_opp_cost_set["net_mr_downtime_hr_per_yr"]
            )
            report_i["total_downtime_hr"] = sum(
                veh_opp_cost_set["total_downtime_hr_per_yr"]
            )
            report_i["fueling_dwell_labor_cost_dol"] = disc_cost_agg.loc[
                "fueling labor cost", "Discounted Cost [$]"
            ]
            report_i["fueling_downtime_oppy_cost_dol"] = disc_cost_agg.loc[
                "fueling downtime cost", "Discounted Cost [$]"
            ]
            report_i["mr_downtime_oppy_cost_dol"] = disc_cost_agg.loc[
                "MR downtime cost", "Discounted Cost [$]"
            ]
            report_i["discounted_downtime_oppy_cost_dol"] = oppy_cost_set[
                "discounted_downtime_oppy_cost_dol"
            ]

            report_i["payload_capacity_cost_dol"] = oppy_cost_set[
                "payload_capacity_cost_dol"
            ]
            report_i["glider_cost_dol"] = veh_cost_set["Glider"]
            report_i["fuel_converter_cost_dol"] = veh_cost_set["Fuel converter"]
            report_i["fuel_storage_cost_dol"] = veh_cost_set["Fuel Storage"]
            report_i["motor_control_power_elecs_cost_dol"] = veh_cost_set[
                "Motor & power electronics"
            ]
            report_i["plug_cost_dol"] = veh_cost_set["Plug"]
            report_i["battery_cost_dol"] = veh_cost_set["Battery"]
            report_i["purchase_tax_dol"] = veh_cost_set["Purchase tax"]
            report_i["msrp_total_dol"] = veh_cost_set["msrp"]
            report_i["insurance_cost_dol"] = disc_cost_agg.loc[
                "insurance", "Discounted Cost [$]"
            ]
            report_i["residual_cost_dol"] = disc_cost_agg.loc[
                "residual cost", "Discounted Cost [$]"
            ]
            report_i["total_fuel_cost_dol"] = disc_cost_agg.loc[
                "Fuel", "Discounted Cost [$]"
            ]

            report_i["total_maintenance_cost_dol"] = disc_cost_agg.loc[
                "maintenance", "Discounted Cost [$]"
            ]
            report_i["discounted_tco_dol"] = disc_cost

            if outdict["design_cycle_sim_drive_record"] is not None:
                report_i["design_cycle_EA_err"] = {
                    sdr.cyc.name: sdr.energy_audit_error
                    for sdr in outdict["design_cycle_sim_drive_record"]
                }
                report_i["design_cyc_trace_miss_dist_frac"] = {
                    sdr.cyc.name: sdr.trace_miss_dist_frac
                    for sdr in outdict["design_cycle_sim_drive_record"]
                }
                report_i["design_cyc_trace_miss_time_frac"] = {
                    sdr.cyc.name: sdr.trace_miss_time_frac
                    for sdr in outdict["design_cycle_sim_drive_record"]
                }
                report_i["design_cyc_trace_miss_speed_mps"] = {
                    sdr.cyc.name: sdr.trace_miss_speed_mps
                    for sdr in outdict["design_cycle_sim_drive_record"]
                }
            if outdict["accel_sim_drive_record"] is not None:
                report_i["accel_EA_err"] = outdict[
                    "accel_sim_drive_record"
                ].energy_audit_error
            if outdict["accel_loaded_sim_drive_record"] is not None:
                report_i["accel_loaded_EA_err"] = outdict[
                    "accel_loaded_sim_drive_record"
                ].energy_audit_error
            if outdict["grade_6_sim_drive_record"] is not None:
                report_i["grade_6_EA_err"] = outdict[
                    "grade_6_sim_drive_record"
                ].energy_audit_error
            if outdict["grade_1p25_sim_drive_record"] is not None:
                report_i["grade_1p25_EA_err"] = outdict[
                    "grade_1p25_sim_drive_record"
                ].energy_audit_error

        # for all vehicles, save their final TCO TSV files
        if write_tsv:
            save_tco_files(outdict["tco_files"], resdir, scenario_name, sel, ts)

        report_i = {k: str(v) for k, v in report_i.items()}
    return report_i


def run_vehicle_scenarios(
    config: run_scenario.Config,
    REPORT_COLS: dict,
    **kwargs,
) -> Tuple[List[int | str], pd.DataFrame, pd.DataFrame, bool, dict, dict]:
    """
    This function reads the input files, validates inputs, compiles the selections, and returns a clean set of inputs that are needed for the current analysis.


    Args:
        config (Config): Config object containing analysis attributes and scenario attribute overrides
        REPORT_COLS (dict): Dictionary of reporting columns from T3CO

    Raises:
        Exception: input validation error
        Exception: optimization error

    Returns:
        selections, vdf, sdf, skip_all_opt, report_kwargs, REPORT_COLS (Tuple[List[int|str], pd.DataFrame, pd.DataFrame, bool, dict, dict]): Selections list, vehicle dataframe, scenario dataframe, skip all optimization, report arguments, and report columns
    """
    vdf = pd.read_csv(config.vehicle_file, index_col="selection", skip_blank_lines=True)
    sdf = pd.read_csv(
        config.scenario_file, index_col="selection", skip_blank_lines=True
    )
    check_input_files(vdf, "vehicles", config.vehicle_file)
    check_input_files(sdf, "scenario", config.scenario_file)
    config.eng_eff_imp_curves_df = pd.read_csv(config.eng_eff_imp_curves)
    config.lw_imp_curves_df = pd.read_csv(config.lw_imp_curves)
    config.aero_drag_imp_curves_df = pd.read_csv(config.aero_drag_imp_curves)

    # optimization scenario parameters where we get our baseline vehicle and scenario
    global FASTSIM_INPUTS, OTHER_INPUTS
    FASTSIM_INPUTS = config.vehicle_file
    OTHER_INPUTS = config.scenario_file
    print("vehicle src:", config.vehicle_file)
    print("scenario src:", config.scenario_file)

    for scen_key in rs.Scenario.__dict__["__annotations__"].keys():
        REPORT_COLS.update({"scenario_" + scen_key: ""})

    df = pd.read_csv(FASTSIM_INPUTS)

    for vc in df.columns.tolist():
        REPORT_COLS.update({"optimized_vehicle_value_" + vc: ""})

    for vc in df.columns.tolist():
        REPORT_COLS.update({"input_vehicle_value_" + vc: ""})

    # optimizer and sweep tuning
    report_kwargs = dict(kwargs)
    n_max_gen = kwargs.pop(
        "n_max_gen", 100
    )  # max number of generations if convergence not met
    pop_size = kwargs.pop("pop_size", 30)  # population of each generation
    nth_gen = kwargs.pop(
        "nth_gen", 1
    )  # period of generations in which to evaluate if convergence happens
    algorithms = kwargs.pop("algo")
    n_last = kwargs.pop(
        "n_last", 5
    )  # number of generations to look back for establishing convergence
    x_tol = kwargs.pop("x_tol", 0.5)  # parameter space tolerance
    f_tol = kwargs.pop("f_tol", 3.0)  # objective space tolerance
    verbose = kwargs.pop("verbose", False)
    look_for = kwargs.pop("look_for", [""])
    assert isinstance(
        look_for, list
    ), "look_for should have been input or cast as a list at this point"
    selections = kwargs.pop(
        "selections", -1
    )  # list of integers representing scenario selections, ex: [34,35,36]
    exclude = kwargs.pop("exclude", [">{-<>-}<"])
    dir_mark = kwargs.pop("dir_mark", "")
    file_mark = kwargs.pop("file_mark", "")
    skip_save_veh = kwargs.pop("skip_save_veh")
    skip_all_opt = kwargs.pop("skip_all_opt")
    do_input_validation = kwargs.pop("do_input_validation")
    write_tsv = kwargs.pop("do_input_validation", False)

    report_kwargs["n_max_gen"] = n_max_gen
    report_kwargs["pop_size"] = pop_size
    report_kwargs["nth_gen"] = nth_gen
    report_kwargs["algorithms"] = algorithms
    report_kwargs["n_last"] = n_last
    report_kwargs["look_for"] = look_for
    report_kwargs["selections"] = selections
    report_kwargs["exclude"] = exclude
    report_kwargs["dir_mark"] = dir_mark
    report_kwargs["file_mark"] = file_mark
    report_kwargs["skip_save_veh"] = skip_save_veh
    report_kwargs["skip_all_opt"] = skip_all_opt
    report_kwargs["do_input_validation"] = do_input_validation
    report_kwargs["write_tsv"] = write_tsv
    report_kwargs["verbose"] = verbose

    if not file_mark.endswith("_"):
        file_mark += "_"
    report_kwargs["file_mark"] = file_mark
    # results dir setup
    ts = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    report_kwargs["ts"] = ts
    report_kwargs["skip_save_veh"] = skip_save_veh

    if config.resfile_suffix is not None:
        RES_FILE = f"{file_mark}results_{ts}_{str(config.resfile_suffix)}.csv".strip(
            "_"
        )
    else:
        selections_string = (
            str(selections)
            .strip("[]")
            .replace(" ", "")
            .replace("'", "")
            .replace(",", "-")
        )
        RES_FILE = f"{file_mark}results_{ts}_sel_{selections_string[:20]}.csv".strip(
            "_"
        )
    report_kwargs["RES_FILE"] = RES_FILE
    if selections == -1:
        selections = vdf.index

    if args.dst_dir is None and config.dst_dir is None:
        resdir = Path(os.path.abspath(__file__)).parents[1] / f"results{dir_mark}"
    elif args.dst_dir is not None:
        resdir = Path(args.dst_dir)
    else:
        resdir = Path(config.dst_dir)

    if not resdir.exists():
        resdir.mkdir(parents=True)

    report_kwargs["resdir"] = resdir

    # with open(str(resdir / RES_FILE), "a", newline="") as f:
    #     print("writing to ", resdir / RES_FILE)
    #     writer = csv.writer(f)
    #     writer.writerow(REPORT_COLS.keys())

    loggingfname = Path(
        str(Path(resdir / f"{file_mark}sweep_error_log_{ts}.log")).strip("_")
    )
    logging.basicConfig(
        filename=loggingfname,
        level=logging.INFO,
        filemode="a",
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-8s %(message)s",
        force=True,
    )
    logging.info(f"kwargs {report_kwargs}")

    # list of report dataframes to write final output at each iteration

    def input_validation(
        sel: float, optpt: str, algo: str, config: run_scenario.Config
    ) -> None:
        """
        This function obtains the vehicle, scenario, and cycle object for a given selection and runs optimization to validate inputs

        Args:
            sel (float): selection number
            optpt (str): vehicle powertrain type
            algo (str): algorithm name
            config (Config): Config object

        Returns:
            None: None
        """
        v = rs.get_vehicle(
            sel,
            veh_input_path=config.vehicle_file,
        )
        print(f"input_validation: {sel} {v.veh_pt_type}")
        s, c = rs.get_scenario_and_cycle(
            sel,
            config.scenario_file,
            a_vehicle=v,
            config=config,
            do_input_validation=True,
        )
        rs.check_phev_init_socs(v, s)

        knobs_bounds, curve_settings = get_knobs_bounds_curves(
            sel,
            optpt,
            sdf,
            config.lw_imp_curves_df,
            config.aero_drag_imp_curves_df,
            config.eng_eff_imp_curves_df,
        )
        objectives, constraints = get_objectives_constraints(sel, sdf, verbose=False)

        _ = moo.run_optimization(
            pop_size,
            n_max_gen,
            knobs_bounds,
            sel,
            optimize_pt=optpt,
            skip_optimization=True,
            obj_list=objectives,
            constr_list=constraints,
            verbose=verbose,
            n_last=n_last,
            algo=algo,
            nth_gen=nth_gen,
            x_tol=x_tol,
            f_tol=f_tol,
            config=config,
            do_input_validation=True,
            **curve_settings,
            **kwargs,
        )
        return None

    if do_input_validation:
        st = time.time()
        print("sweep:: Running input validation...")
        badinputs = False
        noinputs = True
        for sel, scenario_name, optpt in zip(
            vdf.index, vdf["scenario_name"], vdf["veh_pt_type"]
        ):
            if skip_scenario(
                sel,
                selections,
                scenario_name,
                report_kwargs=report_kwargs,
                verbose=False,
            ):
                # print(f'input_validation skip selection: {sel}')
                continue

            for algo in algorithms:
                try:
                    algopart = f"algorithm: {algo.rjust(15)} or None if skipping"
                    print(
                        f"sweep:: validating input {sel}:{scenario_name}".ljust(90),
                        algopart,
                    )
                    # print(f'config: {config}')

                    input_validation(sel, optpt, algo, config)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    badinputs = True
                    logging.exception(
                        f"sweep:: INPUT ERROR selection {sel}, {scenario_name} :: {e}",
                        stack_info=False,
                        exc_info=True,
                    )
                noinputs = False
        print(f"sweep:: Finished input validation, time [s] {round(time.time()-st)}")
        if badinputs:
            raise Exception(
                f"sweep:: input_validation failure, see log file!\n{loggingfname}"
            )
        if noinputs:
            raise Exception(
                f"sweep:: no inputs available, see log file!\n{loggingfname}"
            )

    return selections, vdf, sdf, skip_all_opt, report_kwargs, REPORT_COLS


def run_optimize_analysis(
    sel: str | int,
    vdf: pd.DataFrame,
    sdf: pd.DataFrame,
    skip_all_opt: bool,
    config: run_scenario.Config,
    report_kwargs: dict,
    REPORT_COLS: dict,
) -> dict:
    """
    This function runs the optimization function based on skip_all_opt input to return the report_i dictionary with T3CO results for each selection.

    Args:
        sel (str | int): selection number
        vdf (pd.DataFrame): Dataframe of input vehicle file
        sdf (pd.DataFrame): Dataframe of input scenario file
        skip_all_opt (bool): Skip all optimization. If true, then the optimizer is not run for any scenario
        config (run_scenario.Config): Config object
        report_kwargs (dict): Dictionary of args required for running T3CO
        REPORT_COLS (dict): Dictionary of reporting columns from T3CO

    Returns:
        report_i (dict): Dictionary of T3CO results for given selection
    """
    if skip_all_opt is True or skip_all_opt == "TRUE":
        report_i = optimize(
            sel=sel,
            sdf=sdf,
            vdf=vdf,
            algo="None",
            report_kwargs=report_kwargs,
            REPORT_COLS=REPORT_COLS,
            skip_opt=True,
            config=config,
            write_tsv=False,
        )
    else:
        for algo in algorithms:
            print(f"run optimize {sel}")
            report_i = optimize(
                sel=sel,
                sdf=sdf,
                vdf=vdf,
                algo=algo,
                report_kwargs=report_kwargs,
                REPORT_COLS=REPORT_COLS,
                skip_opt=False,
                config=config,
                write_tsv=False,
            )

    logging.info(f"done with selection {sel}: {report_i['scenario_name']}")

    return report_i


if __name__ == "__main__":
    start = time.time()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="SWEEP",
        description="""The sweep.py module is the main script to run T3CO""",
    )
    parser.add_argument(
        "--config",
        default=gl.SWEEP_PATH.parents[0] / "resources/T3COConfig.csv",
        type=str,
        help="Input Config file",
    )
    parser.add_argument(
        "--analysis-id",
        default=0,
        type=int,
        help="Analysis key from input Config file - 'config.analysis_id'",
    )
    # input files
    parser.add_argument(
        "--vehicles",
        default=gl.SWEEP_PATH.parents[0]
        / "resources/inputs/demo/Demo_FY22_vehicle_model_assumptions.csv",
        type=str,
        help="Input file for Vehicle models",
    )
    parser.add_argument(
        "--scenarios",
        default=gl.SWEEP_PATH.parents[0]
        / "resources/inputs/demo/Demo_FY22_scenario_assumptions.csv",
        type=str,
        help="Input file for Scenario models",
    )
    parser.add_argument(
        "--selections",
        type=str,
        nargs="*",
        help="""Selections desired to run. Selections can be an int, or list of ints, or range expression. Ex: --selections 234 or --selections "[234,236,238]" or --selections "range(234, 150, 2)" """,
    )
    parser.add_argument(
        "--eng-curves",
        default=gl.SWEEP_PATH.parents[0]
        / "resources/auxiliary/EngineEffImprovementCostCurve.csv",
        type=str,
        help="Input file for engine efficiency improvement cost curves",
    )
    parser.add_argument(
        "--lw-curves",
        default=gl.SWEEP_PATH.parents[0]
        / "resources/auxiliary/LightweightImprovementCostCurve.csv",
        type=str,
        help="Input file for lightweighting improvement cost curves",
    )
    parser.add_argument(
        "--aero-curves",
        default=gl.SWEEP_PATH.parents[0]
        / "resources/auxiliary/AeroDragImprovementCostCurve.csv",
        type=str,
        help="Input file for aerodynamics improvement curves",
    )

    parser.add_argument(
        "--look-for",
        default="",
        type=str,
        help="A string for string matching, example --look_for 'FCEV' or -look_for '[\"FCEV\", \"HEV\"]' ",
    )
    parser.add_argument(
        "--skip-all-opt",
        "--skopt",
        action="store_true",
        help="If --skip_all_opt used, all runs skip optimization",
    )
    parser.add_argument(
        "--skip-input-validation",
        "--skiv",
        action="store_false",
        help="If --skip_input_validation used, no pre-validation of inputs is run before sweep commences",
    )
    parser.add_argument(
        "--exclude",
        default=">{-<>-}<",
        type=str,
        nargs="*",
        help="Overrides -look_for. a string for string matching to exclude runs, example -exclude 'FCEV' or -look_for '[\"FCEV\", \"HEV\"]'  ",
    )
    parser.add_argument(
        "--algorithms",
        "--algos",
        "--algo",
        default="NSGA2",
        type=str,
        nargs="*",
        help=f'Enter algorithm or list of algorithms, or "ensemble" to use all, to use for optimization: {moo.ALGORITHMS} ex: -algos PatternSearch | -algos \'["PatternSearch", "NSGA2"]\' | -algos "ensemble" ',
    )
    parser.add_argument(
        "--dst-dir",
        default=Path(os.path.abspath(__file__)).parents[1] / "results",
        type=str,
        help="Directory to store T3CO results",
    )
    parser.add_argument(
        "--dir-mark",
        default="",
        type=str,
        help="Name for results directory in addition to timestamp",
    )
    parser.add_argument(
        "--file-mark",
        default="",
        type=str,
        help="Prefix to add to the result file names",
    )
    parser.add_argument(
        "--skip-save-veh",
        action="store_true",
        help="Toggle result vehicle model YAML file saving off",
    )
    parser.add_argument(
        "--x-tol",
        default=0.001,
        type=float,
        help="Parameter space tolerance for optimization",
    )  # bigger = more lax # TODO: we need to investigate if this is too big of a default
    parser.add_argument(
        "--f-tol",
        default=0.001,
        type=float,
        help="Objective space tolerance for optimzation",
    )  # bigger = more lax # TODO: we need to investigate if this is too big of a default
    parser.add_argument(
        "--n-max-gen",
        default=1000,
        type=float,
        help="Max number of optimizer iterations regardless of algorithm",
    )
    parser.add_argument("--pop-size", default=25, help="population of each generation")
    parser.add_argument(
        "--nth-gen",
        default=1,
        type=int,
        help="Period of generations in which to evaluate if convergence happens during optimization",
    )
    parser.add_argument(
        "--n-last",
        default=5,
        type=int,
        help="Number of generations to look back for establishing convergence during optimization",
    )
    parser.add_argument(
        "--range-overshoot-tol",
        default=None,
        type=float,
        help="Range overshoot tolerance, example '0.20' allows 20%% range overshoot. Default of 'None' does not constrain overshoot.",
    )
    # time-dilation-args passed to T3COProblem instantiation for optimization usage
    parser.add_argument(
        "---missed-trace-correction",
        action="store_true",
        help="Activate FASTSim time-dilation to correct missed trace",
    )
    parser.add_argument(
        "--max-time-dilation",
        default=10,
        type=int,
        help="Maximum time dilation factor to 'catch up' with trace  ",
    )
    parser.add_argument(
        "--min-time-dilation",
        default=0.1,
        type=float,
        help="Minimum time dilation to let trace 'catch up' ",
    )
    parser.add_argument(
        "--time-dilation-tol",
        default=1e-3,
        type=float,
        help="Convergence criteria for time dilation",
    )

    parser.add_argument(
        "--write-tsv",
        default=False,
        type=bool,
        help="Boolean toggle to save intermediary .TSV cost results files",
    )

    parser.add_argument(
        "--run-multi",
        action="store_true",
        help="Boolean switch to select multiprocessing version",
    )
    parser.add_argument(
        "--n-processors",
        type=int,
        help="Number of processors to use for multiprocessing",
        default=9,
    )

    args = parser.parse_args()
    print(f"Sweep file path: {gl.SWEEP_PATH}")

    # selections can be an int, or list of ints, or range expression
    if args.config is None:
        if args.selections is None:
            selections = -1
        elif ("[" in args.selections and "]" in args.selections) or (
            "(" in args.selections and ")" in args.selections
        ):
            selections = ast.literal_eval(args.selections)
        else:
            selections = [int(args.selections)]
        config = rs.Config()
        config.vehicle_file = Path(args.vehicles)
        config.scenario_file = Path(args.scenarios)
        config.eng_eff_imp_curves = Path(args.eng_eff_imp_curves)
        config.lw_imp_curves = Path(args.lw_imp_curves)
        config.aero_drag_imp_curves = Path(args.aero_drag_imp_curves)
        write_tsv = args.write_tsv
    else:
        try:
            config = rs.Config()
            config.from_file(filename=Path(args.config), analysis_id=args.analysis_id)
        except ValueError:
            print(f"Config analysis_id not valid: {args.analysis_id}")
            config = rs.Config()
            config.validate_analysis_id(filename=Path(args.config))
        config.check_drivecycles_and_create_selections(args.config)
        selections = config.selections
        config.vehicle_file = Path(args.config).parent / config.vehicle_file
        config.scenario_file = Path(args.config).parent / config.scenario_file
        config.eng_eff_imp_curves = Path(args.config).parent / config.eng_eff_imp_curves
        config.lw_imp_curves = Path(args.config).parent / config.lw_imp_curves
        config.aero_drag_imp_curves = (
            Path(args.config).parent / config.aero_drag_imp_curves
        )
        write_tsv = config.write_tsv

    look_for = args.look_for
    exclude = args.exclude
    if "[" in look_for:
        look_for = ast.literal_eval(look_for)
    else:
        look_for = [look_for]
    if "[" in exclude:
        exclude = ast.literal_eval(exclude)
    else:
        exclude = [exclude]

    if args.algorithms == "ensemble":
        algorithms = moo.ALGORITHMS
    elif "[" in args.algorithms and "]" in args.algorithms:
        algorithms = ast.literal_eval(args.algorithms)
    elif config.algorithms is not None:
        algorithms = config.algorithms
    else:
        algorithms = args.algorithms

    kwargs = {
        "selections": selections,
        "look_for": look_for,
        "exclude": exclude,
        "algo": algorithms,
        "dir_mark": args.dir_mark,
        "file_mark": args.file_mark.replace(".csv", ""),
        "skip_save_veh": args.skip_save_veh,
        "x_tol": float(args.x_tol),
        "f_tol": float(args.f_tol),
        "n_max_gen": int(args.n_max_gen),
        "pop_size": int(args.pop_size),
        "nth_gen": int(args.nth_gen),
        "n_last": int(args.n_last),
        "skip_all_opt": args.skip_all_opt
        if args.config is None
        else config.skip_all_opt,
        "do_input_validation": args.skip_input_validation,
        "range_overshoot_tol": float(args.range_overshoot_tol)
        if args.range_overshoot_tol is not None
        else None,
        "write_tsv": write_tsv,
    }
    if args.missed_trace_correction:
        kwargs.update(
            {
                "max_time_dilation": float(args.max_time_dilation),
                "min_time_dilation": float(args.min_time_dilation),
                "time_dilation_tol": float(args.time_dilation_tol),
                "missed_trace_correction": bool(args.missed_trace_correction),
            }
        )

    REPORT_COLS = {
        "selection": "",
        "scenario_name": "",
        "veh_year": "",
        "veh_pt_type": "",
        "pareto_front_number": "",
        "run_time_[s]": "",
        "algorithm": "",
        "n_gen": "",
        "fvals_over_gens": "",
        "design_cyc_trace_miss_dist_frac": "",
        "design_cyc_trace_miss_time_frac": "",
        "design_cyc_trace_miss_speed_mps": "",
        "design_cycle_EA_err": "",
        "accel_EA_err": "",
        "accel_loaded_EA_err": "",
        "grade_6_EA_err": "",
        "grade_125_EA_err": "",
        "final_cda_pct": "",
        "final_eng_eff_pct": "",
        "final_ltwt_pct": "",
        "final_max_motor_kw": "",
        "final_battery_kwh": "",
        "final_max_fc_kw": "",
        "final_fs_kwh": "",
        "minSpeed6PercentGradeIn5minAch": "",
        "target_minSpeed6PercentGradeIn5min": "",
        "delta_6PercentGrade": "",
        "minSpeed1point25PercentGradeIn5minAch": "",
        "target_minSpeed1point25PercentGradeIn5min": "",
        "delta_1point25PercentGrade": "",
        "max0to60secAtGVWRAch": "",
        "target_max0to60secAtGVWR": "",
        "delta_0to60sec": "",
        "max0to30secAtGVWRAch": "",
        "target_max0to30secAtGVWR": "",
        "delta_0to30sec": "",
    }
    selections, vdf, sdf, skip_all_opt, report_kwargs, REPORT_COLS = (
        run_vehicle_scenarios(config, REPORT_COLS=REPORT_COLS, **kwargs)
    )
    selections_list = []
    for sel, scenario_name, optpt in zip(
        vdf.index, vdf["scenario_name"], vdf["veh_pt_type"]
    ):
        if skip_scenario(sel, selections, scenario_name, report_kwargs=report_kwargs):
            continue
        scen_df = dict(sdf.loc[sel, :])
        skip_opt = scen_df.get("skip_opt", False)
        try:
            if config.dc_files:
                sel_list = [
                    scenario_selection
                    for scenario_selection in config.selections
                    if str(scenario_selection).split("_")[0] == str(sel)
                ]
                print(f"Selections List: {sel_list}")
                selections_list.extend(sel_list)
                print(scenario_name)
            else:
                selections_list = [sel]
        except:
            logging.exception("Fatal Error")
            raise

    print(f"Selections List final: {selections_list}")
    resdir = Path(report_kwargs["resdir"])
    RES_FILE = report_kwargs["RES_FILE"]

    if args.run_multi:
        print(f"Running multiprocessing version of T3CO")
        with Pool(processes=9) as pool:
            # call the same function with different data in parallel
            # for result in tqdm(pool.map(partial(read_file, root = root),files), total= len(files)):
            reports = []
            # reports_df =  pd.DataFrame()

            for report_i in pool.imap_unordered(
                partial(
                    run_optimize_analysis,
                    vdf=vdf,
                    sdf=sdf,
                    skip_all_opt=skip_all_opt,
                    config=config,
                    report_kwargs=report_kwargs,
                    REPORT_COLS=REPORT_COLS,
                ),
                selections_list,
            ):
                reports.append(report_i)
                k = len(reports)
                if (k % 20 == 0 or k == 4) and (len(selections_list) != 1 and k != 0):
                    reports_df = pd.DataFrame(reports)
                    reports_df.sort_values(by=["selection"], inplace=True)
                    reports_df.to_csv(resdir / RES_FILE, index=False, header=True)
                    print(
                        f"\nSaving intermediate results to {str(resdir / RES_FILE)}\n"
                    )
                print(f"Number of files done: {k}/{len(selections_list)}")

            pool.close()
            pool.join()

            reports_df = pd.DataFrame(reports)
            reports_df.sort_values(by=["selection"], inplace=True)
            print(reports_df.head(5))
            try:
                reports_df.to_csv(resdir / RES_FILE, index=False, header=True)
            except PermissionError:
                reports_df.to_csv(resdir / ("alternate_" + RES_FILE), index=False)
                print(f"Could not write file {resdir / RES_FILE}, file open")
        print("writing to ", resdir / RES_FILE)

    else:
        reports = []
        print(f"selections_list: {selections_list}")
        for sel in selections_list:
            report_i = run_optimize_analysis(
                sel,
                vdf=vdf,
                sdf=sdf,
                skip_all_opt=skip_all_opt,
                config=config,
                report_kwargs=report_kwargs,
                REPORT_COLS=REPORT_COLS,
            )
            reports.append(report_i)
        reports_df = pd.DataFrame(reports)
        reports_df.sort_values(by=["selection"], inplace=True)
        print(reports_df.head(5))
        try:
            if os.path.exists(resdir / RES_FILE):
                reports_df.to_csv(
                    resdir / RES_FILE, index=False, mode="a", header=False
                )
            else:
                reports_df.to_csv(resdir / RES_FILE, index=False, header=True)
        except PermissionError:
            reports_df.to_csv(resdir / ("alternate_" + RES_FILE), index=False)
            print(f"Could not write file {resdir / RES_FILE}, file open")
        print("writing to ", resdir / RES_FILE)

    end = time.time()

    logging.info("T3CO finished")
    print(f"T3CO finished in {end-start}s")


# %%
