#%%
import pandas as pd
import os

from t3co.visualization.charts import T3COCharts
import ast
from functools import partial
import logging
from multiprocessing.pool import Pool
from pathlib import Path
import time
from t3co.run import run_scenario as rs
from t3co.moopack import moo
from t3co import sweep

def run_t3co(analysis_id, config_filename, run_multi=False, save_results=False):
    start = time.time()
    try:
        config = rs.Config()
        config.from_file(filename=Path(config_filename), analysis_id=analysis_id)
    except ValueError:
        print(f"Config analysis_id not valid: {analysis_id}")
        config = rs.Config()
        config.validate_analysis_id(filename=Path(config_filename))
    config.check_drivecycles_and_create_selections(config_filename)
    selections = config.selections
    config.vehicle_file = Path(config_filename).parent / config.vehicle_file
    config.scenario_file = Path(config_filename).parent / config.scenario_file
    config.eng_eff_imp_curves = Path(config_filename).parent / config.eng_eff_imp_curves
    config.lw_imp_curves = Path(config_filename).parent / config.lw_imp_curves
    config.aero_drag_imp_curves = (
        Path(config_filename).parent / config.aero_drag_imp_curves
    )
    write_tsv = config.write_tsv

    look_for = ""
    exclude = ">{-<>-}<"

    if "[" in look_for:
        look_for = ast.literal_eval(look_for)
    else:
        look_for = [look_for]
    if "[" in exclude:
        exclude = ast.literal_eval(exclude)
    else:
        exclude = [exclude]

    if config.algorithms == "ensemble":
        algorithms = moo.ALGORITHMS
    elif "[" in config.algorithms and "]" in config.algorithms:
        algorithms = ast.literal_eval(config.algorithms)
    elif config.algorithms is not None:
        algorithms = config.algorithms
    else:
        algorithms = config.algorithms
    missed_trace_correction = True
    kwargs = {
        "selections": selections,
        "look_for": look_for,
        "exclude": exclude,
        "algo": algorithms,
        "dir_mark": "",
        "dst_dir":  (Path(os.path.abspath(__file__)).parents[1] / "results" if config.dst_dir is None else  config.dst_dir),
        "file_mark": "".replace(".csv", ""),
        "skip_save_veh": True,
        "x_tol": float(0.001),
        "f_tol": float(0.001),
        "n_max_gen": int(1000),
        "pop_size": int(25),
        "nth_gen": int(1),
        "n_last": int(5),
        "skip_all_opt": config.skip_all_opt,
        "do_input_validation": False,
        "range_overshoot_tol": None,
        "write_tsv": write_tsv,
    }
    if missed_trace_correction:
        kwargs.update(
            {
                "max_time_dilation": float(10),
                "min_time_dilation": float(0.1),
                "time_dilation_tol": float(1e-3),
                "missed_trace_correction": bool(missed_trace_correction),
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
        sweep.run_vehicle_scenarios(config, REPORT_COLS=REPORT_COLS, **kwargs)
    )
    selections_list = []
    for sel, scenario_name, optpt in zip(
        vdf.index, vdf["scenario_name"], vdf["veh_pt_type"]
    ):
        if sweep.skip_scenario(
            sel, selections, scenario_name, report_kwargs=report_kwargs
        ):
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
                selections_list.append(sel)
        except:
            logging.exception("Fatal Error")
            raise

    print(f"Selections List final: {selections_list}")
    resdir = Path(report_kwargs["resdir"])
    RES_FILE = report_kwargs["RES_FILE"]

    if run_multi:
        print(f"Running multiprocessing version of T3CO")
        with Pool(processes=9) as pool:
            # call the same function with different data in parallel
            # for result in tqdm(pool.map(partial(read_file, root = root),files), total= len(files)):
            reports = []
            # reports_df =  pd.DataFrame()

            for report_i in pool.imap_unordered(
                partial(
                    sweep.run_optimize_analysis,
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
                if save_results:
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

            
            if save_results:
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
            report_i = sweep.run_optimize_analysis(
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

        if save_results:
            # reports_df = pd.DataFrame(reports)
            # reports_df.sort_values(by=["selection"], inplace=True)
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

    return reports_df

reports_df = run_t3co(analysis_id=0, config_filename=Path(__file__).parents[1]/"resources"/"T3COConfig.csv")
tc = T3COCharts(results_df=reports_df)  
tc.generate_tco_plots(x_group_col='vehicle_fuel_type', y_group_col='None', legend_pos=0.20, bar_width=0.6).show()

tc.generate_histogram(hist_col='discounted_tco_dol', n_bins=4).show()
tc.generate_violin_plot(x_group_col='vehicle_fuel_type', y_group_col='mpgge').show()

# %%
