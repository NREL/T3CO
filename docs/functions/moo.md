# Table of Contents

* [moopack.moo](#moopack.moo)
  * [T3COProblem](#moopack.moo.T3COProblem)
    * [setup\_opt\_records](#moopack.moo.T3COProblem.setup_opt_records)
    * [\_\_init\_\_](#moopack.moo.T3COProblem.__init__)
    * [compile\_reporting\_vars](#moopack.moo.T3COProblem.compile_reporting_vars)
    * [instantiate\_moo\_vehicles\_and\_scenario](#moopack.moo.T3COProblem.instantiate_moo_vehicles_and_scenario)
    * [cda\_percent\_delta\_knob](#moopack.moo.T3COProblem.cda_percent_delta_knob)
    * [weight\_delta\_percent\_knob](#moopack.moo.T3COProblem.weight_delta_percent_knob)
    * [fc\_peak\_eff\_knob](#moopack.moo.T3COProblem.fc_peak_eff_knob)
    * [get\_objs](#moopack.moo.T3COProblem.get_objs)
    * [adjust\_fc\_peak\_eff](#moopack.moo.T3COProblem.adjust_fc_peak_eff)
    * [sweep\_knob](#moopack.moo.T3COProblem.sweep_knob)
    * [get\_tco\_from\_moo\_advanced\_result](#moopack.moo.T3COProblem.get_tco_from_moo_advanced_result)
  * [T3CODisplay](#moopack.moo.T3CODisplay)
    * [\_\_init\_\_](#moopack.moo.T3CODisplay.__init__)
  * [run\_optimization](#moopack.moo.run_optimization)

<a id="moopack.moo"></a>

# moopack.moo

<a id="moopack.moo.T3COProblem"></a>

## T3COProblem Objects

```python
class T3COProblem(ElementwiseProblem)
```

Class for creating PyMoo problem.

<a id="moopack.moo.T3COProblem.setup_opt_records"></a>

#### setup\_opt\_records

```python
def setup_opt_records()
```

This method sets up the empty optimization record arrays

<a id="moopack.moo.T3COProblem.__init__"></a>

#### \_\_init\_\_

```python
def __init__(knobs_bounds,
             vnum,
             optimize_pt=gl.BEV,
             obj_list=None,
             constr_list=None,
             verbose=False,
             config=None,
             **kwargs)
```

This constructor initializes optimization input variables

**Arguments**:

- `knobs_bounds` _dict_ - Dictionary containing knobs bounds for optimization
- `vnum` _float_ - Vehicle selection number
- `optimize_pt` _vehicle.veh_pt_type, optional_ - Vehicle powertrain type - Conv, BEV, HEV, PHEV. Defaults to gl.BEV.
- `obj_list` _list, optional_ - List of objectives. Defaults to None.
- `constr_list` _list, optional_ - List of constraints. Defaults to None.
- `verbose` _bool, optional_ - if True, prints process steps. Defaults to False.
- `config` _run_scenario.Config, optional_ - T3CO Config object containing analysis attributes and scenario attribute overrides. Defaults to None.

<a id="moopack.moo.T3COProblem.compile_reporting_vars"></a>

#### compile\_reporting\_vars

```python
def compile_reporting_vars()
```

This method creates an output dictionary containing optimization results

<a id="moopack.moo.T3COProblem.instantiate_moo_vehicles_and_scenario"></a>

#### instantiate\_moo\_vehicles\_and\_scenario

```python
def instantiate_moo_vehicles_and_scenario(vnum, config=None)
```

This method instantiates the multi-objective optimization problem vehicles and scenarios, starting with the baseline Conventional vehicle.

**Arguments**:

- `vnum` _float_ - vehicle selection number
- `config` _run_scenario.Config, optional_ - T3CO Config object containing analysis attributes and scenario attribute overrides. Defaults to None.
  

**Raises**:

- `TypeError` - Invalid optimize_pt selection

<a id="moopack.moo.T3COProblem.cda_percent_delta_knob"></a>

#### cda\_percent\_delta\_knob

```python
def cda_percent_delta_knob(CdA_perc_reduction, optvehicle)
```

This method sets the drag_coef based on aero improvement curve and glider_kg based on cda_cost_coeff_a and cda_cost_coeff_b

**Arguments**:

- `CdA_perc_reduction` _str_ - Name of aero improvement curve file
- `optvehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for optimization vehicle

<a id="moopack.moo.T3COProblem.weight_delta_percent_knob"></a>

#### weight\_delta\_percent\_knob

```python
def weight_delta_percent_knob(wt_perc_reduction, optvehicle)
```

This method sets the knob from the lightweighting curve

**Arguments**:

- `wt_perc_reduction` _float_ - Weight reduction percentage value from lightweighting curve
- `optvehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of the optimization vehicle

<a id="moopack.moo.T3COProblem.fc_peak_eff_knob"></a>

#### fc\_peak\_eff\_knob

```python
def fc_peak_eff_knob(fc_peak_eff, optvehicle)
```

This method sets the knob from the engine efficiency curve

**Arguments**:

- `fc_peak_eff` _float_ - Fuel converter peak effiency override from engine efficiency improvement curve
- `optvehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for optimization vehicle

<a id="moopack.moo.T3COProblem.get_objs"></a>

#### get\_objs

```python
def get_objs(x, write_tsv=False)
```

This method gets called when PyMoo calls _evaluate. It initializes objectives and constraints and runs vehicle_scenario_sweep

x optimization knobs = [max motor kw, battery kwh, drag coeff % improvement]
Function for running FE cycles and accel tests then returning
fuel consumption and zero-to-sixty times.

x is a set of genes (or parameters), so kwh size is a gene
chromosome is a full gene, all values in x

**Arguments**:

- `x` _dict_ - Dictionary containing optimization knobs - {max motor kw, battery kwh, drag coeff % improvement}
- `write_tsv` _bool, optional_ - if True, save intermediate dataframes. Defaults to False.
  

**Returns**:

- `obj_arr_F` _np.array_ - Array of objectives - tot_cost and phev_cd_fuel_used_kwh
- `constraint_results_G` _np.array_ - Array of constraints
- `rs_sweep` _dict_ - Output dictionary from vehicle_scenario_sweep

<a id="moopack.moo.T3COProblem.adjust_fc_peak_eff"></a>

#### adjust\_fc\_peak\_eff

```python
def adjust_fc_peak_eff(fc_peak_eff, scenario, optvehicle)
```

This method augments an advanced vehicle fc_eff_array based on new fc_peak_eff using baseline fc_eff_array


**Arguments**:

- `fc_peak_eff` _float_ - Fuel converter peak efficiency override
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `optvehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of optimization vehicle

<a id="moopack.moo.T3COProblem.sweep_knob"></a>

#### sweep\_knob

```python
def sweep_knob(knob, definition=100, plot=False, optres=None, **kwargs)
```

This method sweeps the optimization knob of vehicle from lbound to ubound, return TCO             plot optres to see if there's agreement from opt solution and your sweep

**Arguments**:

- `knob` _list_ - list of knobs names for optimization
- `definition` _int, optional_ - Number of points. Defaults to 100.
- `plot` _bool, optional_ - if True, saves plot of bounds and TCOs. Defaults to False.
- `optres` _float, optional_ - Optimization resolution. Defaults to None.
  

**Returns**:

- `tcos` _list_ - List of TCOs of length=definition

<a id="moopack.moo.T3COProblem.get_tco_from_moo_advanced_result"></a>

#### get\_tco\_from\_moo\_advanced\_result

```python
def get_tco_from_moo_advanced_result(x)
```

This method is a utility function to get detailed TCO information from optimized MOO result

**Arguments**:

- `x` _dict_ - Dictionary containing optimization knobs - [max motor kw, battery kwh, drag coeff % improvement]
  

**Returns**:

- `out` _dict_ - Dictionary containing TCO results for optimization runs

<a id="moopack.moo.T3CODisplay"></a>

## T3CODisplay Objects

```python
class T3CODisplay(Output)
```

This class contains the display object for Pymoo optimization printouts - pymoo.util.display.Display

**Arguments**:

- `Output` _pymoo.util.display.output.Output_ - Pymoo minimize display object

<a id="moopack.moo.T3CODisplay.__init__"></a>

#### \_\_init\_\_

```python
def __init__(**kwargs)
```

This constructor initializes the pymoo.util.display.Display object

<a id="moopack.moo.run_optimization"></a>

#### run\_optimization

```python
def run_optimization(pop_size,
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
                     **kwargs)
```

This method creates and runs T3COProblem minimization

**Arguments**:

- `pop_size` _int_ - Population size for optimization
- `n_max_gen` _int_ - maximum number of generations for optimization
- `knobs_bounds` _dict_ - Dictionary containing knobs and bounds
- `vnum` _float_ - vehicle selection number
- `x_tol` _float_ - tolerance in parameter space
- `f_tol` _float_ - tolerance in objective space
- `nth_gen` _int_ - number of generations to evaluate if convergence occurs
- `n_last` _int_ - number of generations to look back for termination
- `algo` _str_ - algorithm name
- `obj_list` _list, optional_ - list of objectives - TCO or PHEV_MINIMIZE_FUEL_USE_OBJECTIVE. Defaults to None.
- `config` _run_scenario.Config, optional_ - T3CO Config object containing analysis attributes and scenario attribute overrides. Defaults to None.
  

**Returns**:

- `res` _pymoo.core.result.Result_ - Pymoo optimization result object
- `problem` _moo.T3COProblem_ - T3COProblem ElementwiseProblem object
- `OPTIMIZATION_SUCCEEDED` _bool_ - if True, pymoo.minimize succeeded

