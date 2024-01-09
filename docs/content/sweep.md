# Table of Contents

* [sweep](#sweep)
  * [save\_tco\_files](#sweep.save_tco_files)
  * [get\_knobs\_bounds\_curves](#sweep.get_knobs_bounds_curves)
  * [get\_objectives\_constraints](#sweep.get_objectives_constraints)
  * [run\_moo](#sweep.run_moo)
  * [check\_input\_files](#sweep.check_input_files)
  * [run\_vehicle\_scenarios](#sweep.run_vehicle_scenarios)

<a id="sweep"></a>

# sweep

<a id="sweep.save_tco_files"></a>

#### save\_tco\_files

```python
def save_tco_files(tco_files, resdir, scenario_name, sel, ts)
```

This function saves the intermediary files as tsv

**Arguments**:

- `tco_files` _dict_ - Contains all TCO calculation dataframes
- `resdir` _str_ - result directory strong
- `scenario_name` _str_ - scenario name
- `sel` _str_ - selection(s)
- `ts` _str_ - timestring

<a id="sweep.get_knobs_bounds_curves"></a>

#### get\_knobs\_bounds\_curves

```python
def get_knobs_bounds_curves(selection, vpttype, sdf, lw_curves, aero_curves,
                            eng_eff_curves)
```

This function fetches the knobs and constraints for running the optimization for a given selection

**Arguments**:

- `selection` _float_ - selection number
- `vpttype` _str_ - vehicle powertrain type = veh_pt_type
- `sdf` _DataFrame_ - scenario dataframe
- `lw_curves` _DataFrame_ - light weighting curve dataframe
- `aero_curves` _DataFrame_ - aero drag curve dataframe
- `eng_eff_curves` _DataFrame_ - engine efficiency curve dataframe
  

**Returns**:

- `knobs_bounds` _dict_ - dict of knobs and bounds
- `curves` _dict_ - dict of lw, aero, and engine efficiency curve parameters

<a id="sweep.get_objectives_constraints"></a>

#### get\_objectives\_constraints

```python
def get_objectives_constraints(selection, sdf, verbose=True)
```

This function appends to list of necessary variables based on the constraints and objectives selected

**Arguments**:

- `selection` _float_ - selection number
- `sdf` _DataFrame_ - scenario dataframe
- `verbose` _bool, optional_ - if selected, function will print objectives and constraints. Defaults to True.
  

**Returns**:

- `objectives` _list_ - list of selected objective variables
- `constraints` _list_ - list of selected constraint variables

<a id="sweep.run_moo"></a>

#### run\_moo

```python
def run_moo(sel, sdf, optpt, algo, skip_opt, pop_size, n_max_gen, n_last,
            nth_gen, x_tol, verbose, f_tol, resdir, lw_curves, aero_curves,
            eng_curves, config, **kwargs)
```

This function calls get_objectives_constraints and get_knobs_bounds_curves, and then calls run_optimization to perform the multiobjective optimization

**Arguments**:

- `sel` _float_ - selection number
- `sdf` _DataFrame_ - scenario dataframe
- `optpt` _str_ - vehicle powertrain type
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
- `lw_curves` _DataFrame_ - light weighting curves dataframe
- `aero_curves` _DataFrame_ - aero drag curves dataframe
- `eng_curves` _DataFrame_ - engine efficiency curve dataframe
- `config` _Config_ - Config class object
  

**Returns**:

- `moo_results` _pymoo.core.result.Result_ - optimization results object
- `moo_problem` _T3COProblem_ - minimization problem that calculates TCO
- `moo_code` _Error_ - Error message

<a id="sweep.check_input_files"></a>

#### check\_input\_files

```python
def check_input_files(df, filetype, filepath)
```

This function contains assert statements that make sure input vehicle and scenario dataframes do not contain numm rows

**Arguments**:

- `df` _DataFrame_ - vehicle or scenario dataframe
- `filetype` _str_ - 'vehicle' or 'scenario'
- `filepath` _str_ - filepath of the vehicle or scenario input files

<a id="sweep.run_vehicle_scenarios"></a>

#### run\_vehicle\_scenarios

```python
def run_vehicle_scenarios(vehicles, scenarios, eng_curves_p, lw_curves_p,
                          aero_curves_p, config, **kwargs)
```

This is the main function that runs T3CO for all the selections input

**Arguments**:

- `vehicles` _str_ - path of vehicle input file
- `scenarios` _str_ - path of scenarios input file
- `eng_curves_p` _str_ - path of engine efficiency curve file
- `lw_curves_p` _str_ - path of light weighting curve file
- `aero_curves_p` _str_ - path of aero drag curve file
- `config` _Config_ - Config object containing analysis attributes and scenario attribute overrides
  

**Raises**:

- `Exception` - input validation error
- `Exception` - optimization error

