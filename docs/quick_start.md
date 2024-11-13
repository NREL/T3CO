# Quick Start Guide to T3CO

A total-cost analysis is only as good as its inputs. Generating T3CO results requires equal parts of investment in inputs gathering as it is in running the tool. To make things easier, we provide 500+ demo scenarios for the user to choose from to run T3CO.

## Inputs

T3CO contains three main input files and several auxiliary files that are referenced in the main files for different purposes.

### Vehicle, Scenario, and Config

The main input files are the [***Vehicle***](vehicle_inputs_descriptions.md), [***Scenario***](scenario_inputs_descriptions.md), and [***Config***](config_inputs_descriptions.md). T3CO provides users with demo input files to get started. One or more *Vehicle-Scenario* pair selections are necessary to run T3CO:

- ***Vehicle*** contains sets of FASTSim vehicle input parameters that define the powertrain and vehicle dynamics of the selected *Vehicle-Scenario* pair. Each entry in the ***Vehicle*** file is called a "Vehicle Model" and is referenced using `vehicle.selection` as a key. [[Demo Vehicles](https://github.com/NREL/T3CO/blob/4aed80f4a2caf65abfc7be176fcf34107621e1fe/t3co/resources/inputs/demo/Demo_FY22_vehicle_model_assumptions.csv)]
- ***Scenario*** contains cost, infrastructure, and optimization related input parameters that define a certain scenario. Each entry in the Scenario file is called a "Scenario Model" and is referenced using `scenario.selection` as a key. [[Demo Scenarios](https://github.com/NREL/T3CO/blob/4aed80f4a2caf65abfc7be176fcf34107621e1fe/t3co/resources/inputs/demo/Demo_FY22_scenario_assumptions.csv)]
- ***Config*** contains easy ways to manage T3CO model settings and to save the inputs needed to run a set of selections of *Vehicle-Scenario* pairs. It also contains paths to various input files and some Scenario parameter overrides to be used globally on all selections. Users can also specify a path to the output directory in which T3CO results need to be saved. Each entry in the ***Config*** file refers to an "Analysis" and is accessed using `config.analysis_id` [[Demo Analyses](https://github.com/NREL/T3CO/blob/4aed80f4a2caf65abfc7be176fcf34107621e1fe/t3co/resources/T3COConfig.csv)]

Note that `scenario.selection` and `vehicle.selection` are expected by the tool to be the same for a chosen *Vehicle-Scenario* pair, i.e., a row on the ***Scenario*** file has a corresponding row on the ***Vehicle*** file with the same `selection` key. The `config.selections` attribute accepts a list of "selection" (that refers to both `scenario.selection` and `vehicle.selection`) and is used to fetch the desired set of inputs to run.

### Auxiliary Inputs

The auxiliary input files in the [`t3co/resources/auxiliary/`](https://github.com/NREL/T3CO/tree/4aed80f4a2caf65abfc7be176fcf34107621e1fe/t3co/resources/auxiliary) folder include `FuelPrices.csv`, `ResidualValues.csv`, `AeroDragImprovementCostCurve.csv`, `LightweightImprovementCostCurve.csv`, and `EngineEffImprovementCostCurve.csv`. These files contain important cost and model assumptions that are necessary to run different aspects of the T3CO cost models. Users can select the default auxiliary input files and choose the relevant set of assumptions. They can also add new entries to these files, or create their own auxiliary input files and mention the new paths in the ***Config*** file.

## Running T3CO
After checking the inputs and creating/modifying an "Analysis" on the ***Config*** file, the next step is to execute the models. The `t3co/sweep.py` module is the main script that needs to be run to perform a TCO analysis. And the most effective way to run the sweep module is to call a specific "Analysis" from the ***Config*** file using the `config.analysis_id` key.

### Running the Sweep Module from a PyPI-installed T3CO
The easiest way to run the `t3co.sweep` module is to use a local copy of the demo input files. If the [`install_t3co_demo_inputs`](./installation.md#copy-demo-inputs) command is used to copy `demo_inputs` to your local directory after [installing from PyPI](./installation.md#install-from-pypi), run the `t3co.sweep` module from any directory. 

```bash
python -m t3co.sweep --analysis-id=0 --config=<path/to/demo_inputs/T3COConfig.csv>
```
Point `--config` to the `T3COConfig.csv` file path and `--analysis-id` to the desired `config.analysis_id` (either an existing one or a newly added "Analysis" in the `demo_inputs/T3COConfig.csv` file. Default = `0`).

### Running Sweep Module from a Cloned Github repo
For running `config.analysis_id`=0 (or a user desired "Analysis") from the [Demo Config](https://github.com/NREL/T3CO/blob/4aed80f4a2caf65abfc7be176fcf34107621e1fe/t3co/resources/T3COConfig.csv) file on a cloned GitHub repo, run these commands from the parent directory:

```bash
python -m t3co.sweep --analysis-id=0
```

## Running T3CO in Batch Mode (using multiprocessing)
The user can run T3CO in a "Batch Mode", which may be useful when running a large number of *Vehicle-Scenario* pairs or a large number of drivecycles or both. T3CO provides a demo analysis (`config.analysis_id`=3 in the sample T3COConfig.csv file) that runs the Batch Mode for a folder of multiple input drivecycles. 

```bash
python -m t3co.sweep --analysis-id=3 --run-multi
```

The Batch Mode allows T3CO to run parallel analyses utilizing multiple processors (or CPU cores) denoted by CLI argument `--n-processors`(defaults to 9). Adjust this number accordingly. To get the fastest run time, close other processor intensive programs running on your computer and assign `--n-processors` as one or two less than the max number of cores.

When a folder path is provided in the T3COConfig.csv file (`config.drive_cycle`) containing "n" number of valid drivecycles, T3CO generates "n" scenarios for each *Vehicle* selections mentioned in `config.selections` with the `scenario.drive_cycle` populated with each of the "n" drivecycles. For Vehicle selection "1" in config.selections, the generated selection numbers are denoted by "1_000" for the first drivecycle, "1_001" for the second drivecycle, and so on.

## Other Command Line Interface arguments
Use the command below to get a list of all CLI arguments:
```bash
python -m t3co.sweep --help
```

```
$ python -m t3co.sweep --help
usage: SWEEP [-h] [--config CONFIG] [--analysis-id ANALYSIS_ID] [--vehicles VEHICLES] [--scenarios SCENARIOS] [--selections [SELECTIONS ...]] [--eng-curves ENG_CURVES] [--lw-curves LW_CURVES]
             [--aero-curves AERO_CURVES] [--look-for LOOK_FOR] [--skip-all-opt] [--skip-input-validation] [--exclude [EXCLUDE ...]] [--algorithms [ALGORITHMS ...]] [--dst-dir DST_DIR]
             [--dir-mark DIR_MARK] [--file-mark FILE_MARK] [--skip-save-veh] [--x-tol X_TOL] [--f-tol F_TOL] [--n-max-gen N_MAX_GEN] [--pop-size POP_SIZE] [--nth-gen NTH_GEN] [--n-last N_LAST]
             [--range-overshoot-tol RANGE_OVERSHOOT_TOL] [---missed-trace-correction] [--max-time-dilation MAX_TIME_DILATION] [--min-time-dilation MIN_TIME_DILATION]
             [--time-dilation-tol TIME_DILATION_TOL] [--write-tsv WRITE_TSV]

The sweep.py module is the main script to run T3CO

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Input Config file (default: ./resources/T3COConfig.csv)
  --analysis-id ANALYSIS_ID
                        Analysis key from input Config file - 'config.analysis_id' (default: 0)
  --vehicles VEHICLES   Input file for Vehicle models (default: ./resources/inputs/demo/Demo_FY22_vehicle_model_assumptions.csv)
  --scenarios SCENARIOS
                        Input file for Scenario models (default: ./resources/inputs/demo/Demo_FY22_scenario_assumptions.csv)
  --selections [SELECTIONS ...]
                        Selections desired to run. Selections can be an int, or list of ints, or range expression. Ex: --selections 234 or --selections "[234,236,238]" or --selections "range(234,
                        150, 2)" (default: None)
  --eng-curves ENG_CURVES
                        Input file for engine efficiency improvement cost curves (default: ./resources/auxiliary/EngineEffImprovementCostCurve.csv)
  --lw-curves LW_CURVES
                        Input file for lightweighting improvement cost curves (default: ./resources/auxiliary/LightweightImprovementCostCurve.csv)
  --aero-curves AERO_CURVES
                        Input file for aerodynamics improvement curves (default: ./resources/auxiliary/AeroDragImprovementCostCurve.csv)
  --look-for LOOK_FOR   A string for string matching, example --look_for 'FCEV' or -look_for '["FCEV", "HEV"]' (default: )
  --skip-all-opt, --skopt
                        If --skip_all_opt used, all runs skip optimization (default: False)
  --skip-input-validation, --skiv
                        If --skip_input_validation used, no pre-validation of inputs is run before sweep commences (default: True)
  --exclude [EXCLUDE ...]
                        Overrides -look_for. a string for string matching to exclude runs, example -exclude 'FCEV' or -look_for '["FCEV", "HEV"]' (default: >{-<>-}<)
  --algorithms [ALGORITHMS ...], --algos [ALGORITHMS ...], --algo [ALGORITHMS ...]
                        Enter algorithm or list of algorithms, or "ensemble" to use all, to use for optimization: ['NSGA2', 'NelderMead', 'PatternSearch', 'PSO'] ex: -algos PatternSearch | -algos
                        '["PatternSearch", "NSGA2"]' | -algos "ensemble" (default: NSGA2)
  --dst-dir DST_DIR     Directory to store T3CO results (default: ./results)
  --dir-mark DIR_MARK   Name for results directory in addition to timestamp (default: )
  --file-mark FILE_MARK
                        Prefix to add to the result file names (default: )
  --skip-save-veh       Toggle result vehicle model YAML file saving off (default: False)
  --x-tol X_TOL         Parameter space tolerance for optimization (default: 0.001)
  --f-tol F_TOL         Objective space tolerance for optimzation (default: 0.001)
  --n-max-gen N_MAX_GEN
                        Max number of optimizer iterations regardless of algorithm (default: 1000)
  --pop-size POP_SIZE   population of each generation (default: 25)
  --nth-gen NTH_GEN     Period of generations in which to evaluate if convergence happens during optimization (default: 1)
  --n-last N_LAST       Number of generations to look back for establishing convergence during optimization (default: 5)
  --range-overshoot-tol RANGE_OVERSHOOT_TOL
                        Range overshoot tolerance, example '0.20' allows 20% range overshoot. Default of 'None' does not constrain overshoot. (default: None)
  ---missed-trace-correction
                        Activate FASTSim time-dilation to correct missed trace (default: False)
  --max-time-dilation MAX_TIME_DILATION
                        Maximum time dilation factor to 'catch up' with trace (default: 10)
  --min-time-dilation MIN_TIME_DILATION
                        Minimum time dilation to let trace 'catch up' (default: 0.1)
  --time-dilation-tol TIME_DILATION_TOL
                        Convergence criteria for time dilation (default: 0.001)
  --write-tsv WRITE_TSV
                        Boolean toggle to save intermediary .TSV cost results files (default: False)
  --run-multi           Boolean switch to select multiprocessing version (default: False)
  --n-processors N_PROCESSORS
                        Number of processors to use for multiprocessing (default: 9)
```

## T3CO Results
After running the analysis, T3CO stores the results .CSV file in the directory specified by `config.dst_dir` (or the CLI argument `--dst-dir`). 

The results file includes a comprehensive list of [***Cost Outputs***](t3co_outputs_descriptions.md) that were calculated by the various ***T3CO Modules***. In addition to the T3CO outputs, all the *Vehicle* input parameters (denoted by a prefix: `input_vehicle_value_`),  *Scenario* input parameters(denoted by a prefix: `scenario_`), and *Config* parameters (denoted by a prefix: `config_`) are also present in the results file. When the optional optimization module is run, the optimized vehicle parameters are also listed ((denoted by a prefix: `optimized_vehicle_value_`)) instead of NaN values for non-optimization runs.