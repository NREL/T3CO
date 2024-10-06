# Table of Contents

* [t3co/tco/tcocalc](#t3co/tco/tcocalc)
  * [find\_residual\_rates](#t3co/tco/tcocalc.find_residual_rates)
  * [calculate\_dollar\_cost](#t3co/tco/tcocalc.calculate_dollar_cost)
  * [calculate\_opp\_costs](#t3co/tco/tcocalc.calculate_opp_costs)
  * [fill\_fuel\_eff\_file](#t3co/tco/tcocalc.fill_fuel_eff_file)
  * [fill\_veh\_expense\_file](#t3co/tco/tcocalc.fill_veh_expense_file)
  * [fill\_trav\_exp\_tsv](#t3co/tco/tcocalc.fill_trav_exp_tsv)
  * [fill\_downtimelabor\_cost\_tsv](#t3co/tco/tcocalc.fill_downtimelabor_cost_tsv)
  * [fill\_market\_share\_tsv](#t3co/tco/tcocalc.fill_market_share_tsv)
  * [fill\_fuel\_expense\_tsv](#t3co/tco/tcocalc.fill_fuel_expense_tsv)
  * [fill\_annual\_tsv](#t3co/tco/tcocalc.fill_annual_tsv)
  * [fill\_reg\_sales\_tsv](#t3co/tco/tcocalc.fill_reg_sales_tsv)
  * [fill\_insurance\_tsv](#t3co/tco/tcocalc.fill_insurance_tsv)
  * [fill\_residual\_cost\_tsc](#t3co/tco/tcocalc.fill_residual_cost_tsc)
  * [fill\_survival\_tsv](#t3co/tco/tcocalc.fill_survival_tsv)
  * [fill\_fuel\_split\_tsv](#t3co/tco/tcocalc.fill_fuel_split_tsv)

<a id="t3co/tco/tcocalc"></a>

# t3co/tco/tcocalc

<a id="t3co/tco/tcocalc.find_residual_rates"></a>

#### find\_residual\_rates

```python
def find_residual_rates(vehicle: fastsim.vehicle.Vehicle,
                        scenario: run_scenario.Scenario) -> float
```

This helper method gets the residual rates from ResidualValues.csv

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
  

**Returns**:

- `residual_rates` _float_ - Residual rate as percentage of MSRP

<a id="t3co/tco/tcocalc.calculate_dollar_cost"></a>

#### calculate\_dollar\_cost

```python
def calculate_dollar_cost(veh: fastsim.vehicle.Vehicle,
                          scenario: run_scenario.Scenario) -> dict
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

- `veh` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
  

**Returns**:

- `cost_set` _dict_ - Dictionary containing MSRP breakdown

<a id="t3co/tco/tcocalc.calculate_opp_costs"></a>

#### calculate\_opp\_costs

```python
def calculate_opp_costs(vehicle: fastsim.vehicle.Vehicle,
                        scenario: run_scenario.Scenario,
                        range_dict: dict) -> dict
```

This helper method calculates opportunity costs and generates veh_opp_cost_set from
-   Payload Lost Capacity Cost/Multiplier
-   Fueling Downtime
-   Maintenance and Repair Downtime

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `range_dict` _dict_ - Dictionary containing range values from fueleconomy.get_range_mi()
  

**Returns**:

- `veh_opp_cost_set` _dict_ - Dictionary containing opportunity cost results

<a id="t3co/tco/tcocalc.fill_fuel_eff_file"></a>

#### fill\_fuel\_eff\_file

```python
def fill_fuel_eff_file(vehicle: fastsim.vehicle.Vehicle,
                       scenario: run_scenario.Scenario,
                       mpgge_dict: dict) -> pd.DataFrame
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

<a id="t3co/tco/tcocalc.fill_veh_expense_file"></a>

#### fill\_veh\_expense\_file

```python
def fill_veh_expense_file(scenario: run_scenario.Scenario,
                          cost_set: dict) -> pd.DataFrame
```

This helper method generates a dataframe of MSRP breakdown costs as Cost [$/veh]

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `cost_set` _dict_ - Dictionary containing MSRP breakdown cost components
  

**Returns**:

- `vexpdf` _pd.DataFrame_ - Dataframe containing MSRP components costs as Cost [$/veh]

<a id="t3co/tco/tcocalc.fill_trav_exp_tsv"></a>

#### fill\_trav\_exp\_tsv

```python
def fill_trav_exp_tsv(vehicle: fastsim.vehicle.Vehicle,
                      scenario: run_scenario.Scenario) -> pd.DataFrame
```

This helper method generates a dataframe containing maintenance costs in Cost [$/mi]

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing maintenance costs in Cost [$/mi]

<a id="t3co/tco/tcocalc.fill_downtimelabor_cost_tsv"></a>

#### fill\_downtimelabor\_cost\_tsv

```python
def fill_downtimelabor_cost_tsv(scenario: run_scenario.Scenario,
                                oppy_cost_set: dict) -> pd.DataFrame
```

This helper method generates a dataframe containing fueling downtime and M&R downtime costs in Cost [$/Yr]

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `oppy_cost_set` _dict_ - Dictionary containing fueling_downtime_oppy_cost_dol_per_yr,fueling_dwell_labor_cost_dol_per_yr and mr_downtime_oppy_cost_dol_per_yr
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing fueling and MR downtime costs in Cost [$/Yr]

<a id="t3co/tco/tcocalc.fill_market_share_tsv"></a>

#### fill\_market\_share\_tsv

```python
def fill_market_share_tsv(scenario: run_scenario.Scenario,
                          num_vs: int = 1) -> pd.DataFrame
```

This helper method generates a dataframe containing market share of current vehicle selection per vehicle sold

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `num_vs` _int, optional_ - Number of vehicles. Defaults to 1.
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing market share of current vehicle in Market Share [veh/veh]

<a id="t3co/tco/tcocalc.fill_fuel_expense_tsv"></a>

#### fill\_fuel\_expense\_tsv

```python
def fill_fuel_expense_tsv(vehicle: fastsim.vehicle.Vehicle,
                          scenario: run_scenario.Scenario) -> pd.DataFrame
```

This helper method generates a dataframe of fuel operating costs in Cost [$/gge]

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
  

**Raises**:

- `Exception` - Invalid fuel_type type
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing fuel operating costs in Cost [$/gge]

<a id="t3co/tco/tcocalc.fill_annual_tsv"></a>

#### fill\_annual\_tsv

```python
def fill_annual_tsv(scenario: run_scenario.Scenario) -> pd.DataFrame
```

This helper method generates a dataframe of annual vehicle miles traveled (vmt) - Annual Travel [mi/yr]

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing Annual Travel [mi/yr]

<a id="t3co/tco/tcocalc.fill_reg_sales_tsv"></a>

#### fill\_reg\_sales\_tsv

```python
def fill_reg_sales_tsv(scenario: run_scenario.Scenario,
                       num_vs: int = 1) -> pd.DataFrame
```

This helper method generates a dataframe containing vehicle sales per year - Sales [veh]

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `num_vs` _int, optional_ - Number of vehicles. Defaults to 1.
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing vehicle sales in Sales [veh]

<a id="t3co/tco/tcocalc.fill_insurance_tsv"></a>

#### fill\_insurance\_tsv

```python
def fill_insurance_tsv(scenario: run_scenario.Scenario,
                       veh_cost_set: dict) -> pd.DataFrame
```

This helper method generates a dataframe containing vehicle insurance costs as Cost [$/Yr]

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `veh_cost_set` _dict_ - Dictionary containing MSRP costs
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing insurance costs in Cost [$/Yr]

<a id="t3co/tco/tcocalc.fill_residual_cost_tsc"></a>

#### fill\_residual\_cost\_tsc

```python
def fill_residual_cost_tsc(vehicle: fastsim.vehicle.Vehicle,
                           scenario: run_scenario.Scenario,
                           veh_cost_set: dict) -> pd.DataFrame
```

This helper method generates a dataframe of residual costs as Cost [$/Yr]

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `veh_cost_set` _dict_ - Dictionary containing MSRP costs
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing vehicle residual costs as Cost [$/Yr]

<a id="t3co/tco/tcocalc.fill_survival_tsv"></a>

#### fill\_survival\_tsv

```python
def fill_survival_tsv(scenario: run_scenario.Scenario,
                      num_vs=1) -> pd.DataFrame
```

This helper method generates a dataframe containing surviving vehicles as Surviving Vehicles [veh/veh]

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `num_vs` _int, optional_ - Number of vehicles. Defaults to 1.
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing number of surviving vehicles on road in Surviving Vehicles [veh/veh]

<a id="t3co/tco/tcocalc.fill_fuel_split_tsv"></a>

#### fill\_fuel\_split\_tsv

```python
def fill_fuel_split_tsv(vehicle: fastsim.vehicle.Vehicle,
                        scenario: run_scenario.Scenario,
                        mpgge: dict) -> pd.DataFrame
```

This helper method generates a dataframe of fraction of travel in each fuel type as Fraction of Travel [mi/mi]

**Arguments**:

- `vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `mpgge` _dict_ - MPGGE dictionary from fueleconomy.get_mpgge()
  

**Returns**:

- `df` _pd.DataFrame_ - Dataframe containing fraction of travel in each fuel type as Fraction of Travel [mi/mi]

