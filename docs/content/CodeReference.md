# Table of Contents

* [.](#.)
* [..tco](#..tco)
* [..tco.tcocalc](#..tco.tcocalc)
  * [find\_residual\_rates](#..tco.tcocalc.find_residual_rates)
  * [calculate\_dollar\_cost](#..tco.tcocalc.calculate_dollar_cost)
  * [calculate\_opp\_costs](#..tco.tcocalc.calculate_opp_costs)
  * [fill\_fuel\_eff\_file](#..tco.tcocalc.fill_fuel_eff_file)
  * [fill\_veh\_expense\_file](#..tco.tcocalc.fill_veh_expense_file)
  * [fill\_trav\_exp\_tsv](#..tco.tcocalc.fill_trav_exp_tsv)
  * [fill\_downtimelabor\_cost\_tsv](#..tco.tcocalc.fill_downtimelabor_cost_tsv)
  * [fill\_market\_share\_tsv](#..tco.tcocalc.fill_market_share_tsv)
  * [fill\_fuel\_expense\_tsv](#..tco.tcocalc.fill_fuel_expense_tsv)
  * [fill\_annual\_tsv](#..tco.tcocalc.fill_annual_tsv)
  * [fill\_reg\_sales\_tsv](#..tco.tcocalc.fill_reg_sales_tsv)
  * [fill\_insurance\_tsv](#..tco.tcocalc.fill_insurance_tsv)
  * [fill\_residual\_cost\_tsc](#..tco.tcocalc.fill_residual_cost_tsc)
  * [fill\_survival\_tsv](#..tco.tcocalc.fill_survival_tsv)
  * [fill\_fuel\_split\_tsv](#..tco.tcocalc.fill_fuel_split_tsv)
* [..tco.opportunity\_cost](#..tco.opportunity_cost)
  * [OpportunityCost](#..tco.opportunity_cost.OpportunityCost)
    * [\_\_init\_\_](#..tco.opportunity_cost.OpportunityCost.__init__)
    * [set\_kdes](#..tco.opportunity_cost.OpportunityCost.set_kdes)
    * [get\_payload\_loss\_factor](#..tco.opportunity_cost.OpportunityCost.get_payload_loss_factor)
    * [get\_dwell\_time\_cost](#..tco.opportunity_cost.OpportunityCost.get_dwell_time_cost)
    * [get\_M\_R\_downtime\_cost](#..tco.opportunity_cost.OpportunityCost.get_M_R_downtime_cost)
  * [main](#..tco.opportunity_cost.main)
* [..tco.tco\_stock\_emissions](#..tco.tco_stock_emissions)
  * [dropCols](#..tco.tco_stock_emissions.dropCols)
  * [stockModel](#..tco.tco_stock_emissions.stockModel)
* [..tco.tco\_analysis](#..tco.tco_analysis)
  * [get\_operating\_costs](#..tco.tco_analysis.get_operating_costs)
  * [discounted\_costs](#..tco.tco_analysis.discounted_costs)
  * [calc\_discountedTCO](#..tco.tco_analysis.calc_discountedTCO)
  * [get\_tco\_of\_vehicle](#..tco.tco_analysis.get_tco_of_vehicle)
* [..tests.test\_tcos](#..tests.test_tcos)
  * [remove](#..tests.test_tcos.remove)
  * [RunCONVTCOTests](#..tests.test_tcos.RunCONVTCOTests)
    * [compare](#..tests.test_tcos.RunCONVTCOTests.compare)
* [..tests](#..tests)
* [..tests.tco\_tests.t2co\_tco\_benchmark](#..tests.tco_tests.t2co_tco_benchmark)
  * [veh\_no](#..tests.tco_tests.t2co_tco_benchmark.veh_no)
* [..tests.tco\_tests.t2co\_bev\_mpgge\_benchmark](#..tests.tco_tests.t2co_bev_mpgge_benchmark)
  * [veh\_no](#..tests.tco_tests.t2co_bev_mpgge_benchmark.veh_no)
* [..tests.test\_moo](#..tests.test_moo)
* [..moopack](#..moopack)
* [..moopack.moo](#..moopack.moo)
  * [T3COProblem](#..moopack.moo.T3COProblem)
    * [setup\_opt\_records](#..moopack.moo.T3COProblem.setup_opt_records)
    * [\_\_init\_\_](#..moopack.moo.T3COProblem.__init__)
    * [compile\_reporting\_vars](#..moopack.moo.T3COProblem.compile_reporting_vars)
    * [instantiate\_moo\_vehicles\_and\_scenario](#..moopack.moo.T3COProblem.instantiate_moo_vehicles_and_scenario)
    * [cda\_percent\_delta\_knob](#..moopack.moo.T3COProblem.cda_percent_delta_knob)
    * [weight\_delta\_percent\_knob](#..moopack.moo.T3COProblem.weight_delta_percent_knob)
    * [fc\_peak\_eff\_knob](#..moopack.moo.T3COProblem.fc_peak_eff_knob)
    * [get\_objs](#..moopack.moo.T3COProblem.get_objs)
    * [adjust\_fc\_peak\_eff](#..moopack.moo.T3COProblem.adjust_fc_peak_eff)
    * [sweep\_knob](#..moopack.moo.T3COProblem.sweep_knob)
    * [get\_tco\_from\_moo\_advanced\_result](#..moopack.moo.T3COProblem.get_tco_from_moo_advanced_result)
  * [T3CODisplay](#..moopack.moo.T3CODisplay)
    * [\_\_init\_\_](#..moopack.moo.T3CODisplay.__init__)
  * [run\_optimization](#..moopack.moo.run_optimization)
* [..objectives.accel](#..objectives.accel)
  * [get\_accel](#..objectives.accel.get_accel)
* [..objectives.fueleconomy](#..objectives.fueleconomy)
  * [get\_range\_mi](#..objectives.fueleconomy.get_range_mi)
  * [get\_sim\_drive](#..objectives.fueleconomy.get_sim_drive)
  * [get\_mpgge](#..objectives.fueleconomy.get_mpgge)
* [..objectives.gradeability](#..objectives.gradeability)
  * [get\_gradeability](#..objectives.gradeability.get_gradeability)
* [..objectives](#..objectives)
* [..sweep](#..sweep)
  * [save\_tco\_files](#..sweep.save_tco_files)
  * [get\_knobs\_bounds\_curves](#..sweep.get_knobs_bounds_curves)
  * [get\_objectives\_constraints](#..sweep.get_objectives_constraints)
  * [run\_moo](#..sweep.run_moo)
  * [check\_input\_files](#..sweep.check_input_files)
  * [run\_vehicle\_scenarios](#..sweep.run_vehicle_scenarios)
* [..run.Global](#..run.Global)
  * [DieselGalPerGasGal](#..run.Global.DieselGalPerGasGal)
  * [kgH2\_per\_gge](#..run.Global.kgH2_per_gge)
  * [mps\_to\_mph](#..run.Global.mps_to_mph)
  * [m\_to\_mi](#..run.Global.m_to_mi)
  * [get\_kwh\_per\_gge](#..run.Global.get_kwh_per_gge)
  * [set\_tco\_intermediates](#..run.Global.set_tco_intermediates)
  * [set\_tco\_results](#..run.Global.set_tco_results)
  * [kg\_to\_lbs](#..run.Global.kg_to_lbs)
  * [lbs\_to\_kgs](#..run.Global.lbs_to_kgs)
  * [not\_falsy](#..run.Global.not_falsy)
* [..run](#..run)
* [..run.generateinputs](#..run.generateinputs)
  * [generate](#..run.generateinputs.generate)
* [..run.run\_scenario](#..run.run_scenario)
  * [set\_test\_weight](#..run.run_scenario.set_test_weight)
  * [reset\_vehicle\_weight](#..run.run_scenario.reset_vehicle_weight)
  * [limit\_cargo\_kg\_for\_moo\_hev\_bev](#..run.run_scenario.limit_cargo_kg_for_moo_hev_bev)
  * [set\_max\_motor\_kw](#..run.run_scenario.set_max_motor_kw)
  * [set\_max\_battery\_kwh](#..run.run_scenario.set_max_battery_kwh)
  * [set\_max\_battery\_power\_kw](#..run.run_scenario.set_max_battery_power_kw)
  * [set\_max\_fuel\_converter\_kw](#..run.run_scenario.set_max_fuel_converter_kw)
  * [set\_fuel\_store\_kwh](#..run.run_scenario.set_fuel_store_kwh)
  * [set\_cargo\_kg](#..run.run_scenario.set_cargo_kg)
  * [Config](#..run.run_scenario.Config)
    * [from\_file](#..run.run_scenario.Config.from_file)
    * [from\_dict](#..run.run_scenario.Config.from_dict)
    * [validate\_analysis\_id](#..run.run_scenario.Config.validate_analysis_id)
  * [Scenario](#..run.run_scenario.Scenario)
    * [originalcargo\_kg](#..run.run_scenario.Scenario.originalcargo_kg)
    * [plf\_scenario\_vehicle\_cargo\_capacity\_kg](#..run.run_scenario.Scenario.plf_scenario_vehicle_cargo_capacity_kg)
    * [from\_config](#..run.run_scenario.Scenario.from_config)
  * [check\_phev\_init\_socs](#..run.run_scenario.check_phev_init_socs)
  * [get\_phev\_util\_factor](#..run.run_scenario.get_phev_util_factor)
  * [get\_objective\_simdrive](#..run.run_scenario.get_objective_simdrive)
  * [run\_grade\_or\_accel](#..run.run_scenario.run_grade_or_accel)
  * [create\_fastsim\_vehicle](#..run.run_scenario.create_fastsim_vehicle)
  * [get\_vehicle](#..run.run_scenario.get_vehicle)
  * [get\_scenario\_and\_cycle](#..run.run_scenario.get_scenario_and_cycle)
  * [load\_scenario](#..run.run_scenario.load_scenario)
  * [load\_design\_cycle\_from\_scenario](#..run.run_scenario.load_design_cycle_from_scenario)
  * [load\_design\_cycle\_from\_path](#..run.run_scenario.load_design_cycle_from_path)
  * [vehicle\_scenario\_sweep](#..run.run_scenario.vehicle_scenario_sweep)
  * [run](#..run.run_scenario.run)
  * [rerun](#..run.run_scenario.rerun)
* [..demos.opp\_cost\_demo](#..demos.opp_cost_demo)
* [..demos.hev\_sweep\_and\_moo](#..demos.hev_sweep_and_moo)
  * [vnum](#..demos.hev_sweep_and_moo.vnum)
* [..demos.example\_load\_and\_run](#..demos.example_load_and_run)
* [..demos.t2co\_opt\_benchmark](#..demos.t2co_opt_benchmark)
* [..demos.Spencer](#..demos.Spencer)

<a id="."></a>

# .

<a id="..tco"></a>

# ..tco

<a id="..tco.tcocalc"></a>

# ..tco.tcocalc

<a id="..tco.tcocalc.find_residual_rates"></a>

#### find\_residual\_rates

```python
def find_residual_rates(vehicle, scenario)
```

This helper method gets the residual rates from ResidualValues.csv

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
  

**Returns**:

- `residual_rates` _float_ - Residual rate as percentage of MSRP

<a id="..tco.tcocalc.calculate_dollar_cost"></a>

#### calculate\_dollar\_cost

```python
def calculate_dollar_cost(veh, scenario)
```

This helper method calculates the MSRP breakdown dictionary from
-   Glider
-   Fuel converter
-   Fuel Storage
-   Motor & power electronics
-   Plug
-   Battery
-   Battery replacement
-   Purchase tax

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
  

**Returns**:

- `cost_set` _dict_ - Dictionary containing MSRP breakdown

<a id="..tco.tcocalc.calculate_opp_costs"></a>

#### calculate\_opp\_costs

```python
def calculate_opp_costs(vehicle, scenario, range_dict)
```

This helper method calculates opportunity costs and generates veh_opp_cost_set from
-   Payload Lost Capacity Cost/Multiplier
-   Fueling Downtime
-   Maintenance and Repair Downtime

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `range_dict` _dict_ - Dictionary containing range values from fueleconomy.get_range_mi()

<a id="..tco.tcocalc.fill_fuel_eff_file"></a>

#### fill\_fuel\_eff\_file

```python
def fill_fuel_eff_file(vehicle, scenario, mpgge_dict)
```

This helper method generates a dataframe of Fuel Efficiency [mi/gge]
For PHEV, cd_grid_electric_mpgge, cd_fuel_mpgge, and cs_fuel_mpgge
For BEV, grid_mpgge
For HEV and CONV, mpgge

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `mpgge_dict` _dict_ - MPGGE dictionary from fueleconomy.get_mpgge()
  

**Returns**:

- `fefdata` _pd.DataFrame_ - Dictionary containing Fuel Efficiency [mi/gge]

<a id="..tco.tcocalc.fill_veh_expense_file"></a>

#### fill\_veh\_expense\_file

```python
def fill_veh_expense_file(scenario, cost_set)
```

This helper method generates a dataframe of MSRP breakdown costs as Cost [$/veh]

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `cost_set` _dict_ - Dictionary containing MSRP breakdown cost components
  

**Returns**:

- `vexpdf` _pd.DataFrame_ - Dataframe containing MSRP components costs as Cost [$/veh]

<a id="..tco.tcocalc.fill_trav_exp_tsv"></a>

#### fill\_trav\_exp\_tsv

```python
def fill_trav_exp_tsv(vehicle, scenario)
```

This helper method generates a dataframe containing maintenance costs in Cost [$/mi]

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing maintenance costs in Cost [$/mi]

<a id="..tco.tcocalc.fill_downtimelabor_cost_tsv"></a>

#### fill\_downtimelabor\_cost\_tsv

```python
def fill_downtimelabor_cost_tsv(scenario, oppy_cost_set)
```

This helper method generates a dataframe containing fueling downtime and M&R downtime costs in Cost [$/Yr]

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `oppy_cost_set` _dict_ - Dictionary containing dwell_time_cost_Dol and MR_downtime_cost_Dol
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing fueling and MR downtime costs in Cost [$/Yr]

<a id="..tco.tcocalc.fill_market_share_tsv"></a>

#### fill\_market\_share\_tsv

```python
def fill_market_share_tsv(scenario, num_vs=1)
```

This helper method generates a dataframe containing market share of current vehicle selection per vehicle sold

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `num_vs` _int, optional_ - Number of vehicles. Defaults to 1.
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing market share of current vehicle in Market Share [veh/veh]

<a id="..tco.tcocalc.fill_fuel_expense_tsv"></a>

#### fill\_fuel\_expense\_tsv

```python
def fill_fuel_expense_tsv(vehicle, scenario)
```

This helper method generates a dataframe of fuel operating costs in Cost [$/gge]

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
  

**Raises**:

- `Exception` - Invalid fuel type
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing fuel operating costs in Cost [$/gge]

<a id="..tco.tcocalc.fill_annual_tsv"></a>

#### fill\_annual\_tsv

```python
def fill_annual_tsv(scenario)
```

This helper method generates a dataframe of annual vehicle miles traveled (vmt) - Annual Travel [mi/yr]

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing Annual Travel [mi/yr]

<a id="..tco.tcocalc.fill_reg_sales_tsv"></a>

#### fill\_reg\_sales\_tsv

```python
def fill_reg_sales_tsv(scenario, num_vs=1)
```

This helper method generates a dataframe containing vehicle sales per year - Sales [veh]

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `num_vs` _int, optional_ - Number of vehicles. Defaults to 1.
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing vehicle sales in Sales [veh]

<a id="..tco.tcocalc.fill_insurance_tsv"></a>

#### fill\_insurance\_tsv

```python
def fill_insurance_tsv(scenario, veh_cost_set)
```

This helper method generates a dataframe containing vehicle insurance costs as Cost [$/Yr]

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `veh_cost_set` _dict_ - Dictionary containing MSRP costs
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing insurance costs in Cost [$/Yr]

<a id="..tco.tcocalc.fill_residual_cost_tsc"></a>

#### fill\_residual\_cost\_tsc

```python
def fill_residual_cost_tsc(vehicle, scenario, veh_cost_set)
```

This helper method generates a dataframe of residual costs as Cost [$/Yr]

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `veh_cost_set` _dict_ - Dictionary containing MSRP costs
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing vehicle residual costs as Cost [$/Yr]

<a id="..tco.tcocalc.fill_survival_tsv"></a>

#### fill\_survival\_tsv

```python
def fill_survival_tsv(scenario, num_vs=1)
```

This helper method generates a dataframe containing surviving vehicles as Surviving Vehicles [veh/veh]

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `num_vs` _int, optional_ - Number of vehicles. Defaults to 1.
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing number of surviving vehicles on road in Surviving Vehicles [veh/veh]

<a id="..tco.tcocalc.fill_fuel_split_tsv"></a>

#### fill\_fuel\_split\_tsv

```python
def fill_fuel_split_tsv(vehicle, scenario, mpgge)
```

This helper method generates a dataframe of fraction of travel in each fuel type as Fraction of Travel [mi/mi]

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `mpgge` _dict_ - MPGGE dictionary from fueleconomy.get_mpgge()
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing fraction of travel in each fuel type as Fraction of Travel [mi/mi]

<a id="..tco.opportunity_cost"></a>

# ..tco.opportunity\_cost

<a id="..tco.opportunity_cost.OpportunityCost"></a>

## OpportunityCost Objects

```python
class OpportunityCost()
```

This class is used to calculate the different opportunity costs for a scenario and vehicle
- Payload Capacity Cost Multiplier
- Fueling Downtime Cost
- Maintenance and Repair Downtime Cost

<a id="..tco.opportunity_cost.OpportunityCost.__init__"></a>

#### \_\_init\_\_

```python
def __init__(scenario, range_dict=None, **kwargs)
```

Initializes OpportunityCost object using Scenario object, range_dict (from fueleconomy module), and other arguments

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object
- `range_dict` _dict, optional_ - dictionary containing primary_fuel_range_mi from fueleconomy.get_range_mi function. Defaults to None.

<a id="..tco.opportunity_cost.OpportunityCost.set_kdes"></a>

#### set\_kdes

```python
def set_kdes(scenario, bw_method=0.15, verbose=False)
```

This method sets tje kde kernel. This is time-consuming, only call this once, if possible.

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object
- `bw_method` _float, optional_ - kernel bandwidth method used by guassian_kde. Defaults to .15.
- `verbose` _bool, optional_ - if True, prints process sets. Defaults to False.

<a id="..tco.opportunity_cost.OpportunityCost.get_payload_loss_factor"></a>

#### get\_payload\_loss\_factor

```python
def get_payload_loss_factor(a_vehicle: fastsim.vehicle,
                            scenario,
                            plots=False,
                            plots_dir=None)
```

This method runs teh kernel density estimation function set_kdes and calculates the payload capacity loss factor (payload_cap_cost_multiplier)             of the new vehicle compared to a conventional vehicle's reference empty weight.

**Arguments**:

- `a_vehicle` _fastsim.vehicle_ - FASTSim vehicle object of the analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `plots` _bool, optional_ - if True, creates histogram of KDE weight bins. Defaults to False.
- `plots_dir` _str, optional_ - output diretory for saving plot figure. Defaults to None.

<a id="..tco.opportunity_cost.OpportunityCost.get_dwell_time_cost"></a>

#### get\_dwell\_time\_cost

```python
def get_dwell_time_cost(a_vehicle: fastsim.vehicle, scenario)
```

This function calculates the fueling dwell time cost for a vehicle based on fuel fill rate/charging power and shifts_per_year

**Arguments**:

- `a_vehicle` _fastsim.vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object for current selection

<a id="..tco.opportunity_cost.OpportunityCost.get_M_R_downtime_cost"></a>

#### get\_M\_R\_downtime\_cost

```python
def get_M_R_downtime_cost(a_vehicle: fastsim.vehicle, scenario)
```

This function calculates the Maintenance and Repair (M&R) downtime cost based on planned, unplanned, and tire replacement downtime inputs

**Arguments**:

- `a_vehicle` _fastsim.vehicle_ - FASTSim object of the analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object for the current selection

<a id="..tco.opportunity_cost.main"></a>

#### main

```python
def main()
```

Runs the opportunity cost module as a standalone code based on input vehicles and scenarios

<a id="..tco.tco_stock_emissions"></a>

# ..tco.tco\_stock\_emissions

<a id="..tco.tco_stock_emissions.dropCols"></a>

#### dropCols

```python
def dropCols(df)
```

This helper method drops columns if any row contains ['*']

**Arguments**:

- `df` _pd.DataFrame_ - Input dataframe
  

**Returns**:

- `df` _pd.DataFrame_ - Output dataframe with dropped dummy columns

<a id="..tco.tco_stock_emissions.stockModel"></a>

#### stockModel

```python
def stockModel(sales,
               marketShares,
               survival,
               annualTravel,
               fuelSplit,
               fuelEfficiency,
               emissions,
               vehicleCosts=None,
               travelCosts=None,
               fuelCosts=None,
               insuranceCosts=None,
               residualCosts=None,
               downtimeCosts=None,
               write_files=False)
```

This function generates the ownershipCosts dataframe from the dataframes for each cost category

**Arguments**:

- `sales` _pd.DataFrame_ - Dataframe of yearly number of vehicles sales
- `marketShares` _pd.DataFrame_ - Dataframe of yearly Market Share of selection's vocation per vehicle [veh/veh]
- `survival` _pd.DataFrame_ - Dataframe of yearly Surviving vehicle per each vehicle [veh/veh]
- `annualTravel` _pd.DataFrame_ - Dataframe of vehicle's vmt: Annual Travel [mi/yr]
- `fuelSplit` _pd.DataFrame_ - Dataframe of fraction of travel using each fuel [mi/mi]
- `fuelEfficiency` _pd.DataFrame_ - Dataframe of vehicle's yearly average fuel efficiency [mi/gge]
- `emissions` _pd.DataFrame_ - Dataframe of vehicle's yearly average emissions
- `vehicleCosts` _pd.DataFrame, optional_ - Dataframe of vehicle components costs [Dol]. Defaults to None.
- `travelCosts` _pd.DataFrame, optional_ - Dataframe of maintenance costs [Dol/mi]. Defaults to None.
- `fuelCosts` _pd.DataFrame, optional_ - Dataframe of fuel operating costs [Dol/gge]. Defaults to None.
- `insuranceCosts` _pd.DataFrame, optional_ - Dataframe of yearly insurance costs [Dol]. Defaults to None.
- `residualCosts` _pd.DataFrame, optional_ - Dataframe of yearly residual costs [Dol]. Defaults to None.
- `downtimeCosts` _pd.DataFrame, optional_ - Dataframe of yearly downtime costs [Dol]. Defaults to None.
- `write_files` _bool, optional_ - if True, save vehicleCosts, travelCosts, fuelCosts, insuranceCosts,residualCosts, downtimeCosts . Defaults to False.
  

**Returns**:

- `stock` _pd.DataFrame_ - Dataframe of stock model of vehicles in the market
- `emissions` _pd.DataFrame_ - Dataframe of total emissions
- `ownershipCosts` _pd.DataFrame_ - Dataframe of all ownership costs for given selection

<a id="..tco.tco_analysis"></a>

# ..tco.tco\_analysis

<a id="..tco.tco_analysis.get_operating_costs"></a>

#### get\_operating\_costs

```python
def get_operating_costs(ownershipCosts, TCO_switch="DIRECT")
```

This function creates a dataframe of operating cost from ownershipCosts dataframe based on TCO_switch ('DIRECT' or 'EFFICIENCY')

**Arguments**:

- `ownershipCosts` _pd.DataFrame_ - Dataframe containing year-wise ownership costs estimations like Fuel, maintenance, insurance, etc
- `TCO_switch` _str, optional_ - Switch between different TCO calculations - 'DIRECT' or 'EFFICIENCY'. Defaults to 'DIRECT'.
  

**Returns**:

- `operatingCosts_df` _pd.DataFrame_ - Dataframe containing operating cost categories based on TCO_switch

<a id="..tco.tco_analysis.discounted_costs"></a>

#### discounted\_costs

```python
def discounted_costs(scenario, ownershipCosts)
```

This function calculates the yearly discounted costs for each category of ownershipCosts based on scenario.discount_rate_pct_per_yr

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object for current selection
- `ownershipCosts` _pd.DataFrame_ - Dataframe containing year-wise ownership costs estimations like Fuel, maintenance, insurance, etc
  

**Returns**:

- `ownershipCosts` _pd.DataFrame_ - ownershipCosts dataframe with additional 'Discounted Cost [$]' column

<a id="..tco.tco_analysis.calc_discountedTCO"></a>

#### calc\_discountedTCO

```python
def calc_discountedTCO(scenario,
                       discounted_costs_df,
                       veh_cost_set,
                       veh_opp_cost_set,
                       sim_drive,
                       TCO_switch="DIRECT")
```

This function calculates the discounted Total Cost of Ownerhip (discounted to account for time-value of money).
There are two methods to calculate discounted TCO - 'DIRECT' and 'EFFICIENCY'

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object for current selection
- `discounted_costs_df` _pd.DataFrame_ - discounted operating costs dataframe
- `veh_cost_set` _dict_ - Dictionary containing MSRP breakdown
- `veh_opp_cost_set` _dict_ - Dictionary containing opportunity costs breakdown
- `sim_drive` _fastsim.simdrive.SimDrive_ - FASTSim.simdrive.SimDrive object containing inputs and outputs from vehicle simulation over a cycle
- `TCO_switch` _str, optional_ - Switch between different TCO calculations - 'DIRECT' or 'EFFICIENCY'. Defaults to 'DIRECT'.
  

**Returns**:

- `discountedTCO` _float_ - Discounted Total Cost of Ownership value
- `oppy_cost_Dol_set` _dict_ - Dictionary containing discounted opportunity costs breakdown
- `veh_oper_cost_set` _dict_ - Dictionary containing discounted operating costs breakdown

<a id="..tco.tco_analysis.get_tco_of_vehicle"></a>

#### get\_tco\_of\_vehicle

```python
def get_tco_of_vehicle(vehicle, range_cyc, scenario, write_tsv=False)
```

This function calculates the Total Cost of Ownership of a vehicle and scenario for a given cycle. The three main components are:
- Opportunity Costs
- MSRP
- Operating Costs

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of selected vehicle
- `range_cyc` _fastsim.cycle.Cycle_ - FASTSim range cycle object
- `scenario` _run_scenario.Scenario_ - Scenario object for current selection
- `write_tsv` _bool, optional_ - if True, save intermediate files as TSV. Defaults to False.
  

**Returns**:

- `tot_cost_Dol` _float_ - TCO in dollars
- `discounted_TCO_Dol` _float_ - discounted TCO in dollars
- `oppy_cost_set` _dict_ - Dictionary of opportunity cost breakdown
- `ownership_costs_df` _pd.DataFrame_ - Ownerhip Costs dataframe containing different categories per year
- `discounted_costs_df` _pd.DataFrame_ - discounted Ownerhip Costs dataframe containing different categories per year
- `mpgge` _dict_ - Dictionary containing MPGGEs
- `veh_cost_set` _dict_ - Dictionary containing MSRP breakdown
- `design_cycle_sdr` _fastsim.simdrive.SimDrive_ - FASTSim SimDrive object for design drivecycle
- `veh_oper_cost_set` _dict_ - Dictionary containing operating costs breakdown
- `veh_opp_cost_set` _dict_ - Dictionary containing opportunity costs breakdown
- `tco_files` _dict_ - Dictionary containing TCO intermediate dataframes

<a id="..tests.test_tcos"></a>

# ..tests.test\_tcos

Testing module for TCO to ensure the TCO related results remain consistent over time

Flow:
code reads TCO tests vehicles and scenarios one at a time. Generates TCO output dictionaries
and compares the results with the hard coded dictionaries below in comparison_dict.

<a id="..tests.test_tcos.remove"></a>

#### remove

```python
def remove(out)
```

removes key-values from output dict that can't be compared very easily

<a id="..tests.test_tcos.RunCONVTCOTests"></a>

## RunCONVTCOTests Objects

```python
class RunCONVTCOTests(unittest.TestCase)
```

<a id="..tests.test_tcos.RunCONVTCOTests.compare"></a>

#### compare

```python
def compare(runresults, staticresults)
```

Check all key-value pairs between dicts for equality

**Arguments**:

- `runresults`: dict of results from generated vehicle results
- `staticresults`: dict of results from static comparison dict

**Returns**:

None

<a id="..tests"></a>

# ..tests

Package for testing modules compliant with unittest folder structure.

<a id="..tests.tco_tests.t2co_tco_benchmark"></a>

# ..tests.tco\_tests.t2co\_tco\_benchmark

Testing module for TCO to ensure the TCO related results remain consistent over time with
previous model (Tech Targets c 2019)

Flow:
code reads TCO tests vehicles and scenarios one at a time. Generates TCO output dictionaries
and compares the results with the hard coded dictionaries below in comparison_dict.

<a id="..tests.tco_tests.t2co_tco_benchmark.veh_no"></a>

#### veh\_no



<a id="..tests.tco_tests.t2co_bev_mpgge_benchmark"></a>

# ..tests.tco\_tests.t2co\_bev\_mpgge\_benchmark

Testing module for TCO to ensure the TCO related results remain consistent over time with
previous model (Tech Targets c 2019)

Flow:
code reads TCO tests vehicles and scenarios one at a time. Generates TCO output dictionaries
and compares the results with the hard coded dictionaries below in comparison_dict.

<a id="..tests.tco_tests.t2co_bev_mpgge_benchmark.veh_no"></a>

#### veh\_no



<a id="..tests.test_moo"></a>

# ..tests.test\_moo

Module for testing moo.  Folder structure, file name, and code 
are written to be compliant with python's unittest package, but 
main() can be called via importing

<a id="..moopack"></a>

# ..moopack

Sub-package contaning module that runs PyMOO optimization

<a id="..moopack.moo"></a>

# ..moopack.moo

<a id="..moopack.moo.T3COProblem"></a>

## T3COProblem Objects

```python
class T3COProblem(ElementwiseProblem)
```

Class for creating PyMoo problem.

<a id="..moopack.moo.T3COProblem.setup_opt_records"></a>

#### setup\_opt\_records

```python
def setup_opt_records()
```

This method sets up the empty optimization record arrays

<a id="..moopack.moo.T3COProblem.__init__"></a>

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

<a id="..moopack.moo.T3COProblem.compile_reporting_vars"></a>

#### compile\_reporting\_vars

```python
def compile_reporting_vars()
```

This method creates an output dictionary containing optimization results

<a id="..moopack.moo.T3COProblem.instantiate_moo_vehicles_and_scenario"></a>

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

<a id="..moopack.moo.T3COProblem.cda_percent_delta_knob"></a>

#### cda\_percent\_delta\_knob

```python
def cda_percent_delta_knob(CdA_perc_reduction, optvehicle)
```

This method sets the drag_coef based on aero improvement curve and glider_kg based on cda_cost_coeff_a and cda_cost_coeff_b

**Arguments**:

- `CdA_perc_reduction` _str_ - Name of aero improvement curve file
- `optvehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for optimization vehicle

<a id="..moopack.moo.T3COProblem.weight_delta_percent_knob"></a>

#### weight\_delta\_percent\_knob

```python
def weight_delta_percent_knob(wt_perc_reduction, optvehicle)
```

This method sets the knob from the lightweighting curve

**Arguments**:

- `wt_perc_reduction` _float_ - Weight reduction percentage value from lightweighting curve
- `optvehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of the optimization vehicle

<a id="..moopack.moo.T3COProblem.fc_peak_eff_knob"></a>

#### fc\_peak\_eff\_knob

```python
def fc_peak_eff_knob(fc_peak_eff, optvehicle)
```

This method sets the knob from the engine efficiency curve

**Arguments**:

- `fc_peak_eff` _float_ - Fuel converter peak effiency override from engine efficiency improvement curve
- `optvehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for optimization vehicle

<a id="..moopack.moo.T3COProblem.get_objs"></a>

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

<a id="..moopack.moo.T3COProblem.adjust_fc_peak_eff"></a>

#### adjust\_fc\_peak\_eff

```python
def adjust_fc_peak_eff(fc_peak_eff, scenario, optvehicle)
```

This method augments an advanced vehicle fc_eff_array based on new fc_peak_eff using baseline fc_eff_array


**Arguments**:

- `fc_peak_eff` _float_ - Fuel converter peak efficiency override
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `optvehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of optimization vehicle

<a id="..moopack.moo.T3COProblem.sweep_knob"></a>

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

<a id="..moopack.moo.T3COProblem.get_tco_from_moo_advanced_result"></a>

#### get\_tco\_from\_moo\_advanced\_result

```python
def get_tco_from_moo_advanced_result(x)
```

This method is a utility function to get detailed TCO information from optimized MOO result

**Arguments**:

- `x` _dict_ - Dictionary containing optimization knobs - [max motor kw, battery kwh, drag coeff % improvement]
  

**Returns**:

- `out` _dict_ - Dictionary containing TCO results for optimization runs

<a id="..moopack.moo.T3CODisplay"></a>

## T3CODisplay Objects

```python
class T3CODisplay(Output)
```

This class contains the display object for Pymoo optimization printouts - pymoo.util.display.Display

**Arguments**:

- `Output` _pymoo.util.display.output.Output_ - Pymoo minimize display object

<a id="..moopack.moo.T3CODisplay.__init__"></a>

#### \_\_init\_\_

```python
def __init__(**kwargs)
```

This constructor initializes the pymoo.util.display.Display object

<a id="..moopack.moo.run_optimization"></a>

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

<a id="..objectives.accel"></a>

# ..objectives.accel

Module for simulating acceleration performance.

<a id="..objectives.accel.get_accel"></a>

#### get\_accel

```python
def get_accel(analysis_vehicle,
              scenario=None,
              set_weight_to_max_kg=True,
              verbose=False,
              ess_init_soc=None)
```

This function runs a simdrive for getting 0-to-60 and 0-30 mph time with fully laden weight at GVWR (plus gvwr_credit_kg?)


**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for analysis vehicle
- `scenario` _run_scenario.Scenario, optional_ - Scenario object for current selection. Defaults to None.
- `set_weight_to_max_kg` _bool, optional_ - if True, runs run_scenario.set_test_weight(). Defaults to True.
- `verbose` _bool, optional_ - if True, prints the process steps. Defaults to False.
- `ess_init_soc` _float, optional_ - ESS initial SOC override. Defaults to None.
  

**Returns**:

- `zero_to_sixty` _float_ - 0-60 mph acceleration time in sec
- `zero_to_thirty` _float_ - 0-30 mph acceleration time in sec
- `accel_simdrive` _fastsim.simdrive.SimDrive_ - FASTSim.simdrive.SimDrive object for running the acceleration drivecycle

<a id="..objectives.fueleconomy"></a>

# ..objectives.fueleconomy

Module containing functions for calculating fuel economy objectives.

<a id="..objectives.fueleconomy.get_range_mi"></a>

#### get\_range\_mi

```python
def get_range_mi(mpgge_info: dict, vehicle: fastsim.vehicle.Vehicle,
                 scenario) -> dict
```

This funcion computes range [miles] from mpgge using vehicle powertrain type and energy (or fuel) store size.

Considerations:
- at some point each vehicle powertrain type could employ the concept
of a "first fuel" or "primary fuel" - so return a primary fuel-based range for all
powertrains.
- PHEVs have two fuels (generally diesel and electricity). So return two ranges:
-- One for determining range during optimization
i.e. the CD range that PHEVs are commonly specified with
(e.g. PHEV-50 = PHEV with 50 mi AER "All-Electric Range" ~= CD range)
-- One that represents the "true" total PHEV range (CD + CS using both ESS and FS)

**Arguments**:

- `mpgge_info` _dict_ - Dictionary containing MPGGE breakdown
- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
  

**Returns**:

- `range_dict` _dict_ - Dictionary containing different range results

<a id="..objectives.fueleconomy.get_sim_drive"></a>

#### get\_sim\_drive

```python
def get_sim_drive(erc, v, scenario)
```

This helper method returns a FASTSim SimDrive object using the vehicle, drive cycle and scenario

**Arguments**:

- `erc` _fastsim.cycle.Cycle| List[Tuple[fastsim.cycle.Cycle, float_ - FASTSim range cycle object or list of tuples of cycles
- `v` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object for current selection
  

**Returns**:

- `sim_drive` _fastsim.simdrive.SimDrive_ - FASTSim SimDrive object

<a id="..objectives.fueleconomy.get_mpgge"></a>

#### get\_mpgge

```python
def get_mpgge(eff_range_cyc: fastsim.cycle.Cycle
              | List[Tuple[fastsim.cycle.Cycle, float]],
              v: fastsim.vehicle.Vehicle,
              scenario,
              diagnostic=False)
```

This helper method gets the composite mpgge fuel efficiency of vehicle for each efficiency_range Drive Cycle and weight.
It runs the vehicle using efficiency range cycle(s) and returns mpgge based on the powertrain type

Method computes a composite mpgge from multiple drive cycles and weights for each cycle.
If the user passes in a single Drive Cycle rather than a list of tuples, the base case of
a composite mpgge from a single Drive Cycle and a single weight, 1, is computed.

Also updates the vehicle's corresponding scenario object

**Arguments**:

- `eff_range_cyc` _fastsim.cycle.Cycle | List[Tuple[fastsim.cycle.Cycle, float]]_ - efficiency range cycle
- `v` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object for current selection
- `diagnostic` _bool, optional_ - if True, returns all mpgge dicts. Defaults to False.
  

**Raises**:

- `ValueError` - unknown vehicle powertrain type
  

**Returns**:

- `mpgge_comp` _dict_ - Dictionary containing MPGGE breakdowns
- `sim_drives` _List[fastsim.simdrive.SimDrive]_ - List of simdrives for charge depleting and charge sustaining cycles
- `mpgges` _List[dict], optional_ - if diagnostic==True, returns additional

<a id="..objectives.gradeability"></a>

# ..objectives.gradeability

<a id="..objectives.gradeability.get_gradeability"></a>

#### get\_gradeability

```python
def get_gradeability(analysis_vehicle,
                     scenario=None,
                     verbose=False,
                     ess_init_soc=None,
                     set_weight_to_max_kg=True)
```

This function runs SimDrives to determine the gradeability at given speed and the grade vehicle is
evaluated at how much it meets or exceeds target speed at the target grade.

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for analysis vehicle
- `scenario` _run_scenario.Scenario, optional_ - Scenario object for current selection. Defaults to None.
- `verbose` _bool, optional_ - if True, prints process steps. Defaults to False.
- `ess_init_soc` _float, optional_ - ESS Initial SOC override. Defaults to None.
- `set_weight_to_max_kg` _bool, optional_ - if True, run_scenario.set_test_weight() overrides vehice weight to GVWR. Defaults to True.
  

**Returns**:

- `grade_6percent_mph_ach` _float_ - Achieved speed on 6% grade test
- `grade_1pt25percent_mph_ach` _float_ - Achieved speed on 1.25% grade test
- `grade_6_simdrive` _fastsim.simdrive.SimDrive_ - FASTSim SimDrive for gradeability test of 6% grade
- `grade_125_simdrive` _fastsim.simdrive.SimDrive_ - FASTSim SimDrive for gradeability test of 1.25% grade

<a id="..objectives"></a>

# ..objectives

Sub-package contaning modules that calculate optimization objectives.

<a id="..sweep"></a>

# ..sweep

<a id="..sweep.save_tco_files"></a>

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

<a id="..sweep.get_knobs_bounds_curves"></a>

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

<a id="..sweep.get_objectives_constraints"></a>

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

<a id="..sweep.run_moo"></a>

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

<a id="..sweep.check_input_files"></a>

#### check\_input\_files

```python
def check_input_files(df, filetype, filepath)
```

This function contains assert statements that make sure input vehicle and scenario dataframes do not contain numm rows

**Arguments**:

- `df` _DataFrame_ - vehicle or scenario dataframe
- `filetype` _str_ - 'vehicle' or 'scenario'
- `filepath` _str_ - filepath of the vehicle or scenario input files

<a id="..sweep.run_vehicle_scenarios"></a>

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

<a id="..run.Global"></a>

# ..run.Global

Global constants
Stores paths to directories used for input files, as well as constants referenced throughout the code base

<a id="..run.Global.DieselGalPerGasGal"></a>

#### DieselGalPerGasGal

energy equivalent gallons of diesel per 1 gallon gas

<a id="..run.Global.kgH2_per_gge"></a>

#### kgH2\_per\_gge

https://epact.energy.gov/fuel-conversion-factors for Hydrogen

<a id="..run.Global.mps_to_mph"></a>

#### mps\_to\_mph

1 mps = 2.23694 mph

<a id="..run.Global.m_to_mi"></a>

#### m\_to\_mi

1 m = 0.000621371 mi

<a id="..run.Global.get_kwh_per_gge"></a>

#### get\_kwh\_per\_gge

```python
def get_kwh_per_gge()
```

This is a getter for kwh_per_gge, sim and scenario dependant var that can change
important to get from one location each time so we can track when and how it's used

**Returns**:

- `kwh_per_gge` _float_ - kWh per Gasoline Gallon Equivalent

<a id="..run.Global.set_tco_intermediates"></a>

#### set\_tco\_intermediates

```python
def set_tco_intermediates()
```

This function sets path for TCO_INTERMEDIATES to save tsv files

<a id="..run.Global.set_tco_results"></a>

#### set\_tco\_results

```python
def set_tco_results()
```

This function sets path for TCO_RESULTS

<a id="..run.Global.kg_to_lbs"></a>

#### kg\_to\_lbs

```python
def kg_to_lbs(kgs)
```

This function converts kg to lb

**Arguments**:

- `kgs` _float_ - mass in kg
  

**Returns**:

- `(float)` - mass in pounds

<a id="..run.Global.lbs_to_kgs"></a>

#### lbs\_to\_kgs

```python
def lbs_to_kgs(lbs)
```

This function converts lb to kg

**Arguments**:

- `lbs` _float_ - mass in pounds
  

**Returns**:

- `(float)` - mass in kg

<a id="..run.Global.not_falsy"></a>

#### not\_falsy

```python
def not_falsy(var)
```

This function returns True to verify that var is NOT falsy: not in [None, np.nan, 0, False]


**Arguments**:

- `var` _float_ - variable to check
  

**Returns**:

- `(bool)` - True if not in [None, 0, False]

<a id="..run"></a>

# ..run

<a id="..run.generateinputs"></a>

# ..run.generateinputs

<a id="..run.generateinputs.generate"></a>

#### generate

```python
def generate(vocation, dst=gl.OPTIMIZATION_AND_TCO_RCRS)
```

This function aggregates specifications from users for powertrains, desired ranges, component costs etc. into two
csv files - FASTSimInputs and OtherInputs

**Arguments**:

- `vocation` _str_ - Vocation type description
- `dst` _str, optional_ - results directory file path. Defaults to gl.OPTIMIZATION_AND_TCO_RCRS.

<a id="..run.run_scenario"></a>

# ..run.run\_scenario

Module for loading vehicles, scenarios, running them and managing them

<a id="..run.run_scenario.set_test_weight"></a>

#### set\_test\_weight

```python
def set_test_weight(vehicle, scenario)
```

assign standardized vehicle mass for accel and grade test using GVWR and GVWR Credit

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `scenario` _t3co.run_scenario.Scenario_ - T3CO scenario object

<a id="..run.run_scenario.reset_vehicle_weight"></a>

#### reset\_vehicle\_weight

```python
def reset_vehicle_weight(vehicle)
```

This function resets vehicle mass after loaded weight tests are done for accel and grade

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object

<a id="..run.run_scenario.limit_cargo_kg_for_moo_hev_bev"></a>

#### limit\_cargo\_kg\_for\_moo\_hev\_bev

```python
def limit_cargo_kg_for_moo_hev_bev(opt_scenario, mooadvancedvehicle)
```

This helper method is used within T3COProblem to assign limited cargo capacity based on GVWR + GVWRCredit and optimization vehicle mass for advanced vehicles

**Arguments**:

- `opt_scenario` _t3co.run_scenario.Scenario_ - T3CO scenario object
- `mooadvancedvehicle` _fastsim.vehicle.Vehicle_ - pymoo optimization vehicle

<a id="..run.run_scenario.set_max_motor_kw"></a>

#### set\_max\_motor\_kw

```python
def set_max_motor_kw(analysis_vehicle, scenario, max_motor_kw)
```

This helper method is used within T3COProblem to set max_motor_kw to optimization vehicle and set kw_demand_fc_on if PHEV

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `scenario` _t3co.run_scenario.Scenario_ - T3CO Scenarion object
- `max_motor_kw` _float_ - max motor power /kW

<a id="..run.run_scenario.set_max_battery_kwh"></a>

#### set\_max\_battery\_kwh

```python
def set_max_battery_kwh(analysis_vehicle, max_ess_kwh)
```

This helper method is used within T3COProblem to set max_ess_kwh to optimization vehicle

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `max_ess_kwh` _float_ - max energy storage system energy capacity /kWh

<a id="..run.run_scenario.set_max_battery_power_kw"></a>

#### set\_max\_battery\_power\_kw

```python
def set_max_battery_power_kw(analysis_vehicle, max_ess_kw)
```

This helper method is used within T3COProblem to set max_ess_kwx to optimization vehicle

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `max_ess_kw` _float_ - max energy storage system power /kW

<a id="..run.run_scenario.set_max_fuel_converter_kw"></a>

#### set\_max\_fuel\_converter\_kw

```python
def set_max_fuel_converter_kw(analysis_vehicle, fc_max_out_kw)
```

This helper method is used within T3COProblem to set fc_max_out_kw to optimization vehicle

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `fc_max_out_kw` _float_ - max fuel converter power /kW

<a id="..run.run_scenario.set_fuel_store_kwh"></a>

#### set\_fuel\_store\_kwh

```python
def set_fuel_store_kwh(analysis_vehicle, fs_kwh)
```

This helper method is used within T3COProblem to set fs_kwh to optimization vehicle

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `fs_kwh` _float_ - fuel storage energy capacity /kWh

<a id="..run.run_scenario.set_cargo_kg"></a>

#### set\_cargo\_kg

```python
def set_cargo_kg(analysis_vehicle, cargo_kg)
```

This helper method is used within T3COProblem to set cargo_kg to optimization vehicle

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `cargo_kg` _float_ - vehicle cargo capacity /kg

<a id="..run.run_scenario.Config"></a>

## Config Objects

```python
@dataclass
class Config()
```

New class to read T3COConfig file containing analysis attributes like vehicle and scenario paths, and scenario attribute overrides

<a id="..run.run_scenario.Config.from_file"></a>

#### from\_file

```python
def from_file(filename: str, analysis_id: int) -> Self
```

This method generates a Config dictionary from CSV file and calls Config.from_dict

**Arguments**:

- `filename` _str_ - path of input T3CO Config file
- `analysis_id` _int_ - analysis ID selections
  

**Returns**:

- `Self.from_dict` - method that gets Config instance from config_dict

<a id="..run.run_scenario.Config.from_dict"></a>

#### from\_dict

```python
def from_dict(config_dict: dict) -> Self
```

This method generates a Config instance from config_dict

**Arguments**:

- `config_dict` _dict_ - dictionary containing fields from T3CO Config input CSV file
  

**Returns**:

- `Self` - Config instance containining all values from T3CO Config CSV file

<a id="..run.run_scenario.Config.validate_analysis_id"></a>

#### validate\_analysis\_id

```python
def validate_analysis_id(filename: str, analysis_id: int = 0)
```

This method validates that correct analysis id is input

**Arguments**:

- `filename` _str_ - T3CO Config input CSV file path
  

**Raises**:

- `Exception` - Error if analysis_id not found

<a id="..run.run_scenario.Scenario"></a>

## Scenario Objects

```python
@dataclass
class Scenario()
```

Class object that contains all TCO parameters and performance target (range, grade, accel) information         for a vehicle such that performance and TCO can be computed during optimization

<a id="..run.run_scenario.Scenario.originalcargo_kg"></a>

#### originalcargo\_kg

if needed, should be assigned immediately after vehicle read in

<a id="..run.run_scenario.Scenario.plf_scenario_vehicle_cargo_capacity_kg"></a>

#### plf\_scenario\_vehicle\_cargo\_capacity\_kg

includes cargo credit kg

<a id="..run.run_scenario.Scenario.from_config"></a>

#### from\_config

```python
def from_config(config: Config = None)
```

This method overrides certain scenario fields if use_config is True and config object is not None

**Arguments**:

- `config` _Config, optional_ - Config object. Defaults to None.

<a id="..run.run_scenario.check_phev_init_socs"></a>

#### check\_phev\_init\_socs

```python
def check_phev_init_socs(a_vehicle: vehicle.Vehicle, scenario: Scenario)
```

This function checks that soc_norm_init_for_grade_pct and soc_norm_init_for_accel_pct are present only for PHEVs

**Arguments**:

- `a_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `scenario` _Scenario_ - T3CO scenario object

<a id="..run.run_scenario.get_phev_util_factor"></a>

#### get\_phev\_util\_factor

```python
def get_phev_util_factor(scenario, v, mpgge)
```

This function gets the PHEV utility factor derived from the computed range of the
vehicle and the operational day range computed from shifts per year and the first vmt year

**Arguments**:

- `scenario` _Scenario_ - T3CO scenario object
- `v` _fastsim.Vehicle.vehicle_ - FASTSim vehicle object
- `mpgge` _dict_ - Miles per Gallon Gasoline Equivalent dictionary
  

**Returns**:

- `uf` _float_ - PHEV computed utility factor

<a id="..run.run_scenario.get_objective_simdrive"></a>

#### get\_objective\_simdrive

```python
def get_objective_simdrive(analysis_vehicle: vehicle.Vehicle, cycle)
```

This function obtains the SimDrive for accel and grade test

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `cycle` _fastsim.cycle.Cycle_ - FASTSim Cycle object
  

**Returns**:

- `sd` _fastsim.simdrive.SimDrive_ - FASTSim SimDrive object containing vehicle inputs and simulation output attributes

<a id="..run.run_scenario.run_grade_or_accel"></a>

#### run\_grade\_or\_accel

```python
def run_grade_or_accel(test, analysis_vehicle, sim_drive, ess_init_soc)
```

This function handles initial SOC considerations for grade and accel tests

If ess_init_soc override is passed, use that
Else if the vehicle is an HEV, use the standard HEV init SOC values for accel and grade
Else, let FASTSim determine init SOC in sim_drive()
BEVs use max_soc
PHEVs use max_soc
Conv init_soc doesn't matter
HEVs attempt SOC balancing but that is overrident by HEV test init SOC

**Arguments**:

- `test` _str_ - 'accel' or 'grade' test
- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `sim_drive` _fastsim.simdrive.SimDrive_ - FASTSim SimDrive object
- `ess_init_soc` _float_ - ESS initial state of charge (SOC)
  

**Raises**:

- `Exception` - if test not in ['accel', 'grade']

<a id="..run.run_scenario.create_fastsim_vehicle"></a>

#### create\_fastsim\_vehicle

```python
def create_fastsim_vehicle(veh_dict=None)
```

This function creates and returns an empty FASTSim vehicle object with no attributes or

**Arguments**:

- `veh_dict` _dict, optional_ - Vehicle attributes dict. Defaults to None.
  

**Returns**:

- `v` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object

<a id="..run.run_scenario.get_vehicle"></a>

#### get\_vehicle

```python
def get_vehicle(veh_no, veh_input_path)
```

This function loads vehicle object from vehicle number and input csv filepath

**Arguments**:

- `veh_no` _int_ - vehicle selection number
- `veh_input_path` _str_ - vehicle model assumptions input CSV file path
  

**Returns**:

- `veh` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object

<a id="..run.run_scenario.get_scenario_and_cycle"></a>

#### get\_scenario\_and\_cycle

```python
def get_scenario_and_cycle(veh_no,
                           scenario_inputs_path,
                           a_vehicle=None,
                           config=None)
```

This function uses helper methods load_scenario and load_design_cycle_from_scenario         to get scenario object and cycle object corresponding to selected vehicle (by veh_no)

**Arguments**:

- `veh_no` _int_ - vehicle selection number
- `scenario_inputs_path` _str_ - input file path for scenario assumptions CSV
- `a_vehicle` _fastsim.vehicle.Vehicle, optional_ - FASTSim vehicle object for given selection. Defaults to None.
- `config` _Config, optional_ - Config object for current analysis. Defaults to None.
  

**Returns**:

- `scenario` _Scenario_ - T3CO scenario object selected
- `cyc` _fastsim.cycle.Cycle_ - FASTSim cycle object selected

<a id="..run.run_scenario.load_scenario"></a>

#### load\_scenario

```python
def load_scenario(veh_no, scenario_inputs_path, a_vehicle=None, config=None)
```

This function gets the Scenario object from scenario input CSV filepath, initializes some fields,          and overrides some fields based on Config object

**Arguments**:

- `veh_no` _int_ - vehicle selection number
- `scenario_inputs_path` _str_ - input file path for scenario assumptions CSV
- `a_vehicle` _fastsim.vehicle.Vehicle, optional_ - FASTSim vehicle object for given selection. Defaults to None.
- `config` _Config, optional_ - Config object for current analysis. Defaults to None.
  

**Returns**:

- `scenario` _Scenario_ - Scenario object for given selection

<a id="..run.run_scenario.load_design_cycle_from_scenario"></a>

#### load\_design\_cycle\_from\_scenario

```python
def load_design_cycle_from_scenario(scenario,
                                    cyc_file_path=gl.OPTIMIZATION_DRIVE_CYCLES
                                    )
```

This helper method loads the design cycle used for mpgge and range determination.
It can also be used standalone to get cycles not in standard gl.OPTIMIZATION_DRIVE_CYCLES location,
but still needs cycle name from scenario object, carried in scenario.drive_cycle.
If the drive cycles are a list of tuples, handle accordingly with eval.

**Arguments**:

- `scenario` _Scenario_ - Scenario object for current selection
- `cyc_file_path` _str, optional_ - drivecycle input file path. Defaults to gl.OPTIMIZATION_DRIVE_CYCLES.
  

**Returns**:

- `range_cyc` _fastsim.cycle.Cycle_ - FASTSim cycle object for current Scenario object

<a id="..run.run_scenario.load_design_cycle_from_path"></a>

#### load\_design\_cycle\_from\_path

```python
def load_design_cycle_from_path(cyc_file_path)
```

This helper method loads the Cycle object from the drivecycle filepath

**Arguments**:

- `cyc_file_path` _str_ - drivecycle input file path
  

**Returns**:

- `range_cyc` _fastsim.cycle.Cycle_ - FASTSim cycle object for current Scenario object

<a id="..run.run_scenario.vehicle_scenario_sweep"></a>

#### vehicle\_scenario\_sweep

```python
def vehicle_scenario_sweep(vehicle,
                           scenario,
                           range_cyc,
                           verbose=False,
                           **kwargs)
```

This function contains helper methods such as get_tco_of_vehicle, check_phev_init_socs, get_accel, and get_gradeability    and returns a dictionary of all TCO related outputs

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for current selection
- `scenario` _Scenario_ - Scenario object for current selection
- `range_cyc` _fastsim.cycle.Cycle_ - FASTSim cycle object for current scenario
- `verbose` _bool, optional_ - if selected, prints out the TCO calculation process. Defaults to False.
  

**Returns**:

- `out` _dict_ - output dictionary containing TCO elements

<a id="..run.run_scenario.run"></a>

#### run

```python
def run(veh_no,
        vocation="blank",
        vehicle_input_path=gl.FASTSIM_INPUTS,
        scenario_inputs_path=gl.OTHER_INPUTS)
```

This function runs vehicle_scenario_sweep based on vehicle and scenario objects read from input file paths

**Arguments**:

- `veh_no` _int_ - vehicle selection number
- `vocation` _str, optional_ - vocation description of selected vehicle. Defaults to "blank".
- `vehicle_input_path` _str, optional_ - input file path for vehicle assumptions CSV. Defaults to gl.FASTSIM_INPUTS.
- `scenario_inputs_path` _str, optional_ - input file path for scenario assumptions CSV. Defaults to gl.OTHER_INPUTS.
  

**Returns**:

- `out` _dict_ - output dictionary containing TCO results

<a id="..run.run_scenario.rerun"></a>

#### rerun

```python
def rerun(vehicle, vocation, scenario)
```

This function runs vehicle_scenario_sweep when given the vehicle and scenario objects

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object
- `vocation` _str_ - vocation description
- `scenario` _Scenario_ - Scenario object
  

**Returns**:

- `out` _dict_ - output dictionary containing TCO outputs

<a id="..demos.opp_cost_demo"></a>

# ..demos.opp\_cost\_demo

<a id="..demos.hev_sweep_and_moo"></a>

# ..demos.hev\_sweep\_and\_moo

<a id="..demos.hev_sweep_and_moo.vnum"></a>

#### vnum



<a id="..demos.example_load_and_run"></a>

# ..demos.example\_load\_and\_run

To run this as a script that drives all the t3co files as a module:
The working directory for this script should be at the same depth as the t3co/ module.
Thus the scripts (run_scenario.py, etc.) will have a parent package and you won't get relative import errors.
ex: run_one.__name__ will be "t3co.run_one"

First step, generateinputs.generate(vocation)
Create the files necessary such that run_scenario.run() can read information for Vehicle and Scenario object
instantiation.

tldr:
generateinputs(vocation) -> gl.FASTSIM_INPUTS, gl.OTHER_INPUTS -> run_scenario.run(gl.FASTSIM_INPUTS, gl.OTHER_INPUTS)

Generate Inputs (GI) first retrieves specific user generated information necessary to create
two final product files used for TCO and optimization: gl.FASTSIM_INPUTS & gl.OTHER_INPUTS.

(GI) gets the user generated information via the specified vocation and the following files:
"t3co/resources/vehicles/{vocation}/specifications/BaselineVehicle.csv"
"...OptimizerInitializationValues.csv"
"...PowertrainTechTargets.csv"
"...VocationRequirements.csv"

Note: the folder {vocation} must exist and be populated by the user beforehand.

gl.FASTSIM_INPUTS & gl.OTHER_INPUTS are populated and stored in the default global locations that
run_scenario.run() uses as default params - implying run() can use other FASTSIM_INPUTS & OTHER_INPUTS files
if desired.

Content of gl.FASTSIM_INPUTS and gl.OTHER_INPUTS:

gl.FASTSIM_INPUTS content:
# standard FASTSim input file header and rows
selection,scenario_name,veh_pt_type,drag_coef,frontalAreaM2,glid...
1.0,"Conv 2020 tech,  750 mi range",1.0,0.546,10.18,11776.0,0...
2.0,"Conv 2025 tech,  750 mi range",1.0,0.5026666670000001,10...
3.0,"Conv 2030 tech,  750 mi range",1.0,0.473125,10.18,11776....
4.0,"Conv 2035 tech,  750 mi range",1.0,0.46,10.18,11776.0,0....

gl.OTHER_INPUTS content:
# all information necessary to determine vehicle TCO as well as performance targets
selection,drive_cycle,vmt_reduct_per_yr,vmt,constant_trip_distance_mi,vehicle_life_yr,...,region,target_range_mi,min_speed_at_6pct_grade_in_5min_mph,min_speed_at_125pct_grade_in_5min_mph,max0to60secAtGV
1.0,long_haul_cyc.csv,0.0,"[100000, 100000, 100000, 100000, 100000, 100000...United States,750.0,30.0,65.0,80.0,20.0
2.0,long_haul_cyc.csv,,"[100000, 100000, 100000, 100000, 100000, 100000, 1...United States,750.0,30.0,65.0,80.0,20.0
3.0,long_haul_cyc.csv,,"[100000, 100000, 100000, 100000, 100000, 100000, 1...United States,750.0,30.0,65.0,80.0,20.0
4.0,long_haul_cyc.csv,,"[100000, 100000, 100000, 100000, 100000, 100000, 1...United States,750.0,30.0,65.0,80.0,20.0
5.0,long_haul_cyc.csv,,"[100000, 100000, 100000, 100000, 100000, 100000, 1...United States,750.0,30.0,65.0,80.0,20.0

default values for these files generated by generateinputs():
gl.FASTSIM_INPUTS: ./t3co/resources/"FASTSimInputs.csv"
gl.OTHER_INPUTS:   ./t3co/resources/"OtherInputs.csv"

These files are populated in generateinputs.generate()
FASTSimInputsDf.to_csv(dst/gl.FASTSIM_INPUTS_FILE, index=False)
OtherInputsDf.to_csv(dst/gl.OTHER_INPUTS_FILE, index=False)

where
gl.FASTSIM_INPUTS_FILE = "FASTSimInputs.csv"
gl.OTHER_INPUTS = "OtherInputs.csv"
and
dst is usually ./t3co/resources

run() usage:
run_scenario.run(veh_no, vocation, vehicle_input_path=gl.FASTSIM_INPUTS,
scenario_inputs_path=gl.OTHER_INPUTS,

>>> print('running', __name__)
>>> generateinputs.generate('Class8_long_haul')
>>> use_jit = False
>>> start = time.time()
>>> res1 = run_scenario.run(1, 'Class8_long_haul', use_jit=use_jit)
>>> print(f'classic time [s] {time.time()-start} | use jit? {use_jit}')

<a id="..demos.t2co_opt_benchmark"></a>

# ..demos.t2co\_opt\_benchmark

<a id="..demos.Spencer"></a>

# ..demos.Spencer

