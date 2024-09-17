# Table of Contents

* [tco.tco\_analysis](#tco.tco_analysis)
  * [get\_operating\_costs](#tco.tco_analysis.get_operating_costs)
  * [discounted\_costs](#tco.tco_analysis.discounted_costs)
  * [calc\_discountedTCO](#tco.tco_analysis.calc_discountedTCO)
  * [get\_tco\_of\_vehicle](#tco.tco_analysis.get_tco_of_vehicle)

<a id="tco.tco_analysis"></a>

# tco.tco\_analysis

<a id="tco.tco_analysis.get_operating_costs"></a>

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

<a id="tco.tco_analysis.discounted_costs"></a>

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

<a id="tco.tco_analysis.calc_discountedTCO"></a>

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

<a id="tco.tco_analysis.get_tco_of_vehicle"></a>

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
