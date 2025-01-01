import argparse
import ast
import os
from pathlib import Path
import time
from typing import Tuple
import pandas as pd
from typing_extensions import List
from t3co.constants import Global as gl
from t3co.input_data.config import Config
from t3co.input_data.vehicle import Vehicle
from t3co.input_data.scenario import Scenario
from t3co.energy_models.energy import Energy
from t3co.tco.ledger import Ledger

def load_vehicle_scenario_energy(selection:int, config: Config)-> Tuple[Vehicle, Scenario, Energy]:
    
    input_scenario = Scenario().from_file(selection=selection, scenario_file=config.scenario_file)
    input_scenario.from_config(config=config,)
    input_vehicle = Vehicle().from_config(selection=selection, config=config)
    input_vehicle.set_veh_kg()
    input_energy = Energy()
    input_energy.run_fastsim_model(veh_no=selection, vehicle_file=config.vehicle_file, scenario=input_scenario)

    return input_vehicle, input_scenario, input_energy

def run_t3co(config: Config, save_results: bool = True):
    reports = []
    for selection in config.selections:
        input_vehicle, input_scenario, input_energy  = load_vehicle_scenario_energy(selection=selection, config=config)
        reports.append(Ledger(vehicle=input_vehicle, scenario=input_scenario, energy=input_energy, config=config).to_dict())
    reports_df = pd.DataFrame(reports)
    print(reports_df)
    if save_results:
        ts = time.strftime("%Y-%m-%d_%H-%M-%S")
        if config.resfile_suffix:
            RES_FILE = f"results_{ts}_{str(config.resfile_suffix)}.csv".strip(
                "_"
            )
        else:
            selections_string = (
                str(config.selections)
                .strip("[]")
                .replace(" ", "")
                .replace("'", "")
                .replace(",", "-")
            )
            RES_FILE = f"results_{ts}_sel_{selections_string[:20]}.csv".strip(
                "_"
            )
        output_path = (
                Path(config.dst_dir)/RES_FILE
                if Path(config.dst_dir).is_absolute()
                else Path(__file__).parents[1]
                / "resources"
                / config.dst_dir / RES_FILE
            )
        if not output_path.exists():
            output_path.parent.mkdir(parents=True, exist_ok=True)
        reports_df.to_csv(output_path)
        print(f'T3CO results saved to: {output_path}')
    
if __name__ == "__main__":
    start = time.time()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="SWEEP",
        description="""The sweep.py module is the main script to run T3CO""",
    )
    parser.add_argument(
        "--config",
        default=gl.SWEEP_PATH.parents[1] / "resources/T3COConfig.csv",
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
        default=gl.SWEEP_PATH.parents[1]
        / "resources/inputs/Demo_FY22_vehicle_model_assumptions.csv",
        type=str,
        help="Input file for Vehicle models",
    )
    parser.add_argument(
        "--scenarios",
        default=gl.SWEEP_PATH.parents[1]
        / "resources/inputs/Demo_FY22_scenario_assumptions.csv",
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
        "--eng-curves",
        default=gl.SWEEP_PATH.parents[1]
        / "resources/auxiliary/EngineEffImprovementCostCurve.csv",
        type=str,
        help="Input file for engine efficiency improvement cost curves",
    )
    parser.add_argument(
        "--lw-curves",
        default=gl.SWEEP_PATH.parents[1]
        / "resources/auxiliary/LightweightImprovementCostCurve.csv",
        type=str,
        help="Input file for lightweighting improvement cost curves",
    )
    parser.add_argument(
        "--aero-curves",
        default=gl.SWEEP_PATH.parents[1]
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
        help="Objective space tolerance for optimzation",
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

    # selections can be an int, or list of ints, or range expression
    if args.config is None or args.config=="None":
        config = Config()
        config.selections = (args.selections[0] if isinstance(args.selections[0], list) else [args.selections])
        config.vehicle_file = Path(args.vehicles)
        config.scenario_file = Path(args.scenarios)
        config.eng_eff_imp_curves = Path(args.eng_curves)
        config.lw_imp_curves = Path(args.lw_curves)
        config.aero_drag_imp_curves = Path(args.aero_curves)
    else:
        config = Config()
        try:
            config.from_file(filename=Path(args.config), analysis_id=args.analysis_id)
        except ValueError:
            print(f"Config analysis_id not valid: {args.analysis_id}")
            config.validate_analysis_id(filename=Path(args.config))
        config.check_drivecycles_and_create_selections(args.config)
        config.vehicle_file = Path(args.config).parent / config.vehicle_file
        config.scenario_file = Path(args.config).parent / config.scenario_file
        config.eng_eff_imp_curves = Path(args.config).parent / config.eng_eff_imp_curves
        config.lw_imp_curves = Path(args.config).parent / config.lw_imp_curves
        config.aero_drag_imp_curves =  Path(args.config).parent / config.aero_drag_imp_curves
        
    run_t3co(config=config)
    print(f'T3CO Run time: {time.time()-start}')

        
