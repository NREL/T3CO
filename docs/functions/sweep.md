# Table of Contents

* [t3co/sweep](#t3co/sweep)
  * [deug\_traces](#t3co/sweep.deug_traces)
  * [save\_tco\_files](#t3co/sweep.save_tco_files)
  * [get\_knobs\_bounds\_curves](#t3co/sweep.get_knobs_bounds_curves)
  * [get\_objectives\_constraints](#t3co/sweep.get_objectives_constraints)
  * [run\_moo](#t3co/sweep.run_moo)
  * [check\_input\_files](#t3co/sweep.check_input_files)
  * [skip\_scenario](#t3co/sweep.skip_scenario)
  * [optimize](#t3co/sweep.optimize)
  * [run\_vehicle\_scenarios](#t3co/sweep.run_vehicle_scenarios)
  * [run\_optimize\_analysis](#t3co/sweep.run_optimize_analysis)

<a id="t3co/sweep"></a>

# t3co/sweep

<a id="t3co/sweep.deug_traces"></a>

#### deug\_traces

```python
def deug_traces(vehicle: fastsim.vehicle.Vehicle,
                cycles: List[fastsim.cycle.Cycle],
                scenario: run_scenario.Scenario) -> None
```

This function gets a diagnostic trace of get_mpgge

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim Vehicle object
- `cycles` _List[fastsim.cycle.Cycle]_ - List of FASTSim drivecycle objects
- `scenario` _run_scenario.Scenario_ - Scenario object

<a id="t3co/sweep.save_tco_files"></a>

#### save\_tco\_files

```python
def save_tco_files(tco_files: dict, resdir: str, scenario_name: str, sel: str,
                   ts: str) -> None
```

This function saves the intermediary files as tsv

**Arguments**:

- `tco_files` _dict_ - Contains all TCO calculation dataframes
- `resdir` _str_ - result directory strong
- `scenario_name` _str_ - scenario name
- `sel` _str_ - selection(s)
- `ts` _str_ - timestring

<a id="t3co/sweep.get_knobs_bounds_curves"></a>

#### get\_knobs\_bounds\_curves

```python
def get_knobs_bounds_curves(selection: int, vpttype: str, sdf: pd.DataFrame,
                            lw_imp_curves: pd.DataFrame,
                            aero_drag_imp_curves: pd.DataFrame,
                            eng_eff_curves: pd.DataFrame) -> Tuple[dict, dict]
```

This function fetches the knobs and constraints for running the optimization for a given selection

**Arguments**:

- `selection` _int_ - selection number
- `vpttype` _str_ - vehicle powertrain type = veh_pt_type
- `sdf` _pd.DataFrame_ - scenario dataframe
- `lw_imp_curves` _pd.DataFrame_ - light weighting curve dataframe
- `aero_drag_imp_curves` _pd.DataFrame_ - aero drag curve dataframe
- `eng_eff_curves` _pd.DataFrame_ - engine efficiency curve dataframe
  

**Returns**:

- `knobs_bounds` _dict_ - dict of knobs and bounds
- `curves` _dict_ - dict of lw, aero, and engine efficiency curve parameters

<a id="t3co/sweep.get_objectives_constraints"></a>

#### get\_objectives\_constraints

```python
def get_objectives_constraints(selection: int,
                               sdf: pd.DataFrame,
                               verbose: bool = True) -> Tuple[list, list]
```

This function appends to list of necessary variables based on the constraints and objectives selected

**Arguments**:

- `selection` _int_ - selection number
- `sdf` _DataFrame_ - scenario dataframe
- `verbose` _bool, optional_ - if selected, function will print objectives and constraints. Defaults to True.
  

**Returns**:

- `objectives` _list_ - list of selected objective variables
- `constraints` _list_ - list of selected constraint variables

<a id="t3co/sweep.run_moo"></a>

#### run\_moo

```python
def run_moo(
        sel: int, sdf: pd.DataFrame, optpt: str, algo: str, skip_opt: bool,
        pop_size: float, n_max_gen: int, n_last: int, nth_gen: int,
        x_tol: float, verbose: bool, f_tol: float, resdir: str,
        lw_imp_curves_df: pd.DataFrame, aero_drag_imp_curves_df: pd.DataFrame,
        eng_eff_imp_curves_df: pd.DataFrame, config: run_scenario.Scenario,
        **kwargs) -> Tuple[pymoo.core.result.Result, moo.T3COProblem, bool]
```

This function calls get_objectives_constraints and get_knobs_bounds_curves, and then calls run_optimization to perform the multiobjective optimization

**Arguments**:

- `sel` _int_ - selection number
- `sdf` _DataFrame_ - Scenario dataframe
- `optpt` _str_ - FASTSim vehicle powertrain type
- `algo` _str_ - algorithm name
- `skip_opt` _bool_ - skip optimization boolean
- `pop_size` _int_ - population size for optimization
- `n_max_gen` _int_ - maximum number of generations for optimization
- `n_last` _int_ - number of generations to look back for termination
- `nth_gen` _int_ - number of generations to evaluate if convergence occurs
- `x_tol` _float_ - tolerance in parameter space
- `verbose` _book_ - if selected, function prints the optimization process
- `f_tol` _float_ - tolerance in objective space
- `resdir` _str_ - results directory
- `lw_imp_curves_df` _DataFrame_ - light weighting curves dataframe
- `aero_drag_imp_curves_df` _DataFrame_ - aero drag curves dataframe
- `eng_eff_imp_curves_df` _DataFrame_ - engine efficiency curve dataframe
- `config` _Config_ - Config class object
  

**Returns**:

- `moo_results` _pymoo.core.result.Result_ - optimization results object
- `moo_problem` _T3COProblem_ - minimization problem that calculates TCO
- `moo_code` _bool_ - Error message

<a id="t3co/sweep.check_input_files"></a>

#### check\_input\_files

```python
def check_input_files(df: pd.DataFrame, filetype: str, filepath: str) -> None
```

This function contains assert statements that make sure input vehicle and scenario dataframes do not contain numm rows

**Arguments**:

- `df` _DataFrame_ - vehicle or scenario dataframe
- `filetype` _str_ - 'vehicle' or 'scenario'
- `filepath` _str_ - filepath of the vehicle or scenario input files

<a id="t3co/sweep.skip_scenario"></a>

#### skip\_scenario

```python
def skip_scenario(sel,
                  selections,
                  scenario_name,
                  report_kwargs,
                  verbose=False) -> bool
```

This function checks if given selection is present in exclude or look_for selections

**Arguments**:

- `sel` _float_ - _description_
- `scenario_name` _str_ - scenario name
- `verbose` _bool, optional_ - if selected, prints out scenarios that are skipped. Defaults to False.
  

**Returns**:

- `bool` - if not present, returns True; Else False

<a id="t3co/sweep.optimize"></a>

#### optimize

```python
def optimize(sel: float,
             sdf: pd.DataFrame,
             vdf: pd.DataFrame,
             algo: str,
             report_kwargs: dict,
             REPORT_COLS: dict,
             skip_opt: bool,
             config: run_scenario.Config,
             write_tsv: bool = False) -> dict
```

This function runs the optimization for a given selection if skip_opt = False


**Arguments**:

- `sel` _float_ - Selection number
- `sdf` _pd.DataFrame_ - Dataframe of input scenario file
- `vdf` _pd.DataFrame_ - Dataframe of input vehicle file
- `algo` _str_ - Multiobjective optimization Algorithm name
- `report_kwargs` _dict_ - arguments related to running T3CO
- `REPORT_COLS` _dict_ - Results columns dictionary for sorting the T3CO results
- `skip_opt` _bool_ - skip optimization. If true, then optimizer is not run.
- `config` _run_scenario.Config_ - Config object
- `write_tsv` _bool, optional_ - if selected, intermediary dataframes are saved as tsv files.. Defaults to False.
  

**Returns**:

- `report_i` _dict_ - Dictionary of T3CO results for given selection

<a id="t3co/sweep.run_vehicle_scenarios"></a>

#### run\_vehicle\_scenarios

```python
def run_vehicle_scenarios(
    config: run_scenario.Config, REPORT_COLS: dict, **kwargs
) -> Tuple[List[int | str], pd.DataFrame, pd.DataFrame, bool, dict, dict]
```

This function reads the input files, validates inputs, compiles the selections, and returns a clean set of inputs that are needed for the current analysis.


**Arguments**:

- `config` _Config_ - Config object containing analysis attributes and scenario attribute overrides
- `REPORT_COLS` _dict_ - Dictionary of reporting columns from T3CO
  

**Raises**:

- `Exception` - input validation error
- `Exception` - optimization error
  

**Returns**:

  selections, vdf, sdf, skip_all_opt, report_kwargs, REPORT_COLS (Tuple[List[int|str], pd.DataFrame, pd.DataFrame, bool, dict, dict]): Selections list, vehicle dataframe, scenario dataframe, skip all optimization, report arguments, and report columns

<a id="t3co/sweep.run_optimize_analysis"></a>

#### run\_optimize\_analysis

```python
def run_optimize_analysis(sel: str | int, vdf: pd.DataFrame, sdf: pd.DataFrame,
                          skip_all_opt: bool, config: run_scenario.Config,
                          report_kwargs: dict, REPORT_COLS: dict) -> dict
```

This function runs the optimization function based on skip_all_opt input to return the report_i dictionary with T3CO results for each selection.

**Arguments**:

- `sel` _str | int_ - selection number
- `vdf` _pd.DataFrame_ - Dataframe of input vehicle file
- `sdf` _pd.DataFrame_ - Dataframe of input scenario file
- `skip_all_opt` _bool_ - Skip all optimization. If true, then the optimizer is not run for any scenario
- `config` _run_scenario.Config_ - Config object
- `report_kwargs` _dict_ - Dictionary of args required for running T3CO
- `REPORT_COLS` _dict_ - Dictionary of reporting columns from T3CO
  

**Returns**:

- `report_i` _dict_ - Dictionary of T3CO results for given selection

