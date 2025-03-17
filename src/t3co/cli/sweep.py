from __future__ import annotations

import argparse
import ast
import time
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from typing import Dict, List, Tuple, Union

import pandas as pd

from t3co.constants import Global as gl
from t3co.energy_models.energy import Energy
from t3co.input_data.config import Config
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle
from t3co.tco.ledger import Ledger
from t3co.utils.print_class_objects import get_path_object


def load_vehicle_scenario_energy(
    selection: Union[int, str],
    config: Config,
    vehicle: Vehicle = None,
    scenario: Scenario = None,
    energy: Energy = None,
) -> Tuple[Vehicle, Scenario, Energy]:
    """
    Loads the vehicle, scenario, and energy models based on the selection and config.

    Args:
        selection (Union[int, str]): The selection index or string.
        config (Config): The configuration instance.

    Returns:
        Tuple[Vehicle, Scenario, Energy]: The vehicle, scenario, and energy models.
    """
    if config.dc_files:
        selection, dc_id = map(int, selection.split("_"))

    if scenario:
        input_scenario = scenario
    else:
        input_scenario = Scenario().from_file(
            selection=selection, scenario_file=config.scenario_file
        )
        input_scenario.override_from_config(config=config)

    if vehicle:
        input_vehicle = vehicle
    else:
        input_vehicle = Vehicle().from_config(selection=selection, config=config)
        input_vehicle.set_veh_kg()

    if config.dc_files:
        input_scenario.drive_cycle = config.dc_files[int(dc_id)]
        if config.energy_file:
            input_scenario.mpgge = config.energy_df.loc[int(dc_id), "mpgge"]
            input_scenario.primary_fuel_range_mi = config.energy_df.loc[
                int(dc_id),
                "primary_fuel_range_mi",
            ]

    if energy:
        input_energy = energy
    elif (
        input_scenario.mpgge
        and input_scenario.primary_fuel_range_mi
        and not input_scenario.cost_toggles.run_fastsim
    ):
        input_energy = Energy(
            mpgge=float(input_scenario.mpgge),
            primary_fuel_range_mi=float(input_scenario.primary_fuel_range_mi),
        )
    else:
        input_energy = Energy()
        input_energy.run_fastsim_model(
            veh_no=selection, vehicle_file=config.vehicle_file, scenario=input_scenario
        )

    return input_vehicle, input_scenario, input_energy


def generate_ledger(selection: int, config: Config) -> Dict:
    """
    Generates the ledger for the given selection and config.

    Args:
        selection (int): The selection index.
        config (Config): The configuration instance.

    Returns:
        Dict: The ledger as a dictionary.
    """
    input_vehicle, input_scenario, input_energy = load_vehicle_scenario_energy(
        selection=selection, config=config
    )
    print(f"Running Selection: {selection}")

    return Ledger(
        vehicle=input_vehicle,
        scenario=input_scenario,
        energy=input_energy,
        config=config,
    ).to_dict()


def create_results_filepath(config: Config) -> Path:
    """
    Creates the results file path based on the config.

    Args:
        config (Config): The configuration instance.

    Returns:
        Path: The path to the results file.
    """
    ts = time.strftime("%Y-%m-%d_%H-%M-%S")
    if config.resfile_suffix:
        result_filename = f"results_{ts}_{str(config.resfile_suffix)}.csv".strip("_")
    else:
        selections_string = (
            str(config.selections)
            .strip("[]")
            .replace(" ", "")
            .replace("'", "")
            .replace(",", "-")
        )
        result_filename = f"results_{ts}_sel_{selections_string[:20]}.csv".strip("_")
    output_path = get_path_object(config.dst_dir) / result_filename

    if not output_path.exists():
        output_path.parent.mkdir(parents=True, exist_ok=True)

    return output_path


def export_results_to_csv(
    reports_list: List[Dict],
    config: Config,
    output_path: Union[str, Path] = None,
    return_filepath: bool = True,
    return_df: bool = False,
    sort_values: bool = False,
) -> Tuple[Union[Path, None], Union[pd.DataFrame, None]]:
    """
    Exports the results to a CSV file.

    Args:
        reports_list (List[Dict]): The list of reports.
        config (Config): The configuration instance.
        output_path (Union[str, Path], optional): The output path for the CSV file. Defaults to None.
        return_filepath (bool, optional): Whether to return the file path. Defaults to True.
        return_df (bool, optional): Whether to return the DataFrame. Defaults to False.
        sort_values (bool, optional): Whether to sort the values by selection. Defaults to False.

    Returns:
        Tuple[Union[Path, None], Union[pd.DataFrame, None]]: The output path and DataFrame if specified.
    """
    reports_df = pd.DataFrame(reports_list)

    if not output_path:
        output_path = create_results_filepath(config=config)

    if sort_values:
        reports_df.sort_values(by="selection", inplace=True)

    reports_df.to_csv(output_path)

    return (output_path if return_filepath else None), (
        reports_df if return_df else None
    )


def run_t3co(config: Config, save_results: bool = True) -> None:
    """
    Runs the T3CO analysis.

    Args:
        config (Config): The configuration instance.
        save_results (bool, optional): Whether to save the results. Defaults to True.
    """
    reports_list = []
    error_list = []
    for selection in config.selections_list:
        try:
            reports_list.append(generate_ledger(selection=selection, config=config))
        except ValueError:
            error_list.append(selection)
            continue

    if save_results:
        output_path, reports_df = export_results_to_csv(
            reports_list=reports_list,
            config=config,
            return_filepath=True,
            return_df=True,
        )
        print(reports_df)
        if len(error_list):
            print(f"Selections {error_list} were skipped due to assumptions errors.")
        print(f"T3CO results saved to: {output_path}")


if __name__ == "__main__":
    start = time.time()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="SWEEP",
        description="""The sweep.py module is the main script to run T3CO""",
    )
    parser.add_argument(
        "--config",
        default=gl.RESOURCES_FOLDERPATH / "T3COConfig.csv",
        type=str,
        help="Input Config file",
    )
    parser.add_argument(
        "--analysis-id",
        default=0,
        type=int,
        help="Analysis key from input Config file - 'config.analysis_id'",
    )
    parser.add_argument(
        "--vehicles",
        default=gl.RESOURCES_FOLDERPATH
        / "inputs"
        / "Demo_FY22_vehicle_model_assumptions.csv",
        type=str,
        help="Input file for Vehicle models",
    )
    parser.add_argument(
        "--scenarios",
        default=gl.RESOURCES_FOLDERPATH
        / "inputs"
        / "Demo_FY22_scenario_assumptions.csv",
        type=str,
        help="Input file for Scenario models",
    )
    parser.add_argument(
        "--selections",
        type=ast.literal_eval,
        nargs="*",
        help="""Selections desired to run. Selections can be an int, or list of ints, or range expression. Ex: --selections 234 or --selections "[234,236,238]" or --selections "range(234, 150, 2)" """,
    )
    parser.add_argument(
        "--drive-cycle",
        type=ast.literal_eval,
        nargs="*",
        help="""Override drive_cycle from scenario with a composite cycle, or an individual cycle, or a folder of cycles. File paths should be relative to the resources folder """,
    )
    parser.add_argument(
        "--eng-curves",
        default=gl.RESOURCES_FOLDERPATH
        / "auxiliary"
        / "EngineEffImprovementCostCurve.csv",
        type=str,
        help="Input file for engine efficiency improvement cost curves",
    )
    parser.add_argument(
        "--lw-curves",
        default=gl.RESOURCES_FOLDERPATH
        / "auxiliary"
        / "LightweightImprovementCostCurve.csv",
        type=str,
        help="Input file for lightweighting improvement cost curves",
    )
    parser.add_argument(
        "--aero-curves",
        default=gl.RESOURCES_FOLDERPATH
        / "auxiliary"
        / "AeroDragImprovementCostCurve.csv",
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
        help='Enter algorithm or list of algorithms, or "ensemble" to use all, to use for optimization: ex: -algos PatternSearch | -algos \'["PatternSearch", "NSGA2"]\' | -algos "ensemble" ',
    )
    parser.add_argument(
        "--dst-dir",
        default=gl.SWEEP_PATH.parents[2] / "results",
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
    )
    parser.add_argument(
        "--f-tol",
        default=0.001,
        type=float,
        help="Objective space tolerance for optimization",
    )
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

    if args.config is None or args.config == "None":
        config = Config()
        config.selections = (
            args.selections[0]
            if isinstance(args.selections[0], list)
            else [args.selections]
        )
        config.drive_cycle = args.drive_cycle
        config.check_drivecycles_and_create_selections()
        config.read_auxiliary_files()
        config.vehicle_file = Path(args.vehicles)
        config.scenario_file = Path(args.scenarios)
        config.eng_eff_imp_curves = Path(args.eng_curves)
        config.lw_imp_curves = Path(args.lw_curves)
        config.aero_drag_imp_curves = Path(args.aero_curves)
    else:
        config = Config()
        config.from_file(filename=args.config, analysis_id=args.analysis_id)
        config.check_drivecycles_and_create_selections()
        config.read_auxiliary_files()
        gl.RESOURCES_FOLDERPATH = Path(args.config).parent
        config.vehicle_file = get_path_object(config.vehicle_file)
        config.scenario_file = get_path_object(config.scenario_file)
        config.eng_eff_imp_curves = get_path_object(config.eng_eff_imp_curves)
        config.lw_imp_curves = get_path_object(config.lw_imp_curves)
        config.aero_drag_imp_curves = get_path_object(config.aero_drag_imp_curves)

    print(f"Selection List: {config.selections_list}")

    if args.run_multi:
        print("Running multiprocessing version of T3CO")
        result_filepath = create_results_filepath(config=config)
        reports_list = []
        with Pool(processes=args.n_processors) as pool:
            for report_i in pool.imap_unordered(
                partial(generate_ledger, config=config),
                config.selections_list,
            ):
                reports_list.append(report_i)
                k = len(reports_list)
                if (k % 20 == 0 or k == 4) and (
                    len(config.selections_list) != 1 and k != 0
                ):
                    export_results_to_csv(
                        reports_list=reports_list,
                        config=config,
                        output_path=result_filepath,
                    )
                    print(f"\nSaving intermediate results to {str(result_filepath)}\n")
                print(f"Number of files done: {k}/{len(config.selections_list)}")

            pool.close()
            pool.join()

            export_results_to_csv(
                reports_list=reports_list,
                config=config,
                output_path=result_filepath,
                sort_values=True,
            )
            print(f"T3CO results saved to: {result_filepath}")

    else:
        run_t3co(config=config, save_results=True)

    print(f"T3CO Run time: {time.time() - start}")
