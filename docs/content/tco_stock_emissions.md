# Table of Contents

* [tco.tco\_stock\_emissions](#tco.tco_stock_emissions)
  * [dropCols](#tco.tco_stock_emissions.dropCols)
  * [stockModel](#tco.tco_stock_emissions.stockModel)

<a id="tco.tco_stock_emissions"></a>

# tco.tco\_stock\_emissions

<a id="tco.tco_stock_emissions.dropCols"></a>

#### dropCols

```python
def dropCols(df)
```

This helper method drops columns if any row contains ['*']

**Arguments**:

- `df` _pd.DataFrame_ - Input dataframe
  

**Returns**:

- `df` _pd.DataFrame_ - Output dataframe with dropped dummy columns

<a id="tco.tco_stock_emissions.stockModel"></a>

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
- `annualTravel` _pd.DataFrame_ - Dataframe of vehicle's VMT: Annual Travel [mi/yr]
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

