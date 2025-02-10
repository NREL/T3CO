# Table of Contents

* [t3co](#t3co)
* [t3co.tco.ledger](#t3co.tco.ledger)
  * [Ledger](#t3co.tco.ledger.Ledger)
    * [\_\_new\_\_](#t3co.tco.ledger.Ledger.__new__)
    * [\_\_init\_\_](#t3co.tco.ledger.Ledger.__init__)
    * [set\_discounted\_costs](#t3co.tco.ledger.Ledger.set_discounted_costs)
    * [set\_discounted\_tco](#t3co.tco.ledger.Ledger.set_discounted_tco)
    * [set\_cost\_components](#t3co.tco.ledger.Ledger.set_cost_components)
    * [to\_dict](#t3co.tco.ledger.Ledger.to_dict)
    * [to\_json](#t3co.tco.ledger.Ledger.to_json)
    * [to\_df](#t3co.tco.ledger.Ledger.to_df)
    * [to\_csv](#t3co.tco.ledger.Ledger.to_csv)
    * [\_\_str\_\_](#t3co.tco.ledger.Ledger.__str__)
* [t3co.tco](#t3co.tco)
* [t3co.tco.tcocalc](#t3co.tco.tcocalc)
  * [TCOCalc](#t3co.tco.tcocalc.TCOCalc)
    * [\_\_new\_\_](#t3co.tco.tcocalc.TCOCalc.__new__)
    * [\_\_init\_\_](#t3co.tco.tcocalc.TCOCalc.__init__)
    * [calculate\_capital\_costs](#t3co.tco.tcocalc.TCOCalc.calculate_capital_costs)
    * [calculate\_opportunity\_costs](#t3co.tco.tcocalc.TCOCalc.calculate_opportunity_costs)
    * [calculate\_operating\_costs](#t3co.tco.tcocalc.TCOCalc.calculate_operating_costs)
    * [set\_total\_cost](#t3co.tco.tcocalc.TCOCalc.set_total_cost)
    * [set\_disc\_total\_cost](#t3co.tco.tcocalc.TCOCalc.set_disc_total_cost)
    * [\_\_str\_\_](#t3co.tco.tcocalc.TCOCalc.__str__)
* [t3co.optimize](#t3co.optimize)
* [t3co.constants.Global](#t3co.constants.Global)
  * [DieselGalPerGasGal](#t3co.constants.Global.DieselGalPerGasGal)
  * [kgH2\_per\_gge](#t3co.constants.Global.kgH2_per_gge)
  * [mps\_to\_mph](#t3co.constants.Global.mps_to_mph)
  * [m\_to\_mi](#t3co.constants.Global.m_to_mi)
  * [set\_tco\_intermediates](#t3co.constants.Global.set_tco_intermediates)
  * [set\_tco\_results](#t3co.constants.Global.set_tco_results)
  * [kg\_to\_lbs](#t3co.constants.Global.kg_to_lbs)
  * [lbs\_to\_kgs](#t3co.constants.Global.lbs_to_kgs)
  * [not\_falsy](#t3co.constants.Global.not_falsy)
* [t3co.constants](#t3co.constants)
* [t3co.resources](#t3co.resources)
* [t3co.energy\_models](#t3co.energy_models)
* [t3co.energy\_models.energy](#t3co.energy_models.energy)
  * [Energy](#t3co.energy_models.energy.Energy)
    * [\_\_new\_\_](#t3co.energy_models.energy.Energy.__new__)
    * [\_\_init\_\_](#t3co.energy_models.energy.Energy.__init__)
    * [run\_fastsim\_model](#t3co.energy_models.energy.Energy.run_fastsim_model)
* [t3co.energy\_models.fastsim\_model.fastsim\_wrapper](#t3co.energy_models.fastsim_model.fastsim_wrapper)
  * [RunFastsim](#t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim)
    * [\_\_new\_\_](#t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim.__new__)
    * [load\_vehicle](#t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim.load_vehicle)
    * [load\_design\_cycle\_from\_scenario](#t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim.load_design_cycle_from_scenario)
    * [load\_design\_cycle\_from\_path](#t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim.load_design_cycle_from_path)
    * [get\_simdrive](#t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim.get_simdrive)
    * [get\_range](#t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim.get_range)
* [t3co.energy\_models.fastsim\_model](#t3co.energy_models.fastsim_model)
* [t3co.utils](#t3co.utils)
* [t3co.utils.print\_class\_objects](#t3co.utils.print_class_objects)
  * [obj\_to\_string](#t3co.utils.print_class_objects.obj_to_string)
  * [handle\_nan](#t3co.utils.print_class_objects.handle_nan)
  * [custom\_default](#t3co.utils.print_class_objects.custom_default)
  * [to\_flat\_dict](#t3co.utils.print_class_objects.to_flat_dict)
  * [remove\_df\_attrs](#t3co.utils.print_class_objects.remove_df_attrs)
* [t3co.utils.demo\_files\_installer](#t3co.utils.demo_files_installer)
  * [main](#t3co.utils.demo_files_installer.main)
  * [copy\_demo\_input\_files](#t3co.utils.demo_files_installer.copy_demo_input_files)
* [t3co.input\_data.config](#t3co.input_data.config)
  * [Config](#t3co.input_data.config.Config)
    * [\_\_new\_\_](#t3co.input_data.config.Config.__new__)
    * [from\_file](#t3co.input_data.config.Config.from_file)
    * [from\_dict](#t3co.input_data.config.Config.from_dict)
    * [validate\_analysis\_id](#t3co.input_data.config.Config.validate_analysis_id)
    * [check\_drivecycles\_and\_create\_selections](#t3co.input_data.config.Config.check_drivecycles_and_create_selections)
    * [read\_auxiliary\_files](#t3co.input_data.config.Config.read_auxiliary_files)
    * [delete\_dataframes](#t3co.input_data.config.Config.delete_dataframes)
* [t3co.input\_data.vehicle](#t3co.input_data.vehicle)
  * [Vehicle](#t3co.input_data.vehicle.Vehicle)
    * [\_\_new\_\_](#t3co.input_data.vehicle.Vehicle.__new__)
    * [from\_config](#t3co.input_data.vehicle.Vehicle.from_config)
    * [from\_db](#t3co.input_data.vehicle.Vehicle.from_db)
    * [set\_veh\_kg](#t3co.input_data.vehicle.Vehicle.set_veh_kg)
    * [delete\_dataframes](#t3co.input_data.vehicle.Vehicle.delete_dataframes)
* [t3co.input\_data](#t3co.input_data)
* [t3co.input\_data.scenario](#t3co.input_data.scenario)
  * [Scenario](#t3co.input_data.scenario.Scenario)
    * [\_\_new\_\_](#t3co.input_data.scenario.Scenario.__new__)
    * [from\_file](#t3co.input_data.scenario.Scenario.from_file)
    * [override\_from\_config](#t3co.input_data.scenario.Scenario.override_from_config)
    * [get\_discounted\_value](#t3co.input_data.scenario.Scenario.get_discounted_value)
    * [delete\_dataframes](#t3co.input_data.scenario.Scenario.delete_dataframes)
* [t3co.cli](#t3co.cli)
* [t3co.cli.sweep](#t3co.cli.sweep)
  * [load\_vehicle\_scenario\_energy](#t3co.cli.sweep.load_vehicle_scenario_energy)
  * [generate\_ledger](#t3co.cli.sweep.generate_ledger)
  * [create\_results\_filepath](#t3co.cli.sweep.create_results_filepath)
  * [export\_results\_to\_csv](#t3co.cli.sweep.export_results_to_csv)
  * [run\_t3co](#t3co.cli.sweep.run_t3co)
* [t3co.visualize.charts](#t3co.visualize.charts)
* [t3co.visualize](#t3co.visualize)
* [t3co.cost\_models.operating\_costs](#t3co.cost_models.operating_costs)
  * [OperatingCosts](#t3co.cost_models.operating_costs.OperatingCosts)
    * [\_\_new\_\_](#t3co.cost_models.operating_costs.OperatingCosts.__new__)
    * [\_\_init\_\_](#t3co.cost_models.operating_costs.OperatingCosts.__init__)
    * [set\_fuel\_cost](#t3co.cost_models.operating_costs.OperatingCosts.set_fuel_cost)
    * [set\_maintenance\_oper\_cost](#t3co.cost_models.operating_costs.OperatingCosts.set_maintenance_oper_cost)
    * [set\_insurance\_cost](#t3co.cost_models.operating_costs.OperatingCosts.set_insurance_cost)
    * [set\_purchasing\_payment\_cost](#t3co.cost_models.operating_costs.OperatingCosts.set_purchasing_payment_cost)
    * [set\_fueling\_dwell\_labor\_cost](#t3co.cost_models.operating_costs.OperatingCosts.set_fueling_dwell_labor_cost)
    * [set\_net\_oper\_cost](#t3co.cost_models.operating_costs.OperatingCosts.set_net_oper_cost)
    * [set\_disc\_oper\_cost](#t3co.cost_models.operating_costs.OperatingCosts.set_disc_oper_cost)
    * [\_\_str\_\_](#t3co.cost_models.operating_costs.OperatingCosts.__str__)
* [t3co.cost\_models](#t3co.cost_models)
* [t3co.cost\_models.opportunity\_costs](#t3co.cost_models.opportunity_costs)
  * [OpportunityCosts](#t3co.cost_models.opportunity_costs.OpportunityCosts)
    * [\_\_new\_\_](#t3co.cost_models.opportunity_costs.OpportunityCosts.__new__)
    * [\_\_init\_\_](#t3co.cost_models.opportunity_costs.OpportunityCosts.__init__)
    * [set\_payload\_cap\_cost\_multiplier](#t3co.cost_models.opportunity_costs.OpportunityCosts.set_payload_cap_cost_multiplier)
    * [set\_fueling\_dwell\_time\_cost](#t3co.cost_models.opportunity_costs.OpportunityCosts.set_fueling_dwell_time_cost)
    * [set\_mr\_downtime\_cost](#t3co.cost_models.opportunity_costs.OpportunityCosts.set_mr_downtime_cost)
    * [set\_net\_downtime\_oppy\_cost](#t3co.cost_models.opportunity_costs.OpportunityCosts.set_net_downtime_oppy_cost)
    * [set\_disc\_downtime\_oppy\_cost](#t3co.cost_models.opportunity_costs.OpportunityCosts.set_disc_downtime_oppy_cost)
    * [\_\_str\_\_](#t3co.cost_models.opportunity_costs.OpportunityCosts.__str__)
* [t3co.cost\_models.capital\_costs](#t3co.cost_models.capital_costs)
  * [CapitalCosts](#t3co.cost_models.capital_costs.CapitalCosts)
    * [\_\_new\_\_](#t3co.cost_models.capital_costs.CapitalCosts.__new__)
    * [\_\_init\_\_](#t3co.cost_models.capital_costs.CapitalCosts.__init__)
    * [set\_glider\_cost](#t3co.cost_models.capital_costs.CapitalCosts.set_glider_cost)
    * [set\_fuel\_converter\_cost\_dol](#t3co.cost_models.capital_costs.CapitalCosts.set_fuel_converter_cost_dol)
    * [set\_fuel\_storage\_cost](#t3co.cost_models.capital_costs.CapitalCosts.set_fuel_storage_cost)
    * [set\_motor\_control\_power\_elecs\_cost](#t3co.cost_models.capital_costs.CapitalCosts.set_motor_control_power_elecs_cost)
    * [set\_plug\_cost](#t3co.cost_models.capital_costs.CapitalCosts.set_plug_cost)
    * [set\_battery\_cost](#t3co.cost_models.capital_costs.CapitalCosts.set_battery_cost)
    * [set\_msrp](#t3co.cost_models.capital_costs.CapitalCosts.set_msrp)
    * [set\_purchase\_tax](#t3co.cost_models.capital_costs.CapitalCosts.set_purchase_tax)
    * [set\_downpayment](#t3co.cost_models.capital_costs.CapitalCosts.set_downpayment)
    * [set\_residual\_cost](#t3co.cost_models.capital_costs.CapitalCosts.set_residual_cost)
    * [set\_net\_capital\_cost](#t3co.cost_models.capital_costs.CapitalCosts.set_net_capital_cost)
    * [set\_disc\_residual\_cost](#t3co.cost_models.capital_costs.CapitalCosts.set_disc_residual_cost)
    * [get\_marked\_up\_value](#t3co.cost_models.capital_costs.CapitalCosts.get_marked_up_value)
* [t3co.demos](#t3co.demos)
* [t3co.demos.demo](#t3co.demos.demo)

<a id="t3co"></a>

# t3co

Python Package Template

<a id="t3co.tco.ledger"></a>

# t3co.tco.ledger

<a id="t3co.tco.ledger.Ledger"></a>

## Ledger Objects

```python
class Ledger()
```

<a id="t3co.tco.ledger.Ledger.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the Ledger class.

<a id="t3co.tco.ledger.Ledger.__init__"></a>

#### \_\_init\_\_

```python
def __init__(vehicle: Vehicle,
             scenario: Scenario,
             energy: Energy = None,
             config: Config = None)
```

Initializes the Ledger instance.

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance.
- `energy` _Energy, optional_ - The energy instance. Defaults to None.
- `config` _Config, optional_ - The configuration instance. Defaults to None.

<a id="t3co.tco.ledger.Ledger.set_discounted_costs"></a>

#### set\_discounted\_costs

```python
def set_discounted_costs()
```

Sets the discounted cost components for the Ledger instance.

<a id="t3co.tco.ledger.Ledger.set_discounted_tco"></a>

#### set\_discounted\_tco

```python
def set_discounted_tco()
```

Sets the discounted TCO for the Ledger instance.

<a id="t3co.tco.ledger.Ledger.set_cost_components"></a>

#### set\_cost\_components

```python
def set_cost_components()
```

Sets the cost components for the Ledger instance.

<a id="t3co.tco.ledger.Ledger.to_dict"></a>

#### to\_dict

```python
def to_dict(include_prefix: bool = True, flatten: bool = True) -> dict
```

Exports the Ledger instance to a dictionary.

**Arguments**:

- `include_prefix` _bool, optional_ - If True, exported column names contain the T3CO submodule names as prefix. Defaults to True.
- `flatten` _bool, optional_ - If True, the nested dict output flattens to a single dictionary. Defaults to True.
  

**Returns**:

- `dict` - The Ledger instance as a dictionary.

<a id="t3co.tco.ledger.Ledger.to_json"></a>

#### to\_json

```python
def to_json(filepath: Union[str, Path],
            include_prefix: bool = True,
            flatten: bool = True) -> None
```

Saves the Ledger instance to a JSON file.

**Arguments**:

- `filepath` _Union[str, Path]_ - The file path where the JSON will be saved.
- `include_prefix` _bool, optional_ - If True, exported column names contain the T3CO submodule names as prefix. Defaults to True.
- `flatten` _bool, optional_ - If True, the nested dict output flattens to a single dictionary. Defaults to True.

<a id="t3co.tco.ledger.Ledger.to_df"></a>

#### to\_df

```python
def to_df() -> pd.DataFrame
```

Converts the Ledger instance to a DataFrame.

**Returns**:

- `pd.DataFrame` - The Ledger instance as a DataFrame.

<a id="t3co.tco.ledger.Ledger.to_csv"></a>

#### to\_csv

```python
def to_csv(filepath: Union[str, Path]) -> None
```

Saves the Ledger instance to a CSV file.

**Arguments**:

- `filepath` _Union[str, Path]_ - The file path where the CSV will be saved.

<a id="t3co.tco.ledger.Ledger.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns a string representation of the Ledger instance.

**Returns**:

- `str` - String representation of the Ledger instance.

<a id="t3co.tco"></a>

# t3co.tco

<a id="t3co.tco.tcocalc"></a>

# t3co.tco.tcocalc

<a id="t3co.tco.tcocalc.TCOCalc"></a>

## TCOCalc Objects

```python
class TCOCalc()
```

<a id="t3co.tco.tcocalc.TCOCalc.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the TCOCalc class.

<a id="t3co.tco.tcocalc.TCOCalc.__init__"></a>

#### \_\_init\_\_

```python
def __init__(year_index: int,
             vehicle: Vehicle,
             scenario: Scenario,
             energy: Energy,
             payload_cap_cost_multiplier: float = None,
             cap_costs: CapitalCosts = None)
```

Initializes the TCOCalc instance.

**Arguments**:

- `year_index` _int_ - The year index.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance.
- `energy` _Energy_ - The energy instance.
- `payload_cap_cost_multiplier` _float, optional_ - Payload capacity cost multiplier. Defaults to None.
- `cap_costs` _CapitalCosts, optional_ - Capital costs instance. Defaults to None.

<a id="t3co.tco.tcocalc.TCOCalc.calculate_capital_costs"></a>

#### calculate\_capital\_costs

```python
def calculate_capital_costs(vehicle: Vehicle, scenario: Scenario) -> None
```

Calculates the capital costs.

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance.

<a id="t3co.tco.tcocalc.TCOCalc.calculate_opportunity_costs"></a>

#### calculate\_opportunity\_costs

```python
def calculate_opportunity_costs(vehicle: Vehicle, scenario: Scenario,
                                energy: Energy) -> None
```

Calculates the opportunity costs.

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance.
- `energy` _Energy_ - The energy instance.

<a id="t3co.tco.tcocalc.TCOCalc.calculate_operating_costs"></a>

#### calculate\_operating\_costs

```python
def calculate_operating_costs(vehicle: Vehicle, scenario: Scenario,
                              energy: Energy) -> None
```

Calculates the operating costs.

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance.
- `energy` _Energy_ - The energy instance.

<a id="t3co.tco.tcocalc.TCOCalc.set_total_cost"></a>

#### set\_total\_cost

```python
def set_total_cost(scenario: Scenario) -> None
```

Sets the total cost for the year.

**Arguments**:

- `scenario` _Scenario_ - The scenario instance.

<a id="t3co.tco.tcocalc.TCOCalc.set_disc_total_cost"></a>

#### set\_disc\_total\_cost

```python
def set_disc_total_cost(vehicle: Vehicle,
                        scenario: Scenario,
                        payload_cap_cost_multiplier: float = None,
                        TCO_switch="DIRECT") -> None
```

Sets the discounted total cost for the year.

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance.
- `payload_cap_cost_multiplier` _float, optional_ - Payload capacity cost multiplier. Defaults to None.
- `TCO_switch` _str, optional_ - TCO calculation method. Defaults to "DIRECT".

<a id="t3co.tco.tcocalc.TCOCalc.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns a string representation of the TCOCalc instance.

**Returns**:

- `str` - String representation of the TCOCalc instance.

<a id="t3co.optimize"></a>

# t3co.optimize

<a id="t3co.constants.Global"></a>

# t3co.constants.Global

Global constants
Stores paths to directories used for input files, as well as constants referenced throughout the code base

<a id="t3co.constants.Global.DieselGalPerGasGal"></a>

#### DieselGalPerGasGal

energy equivalent gallons of diesel per 1 gallon gas

<a id="t3co.constants.Global.kgH2_per_gge"></a>

#### kgH2\_per\_gge

https://epact.energy.gov/fuel-conversion-factors for Hydrogen

<a id="t3co.constants.Global.mps_to_mph"></a>

#### mps\_to\_mph

1 mps = 2.23694 mph

<a id="t3co.constants.Global.m_to_mi"></a>

#### m\_to\_mi

1 m = 0.000621371 mi

<a id="t3co.constants.Global.set_tco_intermediates"></a>

#### set\_tco\_intermediates

```python
def set_tco_intermediates()
```

This function sets path for TCO_INTERMEDIATES to save tsv files

<a id="t3co.constants.Global.set_tco_results"></a>

#### set\_tco\_results

```python
def set_tco_results()
```

This function sets path for TCO_RESULTS

<a id="t3co.constants.Global.kg_to_lbs"></a>

#### kg\_to\_lbs

```python
def kg_to_lbs(kgs: float) -> float
```

This function converts kg to lb

**Arguments**:

- `kgs` _float_ - mass in kg
  

**Returns**:

- `(float)` - mass in pounds

<a id="t3co.constants.Global.lbs_to_kgs"></a>

#### lbs\_to\_kgs

```python
def lbs_to_kgs(lbs: float) -> float
```

This function converts lb to kg

**Arguments**:

- `lbs` _float_ - mass in pounds
  

**Returns**:

- `(float)` - mass in kg

<a id="t3co.constants.Global.not_falsy"></a>

#### not\_falsy

```python
def not_falsy(var: float) -> bool
```

This function returns True to verify that var is NOT falsy: not in [None, np.nan, 0, False]


**Arguments**:

- `var` _float_ - variable to check
  

**Returns**:

- `(bool)` - True if not in [None, 0, False]

<a id="t3co.constants"></a>

# t3co.constants

<a id="t3co.resources"></a>

# t3co.resources

<a id="t3co.energy_models"></a>

# t3co.energy\_models

<a id="t3co.energy_models.energy"></a>

# t3co.energy\_models.energy

<a id="t3co.energy_models.energy.Energy"></a>

## Energy Objects

```python
@dataclass
class Energy()
```

<a id="t3co.energy_models.energy.Energy.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the Energy class.

<a id="t3co.energy_models.energy.Energy.__init__"></a>

#### \_\_init\_\_

```python
def __init__(mpgge: float = None, primary_fuel_range_mi: float = None)
```

Initializes the Energy instance.

**Arguments**:

- `mpgge` _float, optional_ - Miles per gallon gasoline equivalent. Defaults to None.
- `primary_fuel_range_mi` _float, optional_ - Primary fuel range in miles. Defaults to None.

<a id="t3co.energy_models.energy.Energy.run_fastsim_model"></a>

#### run\_fastsim\_model

```python
def run_fastsim_model(
    veh_no: int,
    scenario: Scenario,
    vehicle_file: Union[str, Path] = gl.RESOURCES_FOLDERPATH / "inputs" /
    "Demo_FY22_vehicle_model_assumptions.csv"
) -> None
```

Runs the FASTSim model to calculate mpgge and primary fuel range.

**Arguments**:

- `veh_no` _int_ - Vehicle selection number.
- `scenario` _Scenario_ - Scenario instance containing configuration data.
- `vehicle_file` _Union[str, Path], optional_ - Vehicle model assumptions input CSV file path. Defaults to gl.RESOURCES_FOLDERPATH / "inputs" / "Demo_FY22_vehicle_model_assumptions.csv".

<a id="t3co.energy_models.fastsim_model.fastsim_wrapper"></a>

# t3co.energy\_models.fastsim\_model.fastsim\_wrapper

<a id="t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim"></a>

## RunFastsim Objects

```python
class RunFastsim()
```

<a id="t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the RunFastsim class.

<a id="t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim.load_vehicle"></a>

#### load\_vehicle

```python
def load_vehicle(veh_no: int,
                 veh_input_path: Union[str, Path],
                 use_rust: bool = True) -> fastsim.vehicle.Vehicle
```

Loads vehicle object from vehicle number and input CSV filepath.

**Arguments**:

- `veh_no` _int_ - Vehicle selection number.
- `veh_input_path` _Union[str, Path]_ - Vehicle model assumptions input CSV file path.
  

**Returns**:

- `fastsim.vehicle.Vehicle` - FASTSim vehicle object.

<a id="t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim.load_design_cycle_from_scenario"></a>

#### load\_design\_cycle\_from\_scenario

```python
def load_design_cycle_from_scenario(
    scenario: Scenario,
    cyc_file_path: Union[str, Path] = gl.CYCLES_FOLDER,
    return_rustcycle: bool = True
) -> Union[fastsim.cycle.Cycle, List[fastsim.cycle.Cycle]]
```

Loads the design cycle used for mpgge and range determination.

**Arguments**:

- `scenario` _Scenario_ - Scenario object for current selection.
- `cyc_file_path` _Union[str, Path], optional_ - Drive cycle input file path. Defaults to gl.CYCLES_FOLDER.
  

**Returns**:

  Union[fastsim.cycle.Cycle, List[fastsim.cycle.Cycle]]: FASTSim cycle object for current Scenario object.

<a id="t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim.load_design_cycle_from_path"></a>

#### load\_design\_cycle\_from\_path

```python
def load_design_cycle_from_path(
    cyc_file_path: Union[str, Path],
    return_rustcycle: bool = True
) -> Union[fastsim.cycle.RustCycle, fastsim.cycle.Cycle]
```

Loads the Cycle object from the drive cycle filepath.

**Arguments**:

- `cyc_file_path` _Union[str, Path]_ - Drive cycle input file path.
  

**Returns**:

- `fastsim.cycle.Cycle` - FASTSim cycle object for current Scenario object.

<a id="t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim.get_simdrive"></a>

#### get\_simdrive

```python
def get_simdrive(
        cycle: fastsim.cycle.Cycle) -> fastsim.fastsimrust.RustSimDrive
```

Creates a SimDrive object for the given cycle and vehicle.

**Arguments**:

- `cycle` _fastsim.cycle.Cycle_ - The drive cycle.
  

**Returns**:

- `fastsim.fastsimrust.RustSimDrive` - The RustSimDrive object.

<a id="t3co.energy_models.fastsim_model.fastsim_wrapper.RunFastsim.get_range"></a>

#### get\_range

```python
def get_range() -> None
```

Calculates the range of the vehicle based on its type and energy storage.

<a id="t3co.energy_models.fastsim_model"></a>

# t3co.energy\_models.fastsim\_model

<a id="t3co.utils"></a>

# t3co.utils

<a id="t3co.utils.print_class_objects"></a>

# t3co.utils.print\_class\_objects

<a id="t3co.utils.print_class_objects.obj_to_string"></a>

#### obj\_to\_string

```python
def obj_to_string(obj: Union[object, List[object]],
                  extra: str = "    ") -> str
```

Converts an object or list of objects to a formatted string representation.

**Arguments**:

- `obj` _Union[object, List[object]]_ - The object or list of objects to convert.
- `extra` _str, optional_ - Indentation string for nested objects. Defaults to "    ".
  

**Returns**:

- `str` - Formatted string representation of the object.

<a id="t3co.utils.print_class_objects.handle_nan"></a>

#### handle\_nan

```python
def handle_nan(
        obj: Union[float, dict, list]) -> Union[None, dict, list, float]
```

Replaces NaN values in an object with None.

**Arguments**:

- `obj` _Union[float, dict, list]_ - The object to process.
  

**Returns**:

  Union[None, dict, list, float]: The processed object with NaN values replaced by None.

<a id="t3co.utils.print_class_objects.custom_default"></a>

#### custom\_default

```python
def custom_default(obj: object) -> Union[None, dict, str]
```

Custom default function for JSON serialization.

**Arguments**:

- `obj` _object_ - The object to serialize.
  

**Returns**:

  Union[None, dict, str]: The serialized object.

<a id="t3co.utils.print_class_objects.to_flat_dict"></a>

#### to\_flat\_dict

```python
def to_flat_dict(obj: object,
                 include_predix: bool = True,
                 prefix: str = "",
                 delimiter: str = "_") -> dict
```

Flattens a nested object into a dictionary.

**Arguments**:

- `obj` _object_ - The object to flatten.
- `include_predix` _bool, optional_ - Whether to include the prefix in the keys. Defaults to True.
- `prefix` _str, optional_ - The prefix for the keys. Defaults to "".
- `delimiter` _str, optional_ - The delimiter for the keys. Defaults to "_".
  

**Returns**:

- `dict` - The flattened dictionary.

<a id="t3co.utils.print_class_objects.remove_df_attrs"></a>

#### remove\_df\_attrs

```python
def remove_df_attrs(obj: object) -> None
```

Removes DataFrame attributes from an object.

**Arguments**:

- `obj` _object_ - The object to process.

<a id="t3co.utils.demo_files_installer"></a>

# t3co.utils.demo\_files\_installer

<a id="t3co.utils.demo_files_installer.main"></a>

#### main

```python
def main()
```

Requests user inputs for whether and where to copy t3co demo input files from the t3co.resources folder. Calls the copy_demo_input_files function.

<a id="t3co.utils.demo_files_installer.copy_demo_input_files"></a>

#### copy\_demo\_input\_files

```python
def copy_demo_input_files(destination_path: Union[str, Path]) -> None
```

Copies the t3co.resources folder that includes demo input files to a user input destination_path.

**Arguments**:

- `destination_path` _Union[str, Path]_ - Path of destination directory for copying t3co.resources folder.

<a id="t3co.input_data.config"></a>

# t3co.input\_data.config

<a id="t3co.input_data.config.Config"></a>

## Config Objects

```python
@dataclass
class Config()
```

<a id="t3co.input_data.config.Config.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the Config class.

<a id="t3co.input_data.config.Config.from_file"></a>

#### from\_file

```python
def from_file(
        analysis_id: int = 0,
        filename: str = gl.RESOURCES_FOLDERPATH / "T3COConfig.csv") -> Self
```

Generates a Config dictionary from CSV file and calls Config.from_dict.

**Arguments**:

- `filename` _str_ - Path of input T3CO Config file.
- `analysis_id` _int_ - Analysis ID selections.
  

**Returns**:

- `Self` - Config instance containing all values from T3CO Config CSV file.

<a id="t3co.input_data.config.Config.from_dict"></a>

#### from\_dict

```python
def from_dict(config_dict: dict) -> Self
```

Generates a Config instance from config_dict.

**Arguments**:

- `config_dict` _dict_ - Dictionary containing fields from T3CO Config input CSV file.
  

**Returns**:

- `Self` - Config instance containing all values from T3CO Config CSV file.

<a id="t3co.input_data.config.Config.validate_analysis_id"></a>

#### validate\_analysis\_id

```python
def validate_analysis_id() -> pd.DataFrame
```

Validates that the correct analysis ID is input.

**Returns**:

- `pd.DataFrame` - DataFrame containing the configuration data for the given analysis ID.
  

**Raises**:

- `Exception` - If analysis_id is not found or config file does not exist.

<a id="t3co.input_data.config.Config.check_drivecycles_and_create_selections"></a>

#### check\_drivecycles\_and\_create\_selections

```python
def check_drivecycles_and_create_selections() -> None
```

Checks if the config.drive_cycle input is a file or a folder. If a folder is provided, creates a list of all selections for each drive cycle in the folder as config.dc_files.

<a id="t3co.input_data.config.Config.read_auxiliary_files"></a>

#### read\_auxiliary\_files

```python
def read_auxiliary_files() -> None
```

Reads auxiliary files such as fuel prices and residual rates.

<a id="t3co.input_data.config.Config.delete_dataframes"></a>

#### delete\_dataframes

```python
def delete_dataframes() -> None
```

Deletes DataFrame attributes from the Config instance.

<a id="t3co.input_data.vehicle"></a>

# t3co.input\_data.vehicle

<a id="t3co.input_data.vehicle.Vehicle"></a>

## Vehicle Objects

```python
@dataclass
class Vehicle()
```

<a id="t3co.input_data.vehicle.Vehicle.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the OpportunityCosts class.

<a id="t3co.input_data.vehicle.Vehicle.from_config"></a>

#### from\_config

```python
@classmethod
def from_config(cls, selection: int, config: Config) -> Self
```

Creates a Vehicle instance from the configuration.

**Arguments**:

- `selection` _int_ - The selection index.
- `config` _Config_ - The configuration instance.
  

**Returns**:

- `Self` - An instance of the Vehicle class.

<a id="t3co.input_data.vehicle.Vehicle.from_db"></a>

#### from\_db

```python
@classmethod
def from_db(cls, selection: int, vehicle_db_file: Union[str, Path]) -> Self
```

Creates a Vehicle instance from the vehicle database file.

**Arguments**:

- `selection` _int_ - The selection index.
- `vehicle_db_file` _Union[str, Path]_ - The vehicle database file path.
  

**Returns**:

- `Self` - An instance of the Vehicle class.

<a id="t3co.input_data.vehicle.Vehicle.set_veh_kg"></a>

#### set\_veh\_kg

```python
def set_veh_kg() -> None
```

Sets the vehicle weight in kilograms.

<a id="t3co.input_data.vehicle.Vehicle.delete_dataframes"></a>

#### delete\_dataframes

```python
def delete_dataframes() -> None
```

Deletes DataFrame attributes from the Vehicle instance.

<a id="t3co.input_data"></a>

# t3co.input\_data

<a id="t3co.input_data.scenario"></a>

# t3co.input\_data.scenario

<a id="t3co.input_data.scenario.Scenario"></a>

## Scenario Objects

```python
@dataclass
class Scenario()
```

Class object that contains all TCO parameters and performance target (range, grade, accel) information
for a vehicle such that performance and TCO can be computed during optimization.

<a id="t3co.input_data.scenario.Scenario.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the Scenario class.

<a id="t3co.input_data.scenario.Scenario.from_file"></a>

#### from\_file

```python
@classmethod
def from_file(
    cls,
    selection: int,
    scenario_file: Union[str, Path] = gl.RESOURCES_FOLDERPATH / "inputs" /
    "Demo_FY22_scenario_assumptions.csv"
) -> Self
```

Creates a Scenario instance from a CSV file.

**Arguments**:

- `selection` _int_ - The selection index to filter the scenario data.
- `scenario_file` _Union[str, Path]_ - Path to the scenario CSV file.
  

**Returns**:

- `Scenario` - An instance of the Scenario class.

<a id="t3co.input_data.scenario.Scenario.override_from_config"></a>

#### override\_from\_config

```python
def override_from_config(config: Config = None, verbose: bool = False) -> Self
```

Overrides certain scenario fields if use_config is True and config object is not None.

**Arguments**:

- `config` _Config, optional_ - Config object containing configuration data. Defaults to None.
- `verbose` _bool, optional_ - If True, prints the overridden fields. Defaults to False.
  

**Raises**:

- `Exception` - If config file is not attached or scenario.use_config is set to False.

<a id="t3co.input_data.scenario.Scenario.get_discounted_value"></a>

#### get\_discounted\_value

```python
def get_discounted_value(value: float, year_number: int) -> float
```

Calculates the discounted value for a given year.

**Arguments**:

- `value` _float_ - The value to be discounted.
- `year_number` _int_ - The year number for discounting.
  

**Returns**:

- `float` - The discounted value.

<a id="t3co.input_data.scenario.Scenario.delete_dataframes"></a>

#### delete\_dataframes

```python
def delete_dataframes() -> None
```

Deletes DataFrame attributes from the Scenario instance.

<a id="t3co.cli"></a>

# t3co.cli

<a id="t3co.cli.sweep"></a>

# t3co.cli.sweep

<a id="t3co.cli.sweep.load_vehicle_scenario_energy"></a>

#### load\_vehicle\_scenario\_energy

```python
def load_vehicle_scenario_energy(
        selection: Union[int, str],
        config: Config,
        vehicle: Vehicle = None,
        scenario: Scenario = None,
        energy: Energy = None) -> Tuple[Vehicle, Scenario, Energy]
```

Loads the vehicle, scenario, and energy models based on the selection and config.

**Arguments**:

- `selection` _Union[int, str]_ - The selection index or string.
- `config` _Config_ - The configuration instance.
  

**Returns**:

  Tuple[Vehicle, Scenario, Energy]: The vehicle, scenario, and energy models.

<a id="t3co.cli.sweep.generate_ledger"></a>

#### generate\_ledger

```python
def generate_ledger(selection: int, config: Config) -> Dict
```

Generates the ledger for the given selection and config.

**Arguments**:

- `selection` _int_ - The selection index.
- `config` _Config_ - The configuration instance.
  

**Returns**:

- `Dict` - The ledger as a dictionary.

<a id="t3co.cli.sweep.create_results_filepath"></a>

#### create\_results\_filepath

```python
def create_results_filepath(config: Config) -> Path
```

Creates the results file path based on the config.

**Arguments**:

- `config` _Config_ - The configuration instance.
  

**Returns**:

- `Path` - The path to the results file.

<a id="t3co.cli.sweep.export_results_to_csv"></a>

#### export\_results\_to\_csv

```python
def export_results_to_csv(
    reports_list: List[Dict],
    config: Config,
    output_path: Union[str, Path] = None,
    return_filepath: bool = True,
    return_df: bool = False,
    sort_values: bool = False
) -> Tuple[Union[Path, None], Union[pd.DataFrame, None]]
```

Exports the results to a CSV file.

**Arguments**:

- `reports_list` _List[Dict]_ - The list of reports.
- `config` _Config_ - The configuration instance.
- `output_path` _Union[str, Path], optional_ - The output path for the CSV file. Defaults to None.
- `return_filepath` _bool, optional_ - Whether to return the file path. Defaults to True.
- `return_df` _bool, optional_ - Whether to return the DataFrame. Defaults to False.
- `sort_values` _bool, optional_ - Whether to sort the values by selection. Defaults to False.
  

**Returns**:

  Tuple[Union[Path, None], Union[pd.DataFrame, None]]: The output path and DataFrame if specified.

<a id="t3co.cli.sweep.run_t3co"></a>

#### run\_t3co

```python
def run_t3co(config: Config, save_results: bool = True) -> None
```

Runs the T3CO analysis.

**Arguments**:

- `config` _Config_ - The configuration instance.
- `save_results` _bool, optional_ - Whether to save the results. Defaults to True.

<a id="t3co.visualize.charts"></a>

# t3co.visualize.charts

<a id="t3co.visualize"></a>

# t3co.visualize

<a id="t3co.cost_models.operating_costs"></a>

# t3co.cost\_models.operating\_costs

<a id="t3co.cost_models.operating_costs.OperatingCosts"></a>

## OperatingCosts Objects

```python
class OperatingCosts()
```

<a id="t3co.cost_models.operating_costs.OperatingCosts.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the OperatingCosts class.

<a id="t3co.cost_models.operating_costs.OperatingCosts.__init__"></a>

#### \_\_init\_\_

```python
def __init__(year_number: int,
             cap_costs: CapitalCosts,
             vehicle: Vehicle,
             scenario: Scenario,
             energy: Energy = None,
             oppy_costs: OpportunityCosts = None)
```

Initializes the OperatingCosts instance.

**Arguments**:

- `year_number` _int_ - The year number for which the operating costs are calculated.
- `cap_costs` _CapitalCosts_ - The capital costs associated with the vehicle.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.
- `energy` _Energy_ - The energy model instance.
- `oppy_costs` _OpportunityCosts_ - The opportunity costs associated with the vehicle.

<a id="t3co.cost_models.operating_costs.OperatingCosts.set_fuel_cost"></a>

#### set\_fuel\_cost

```python
def set_fuel_cost(year_number: int, vehicle: Vehicle,
                  scenario: Scenario) -> None
```

Sets the fuel cost for the given year.

This method calculates the fuel cost based on the fuel price and the amount of fuel used.
The calculation uses the following OperatingCosts elements:
- distance_traveled_mi_per_yr
- mpgge

Inputs from scenario:
- fuel_prices_df
- fuel_type
- model_year
- region

Estimated class variables:
- fuel_price_dol_per_gge
- fuel_used_gal_gge_per_yr
- fuel_used_gal_gde_per_yr
- energy_used_kwh_per_yr
- fuel_cost_dol_per_yr

**Arguments**:

- `year_number` _int_ - The year number for which the fuel cost is calculated.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co.cost_models.operating_costs.OperatingCosts.set_maintenance_oper_cost"></a>

#### set\_maintenance\_oper\_cost

```python
def set_maintenance_oper_cost(year_number: int, vehicle: Vehicle,
                              scenario: Scenario) -> None
```

Sets the maintenance operating cost for the given year.

This method calculates the maintenance cost based on the maintenance cost per mile and the distance traveled.

Inputs from scenario:
- maint_oper_cost_dol_per_mi
- vmt

Estimated class variables:
- maintenance_cost_dol_per_mi
- maintenance_cost_dol_per_yr

**Arguments**:

- `year_number` _int_ - The year number for which the maintenance cost is calculated.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co.cost_models.operating_costs.OperatingCosts.set_insurance_cost"></a>

#### set\_insurance\_cost

```python
def set_insurance_cost(year_number: int, cap_cost: CapitalCosts,
                       vehicle: Vehicle, scenario: Scenario) -> None
```

Sets the insurance cost for the given year.

This method calculates the insurance cost based on the insurance rate and the total value of the vehicle.

Inputs from scenario:
- insurance_rates_pct_per_yr

Inputs from cap_cost:
- msrp_total_dol

Estimated class variables:
- insurance_cost_dol_per_yr

**Arguments**:

- `year_number` _int_ - The year number for which the insurance cost is calculated.
- `cap_cost` _CapitalCosts_ - The capital costs associated with the vehicle.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co.cost_models.operating_costs.OperatingCosts.set_purchasing_payment_cost"></a>

#### set\_purchasing\_payment\_cost

```python
def set_purchasing_payment_cost(year_number: int, scenario: Scenario,
                                cap_costs: CapitalCosts)
```

Sets the purchasing payment cost for the given year.

This method calculates the purchasing payment cost based on the purchasing method specified in the scenario.

Inputs from scenario:
- purchasing_method
- purchasing_interest_apr_pct_per_yr
- purchasing_payment_frequency_months
- purchasing_term_yr
- tax_rate_pct
- leasing_money_factor

Inputs from cap_costs:
- purchasing_initial_principal_dol
- msrp_total_dol
- purchase_tax_dol
- purchasing_downpayment_dol
- residual_cost_dol

Estimated OperatingCosts variables:
- purchasing_payment_dol_per_yr
- purchasing_cost_dol_per_yr
- purchasing_remaining_principal_dol
- purchasing_tax_amount_dol_per_year

**Arguments**:

- `year_number` _int_ - The year number for which the purchasing payment cost is calculated.
- `scenario` _Scenario_ - The scenario instance containing configuration data, including the purchasing method, interest rate, and term.
- `cap_costs` _CapitalCosts_ - The capital costs associated with the vehicle.

<a id="t3co.cost_models.operating_costs.OperatingCosts.set_fueling_dwell_labor_cost"></a>

#### set\_fueling\_dwell\_labor\_cost

```python
def set_fueling_dwell_labor_cost(scenario: Scenario,
                                 oppy_costs: OpportunityCosts) -> None
```

Sets the fueling dwell labor cost for the given year.

This method calculates the fueling dwell labor cost based on the fueling dwell time and the labor rate.

Inputs from scenario:
- labor_rate_dol_per_hr

Inputs from oppy_costs:
- fueling_dwell_time_hr_per_yr

Estimated OperatingCosts variables:
- fueling_dwell_labor_cost_dol_per_yr

**Arguments**:

- `scenario` _Scenario_ - The scenario instance containing configuration data.
- `oppy_costs` _OpportunityCosts_ - The opportunity costs associated with the vehicle.

<a id="t3co.cost_models.operating_costs.OperatingCosts.set_net_oper_cost"></a>

#### set\_net\_oper\_cost

```python
def set_net_oper_cost() -> None
```

Sets the net operating cost for the given year.

This method calculates the net operating cost by summing the various operating cost components.
The calculation uses the following OperatingCosts elements:
- fuel_cost_dol_per_yr
- fueling_dwell_labor_cost_dol_per_yr
- maintenance_cost_dol_per_yr
- insurance_cost_dol_per_yr
- purchasing_payment_dol_per_yr

Estimated OperatingCosts variables:
- net_oper_cost_dol_per_yr

<a id="t3co.cost_models.operating_costs.OperatingCosts.set_disc_oper_cost"></a>

#### set\_disc\_oper\_cost

```python
def set_disc_oper_cost(year_number: int, scenario: Scenario) -> None
```

Sets the discounted operating cost for the given year.

This method calculates the discounted operating cost based on the net operating cost and the discount rate.
The calculation uses the following OperatingCosts elements:
- net_oper_cost_dol_per_yr

Inputs from scenario:
- discount_rate_pct_per_yr

Estimated OperatingCosts variables:
- disc_oper_cost_dol_per_yr

**Arguments**:

- `year_number` _int_ - The year number for which the discounted operating cost is calculated.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co.cost_models.operating_costs.OperatingCosts.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns a string representation of the OperatingCosts instance.

**Returns**:

- `str` - String representation of the OperatingCosts instance.

<a id="t3co.cost_models"></a>

# t3co.cost\_models

<a id="t3co.cost_models.opportunity_costs"></a>

# t3co.cost\_models.opportunity\_costs

<a id="t3co.cost_models.opportunity_costs.OpportunityCosts"></a>

## OpportunityCosts Objects

```python
class OpportunityCosts()
```

<a id="t3co.cost_models.opportunity_costs.OpportunityCosts.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the OpportunityCosts class.

<a id="t3co.cost_models.opportunity_costs.OpportunityCosts.__init__"></a>

#### \_\_init\_\_

```python
def __init__(year_number: int, vehicle: Vehicle, scenario: Scenario,
             energy: Energy)
```

Initializes the OpportunityCosts instance.

**Arguments**:

- `year_number` _int_ - The year number for which the opportunity costs are calculated.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.
- `energy` _Energy_ - The energy model instance.

<a id="t3co.cost_models.opportunity_costs.OpportunityCosts.set_payload_cap_cost_multiplier"></a>

#### set\_payload\_cap\_cost\_multiplier

```python
def set_payload_cap_cost_multiplier(vehicle: Vehicle,
                                    scenario: Scenario) -> None
```

Sets the payload capacity cost multiplier for the vehicle.

This method calculates the payload capacity cost multiplier based on the vehicle's weight and the scenario's weight distribution.

Inputs from scenario:
- plf_weight_distribution_file
- plf_ref_veh_empty_mass_kg
- gvwr_kg
- gvwr_credit_kg

Inputs from vehicle:
- veh_kg
- cargo_kg

Estimated class variables:
- payload_cap_cost_multiplier

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co.cost_models.opportunity_costs.OpportunityCosts.set_fueling_dwell_time_cost"></a>

#### set\_fueling\_dwell\_time\_cost

```python
def set_fueling_dwell_time_cost(year_number: int, vehicle: Vehicle,
                                scenario: Scenario, energy: Energy) -> None
```

Calculates the fueling dwell time cost for a vehicle based on fuel fill rate/charging power and shifts per year.

Inputs from scenario:
- fdt_frac_full_charge_bounds
- shifts_per_year
- constant_trip_distance_mi
- vmt
- fdt_dwpt_fraction_power_pct
- ess_max_charging_power_kw
- fs_fueling_rate_gasoline_gpm
- fs_fueling_rate_diesel_gpm
- fdt_num_free_dwell_trips
- fdt_avg_overhead_hr_per_dwell_hr
- fdt_available_freetime_hr
- downtime_oppy_cost_dol_per_hr

Inputs from vehicle:
- veh_pt_type
- ess_max_kwh
- fs_kwh

Inputs from energy:
- primary_fuel_range_mi

Estimated OpportunityCosts variables:
- fdt_frac_full_charge_bounds
- shifts_per_year
- fdt_full_dwell_hr
- trip_distance_mi
- fdt_num_of_dwells
- fueling_dwell_time_hr_per_yr
- fueling_downtime_oppy_cost_dol_per_yr

**Arguments**:

- `year_number` _int_ - The year number for which the fueling dwell time cost is calculated.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.
- `energy` _Energy_ - The energy model instance.

<a id="t3co.cost_models.opportunity_costs.OpportunityCosts.set_mr_downtime_cost"></a>

#### set\_mr\_downtime\_cost

```python
def set_mr_downtime_cost(year_number: int, vehicle: Vehicle,
                         scenario: Scenario) -> None
```

Calculates the Maintenance and Repair (M&R) downtime cost based on planned, unplanned, and tire replacement downtime inputs.

Inputs from scenario:
- mr_planned_downtime_hr_per_yr
- mr_unplanned_downtime_hr_per_mi
- vmt
- mr_avg_tire_life_mi
- mr_tire_replace_downtime_hr_per_event
- downtime_oppy_cost_dol_per_hr

Estimated OpportunityCosts variables:
- mr_planned_downtime_hr
- mr_unplanned_downtime_hr
- mr_tire_replacement_downtime_hr
- mr_downtime_hr_per_yr
- mr_downtime_oppy_cost_dol_per_yr

**Arguments**:

- `year_number` _int_ - The year number for which the M&R downtime cost is calculated.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co.cost_models.opportunity_costs.OpportunityCosts.set_net_downtime_oppy_cost"></a>

#### set\_net\_downtime\_oppy\_cost

```python
def set_net_downtime_oppy_cost() -> None
```

Sets the net downtime opportunity cost for the vehicle.

This method calculates the net downtime opportunity cost by summing the fueling downtime and MR downtime opportunity costs.
The calculation uses the following OpportunityCosts elements:
- fueling_downtime_oppy_cost_dol_per_yr
- mr_downtime_oppy_cost_dol_per_yr
- fueling_dwell_time_hr_per_yr
- mr_downtime_hr_per_yr

Estimated OpportunityCosts variables:
- net_downtime_oppy_cost_dol_per_yr
- net_downtime_hr_per_yr

<a id="t3co.cost_models.opportunity_costs.OpportunityCosts.set_disc_downtime_oppy_cost"></a>

#### set\_disc\_downtime\_oppy\_cost

```python
def set_disc_downtime_oppy_cost(year_number: int, scenario: Scenario) -> None
```

Sets the discounted downtime opportunity cost for the given year.

Inputs from scenario:
- discount_rate_pct_per_yr

Estimated class variables:
- disc_downtime_oppy_cost_dol

**Arguments**:

- `year_number` _int_ - The year number for which the discounted downtime opportunity cost is calculated.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co.cost_models.opportunity_costs.OpportunityCosts.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns a string representation of the OpportunityCosts instance.

**Returns**:

- `str` - String representation of the OpportunityCosts instance.

<a id="t3co.cost_models.capital_costs"></a>

# t3co.cost\_models.capital\_costs

<a id="t3co.cost_models.capital_costs.CapitalCosts"></a>

## CapitalCosts Objects

```python
class CapitalCosts()
```

<a id="t3co.cost_models.capital_costs.CapitalCosts.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the CapitalCosts class.

<a id="t3co.cost_models.capital_costs.CapitalCosts.__init__"></a>

#### \_\_init\_\_

```python
def __init__(vehicle: Vehicle,
             scenario: Scenario,
             msrp_total_dol: float = None)
```

Initializes the CapitalCosts instance.

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.
- `msrp_total_dol` _float, optional_ - MSRP in dollars as input

<a id="t3co.cost_models.capital_costs.CapitalCosts.set_glider_cost"></a>

#### set\_glider\_cost

```python
def set_glider_cost(scenario: Scenario) -> None
```

Sets the glider cost for the vehicle.

This method calculates the marked up glider cost based on the vehicle class and the base cost.

Inputs from scenario:
- vehicle_glider_cost_dol

Estimated class variables:
- glider_cost_dol

**Arguments**:

- `scenario` _Scenario_ - The scenario instance containing configuration data, including the base cost for the glider.

<a id="t3co.cost_models.capital_costs.CapitalCosts.set_fuel_converter_cost_dol"></a>

#### set\_fuel\_converter\_cost\_dol

```python
def set_fuel_converter_cost_dol(vehicle: Vehicle, scenario: Scenario) -> None
```

Sets the fuel converter cost for the vehicle.

This method calculates the marked up fuel converter cost based on the vehicle powertrain type and the cost per kW.

Inputs from vehicle:
- fc_max_kw

Inputs from scenario:
- fc_fuelcell_cost_dol_per_kw
- fc_ice_cost_dol_per_kw
- fc_cng_ice_cost_dol_per_kw
- fc_ice_base_cost_dol

Estimated class variables:
- fuel_converter_cost_dol

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data, including the cost per kW for the fuel converter.

<a id="t3co.cost_models.capital_costs.CapitalCosts.set_fuel_storage_cost"></a>

#### set\_fuel\_storage\_cost

```python
def set_fuel_storage_cost(vehicle: Vehicle, scenario: Scenario) -> None
```

Sets the fuel storage cost for the vehicle.

This method calculates the marked up fuel storage cost based on the vehicle powertrain type and the cost per kWh.

Inputs from vehicle:
- fs_kwh

Inputs from scenario:
- fs_h2_cost_dol_per_kwh
- fs_cng_cost_dol_per_kwh
- fs_cost_dol_per_kwh

Estimated class variables:
- fuel_storage_cost_dol

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data, including the cost per kWh for the fuel storage.

<a id="t3co.cost_models.capital_costs.CapitalCosts.set_motor_control_power_elecs_cost"></a>

#### set\_motor\_control\_power\_elecs\_cost

```python
def set_motor_control_power_elecs_cost(vehicle: Vehicle,
                                       scenario: Scenario) -> None
```

Sets the motor control and power electronics cost for the vehicle.

This method calculates the marked up motor control and power electronics cost based on the vehicle powertrain type and the cost per kW.

Inputs from vehicle:
- mc_max_kw

Inputs from scenario:
- pe_mc_base_cost_dol
- pe_mc_cost_dol_per_kw

Estimated class variables:
- motor_control_power_elecs_cost_dol

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data, including the cost per kW for the motor control and power electronics.

<a id="t3co.cost_models.capital_costs.CapitalCosts.set_plug_cost"></a>

#### set\_plug\_cost

```python
def set_plug_cost(vehicle: Vehicle, scenario: Scenario) -> None
```

Sets the plug cost for the vehicle.

This method calculates the marked up plug cost based on the base cost.

Inputs from scenario:
- plug_base_cost_dol

Estimated class variables:
- plug_cost_dol

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data, including the base cost for the plug.

<a id="t3co.cost_models.capital_costs.CapitalCosts.set_battery_cost"></a>

#### set\_battery\_cost

```python
def set_battery_cost(vehicle: Vehicle, scenario: Scenario) -> None
```

Sets the battery cost for the vehicle.

This method calculates the marked up battery cost based on the energy storage system (ESS) capacity and the cost per kWh.

Inputs from vehicle:
- ess_max_kwh

Inputs from scenario:
- ess_base_cost_dol
- ess_cost_dol_per_kwh

Estimated class variables:
- battery_cost_dol

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data, including the cost per kWh for the battery.

<a id="t3co.cost_models.capital_costs.CapitalCosts.set_msrp"></a>

#### set\_msrp

```python
def set_msrp() -> None
```

Calculates the total MSRP (Manufacturer's Suggested Retail Price) for the vehicle.

This method calculates the total MSRP by summing the costs of various components of the vehicle.
The calculation uses the following CapitalCosts elements:
- glider_cost_dol
- fuel_storage_cost_dol
- fuel_converter_cost_dol
- motor_control_power_elecs_cost_dol
- battery_cost_dol
- plug_cost_dol

Estimated class variables:
- msrp_total_dol

<a id="t3co.cost_models.capital_costs.CapitalCosts.set_purchase_tax"></a>

#### set\_purchase\_tax

```python
def set_purchase_tax(scenario: Scenario) -> None
```

Sets the purchase tax for the vehicle.

This method calculates the purchase tax based on the total MSRP (Manufacturer's Suggested Retail Price) of the vehicle components.
The calculations use the following CapitalCosts elements:
- msrp_total_dol

Inputs from scenario:
- tax_rate_pct

Estimated class variables:
- purchase_tax_dol

**Arguments**:

- `scenario` _Scenario_ - The scenario instance containing configuration data, including the tax rate.

<a id="t3co.cost_models.capital_costs.CapitalCosts.set_downpayment"></a>

#### set\_downpayment

```python
def set_downpayment(scenario: Scenario) -> None
```

Sets the downpayment and initial principal for the vehicle purchase.

This method calculates the downpayment and initial principal based on the purchasing method specified in the scenario.
The calculations use the following CapitalCosts elements:
- msrp_total_dol
- purchase_tax_dol

Inputs from scenario:
- purchasing_method
- purchasing_down_payment_pct
- purchasing_interest_apr_pct_per_yr

Estimated class variables:
- purchasing_downpayment_dol
- purchasing_initial_principal_dol

**Arguments**:

- `scenario` _Scenario_ - The scenario instance containing configuration data, including the purchasing method, down payment percentage, and interest rate.

<a id="t3co.cost_models.capital_costs.CapitalCosts.set_residual_cost"></a>

#### set\_residual\_cost

```python
def set_residual_cost(scenario: Scenario) -> None
```

Sets the residual cost for the vehicle.

This method calculates the residual cost based on the total MSRP (Manufacturer's Suggested Retail Price) of the vehicle components,
the depreciation rates per year, and the vehicle's life span. The residual cost is the remaining value of the vehicle after depreciation.
The calculation uses the following CapitalCosts elements:
- msrp_total_dol

Inputs from scenario:
- depreciation_rates_pct_per_yr
- vehicle_life_yr

Estimated scenario variables:
- residual_rate_pct

Estimated class variables:
- residual_cost_dol

**Arguments**:

- `scenario` _Scenario_ - The scenario instance containing configuration data, including depreciation rates and vehicle life span.

<a id="t3co.cost_models.capital_costs.CapitalCosts.set_net_capital_cost"></a>

#### set\_net\_capital\_cost

```python
def set_net_capital_cost() -> None
```

Sets the total capital cost for the vehicle.

This method calculates the total capital cost by summing the costs of various components and applying the purchase tax.
The calculation uses the following CapitalCosts elements:
- purchasing_downpayment_dol

Inputs from scenario:
- tax_rate_pct

Estimated class variables:
- net_capital_cost_dol

<a id="t3co.cost_models.capital_costs.CapitalCosts.set_disc_residual_cost"></a>

#### set\_disc\_residual\_cost

```python
def set_disc_residual_cost(scenario: Scenario) -> None
```

Sets the discounted residual cost for the vehicle.

**Arguments**:

- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co.cost_models.capital_costs.CapitalCosts.get_marked_up_value"></a>

#### get\_marked\_up\_value

```python
def get_marked_up_value(value: float, scenario: Scenario) -> float
```

Returns the marked up value.

**Arguments**:

- `value` _float_ - The value to mark up.
- `scenario` _Scenario_ - The scenario instance containing configuration data.
  

**Returns**:

- `float` - The marked up value.

<a id="t3co.demos"></a>

# t3co.demos

<a id="t3co.demos.demo"></a>

# t3co.demos.demo

