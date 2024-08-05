#December 2018
#Stock Model in Python
# C. Hunter

import pandas as pd

from t3co.run import Global as gl


def dropCols(df):
    """
    This helper method drops columns if any row contains ['*']

    Args:
        df (pd.DataFrame): Input dataframe

    Returns:
        df (pd.DataFrame): Output dataframe with dropped dummy columns
    """
    if df is not None:
        droplist = [i for i in df.columns if df[i].isin(["*"]).any()]
        df = df.drop(droplist, axis=1)
    return df


def stockModel(
    sales,
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
    write_files=False,
):
    """
    This function generates the ownershipCosts dataframe from the dataframes for each cost category

    Args:
        sales (pd.DataFrame): Dataframe of yearly number of vehicles sales
        marketShares (pd.DataFrame): Dataframe of yearly Market Share of selection's vocation per vehicle [veh/veh]
        survival (pd.DataFrame): Dataframe of yearly Surviving vehicle per each vehicle [veh/veh]
        annualTravel (pd.DataFrame): Dataframe of vehicle's vmt: Annual Travel [mi/yr]
        fuelSplit (pd.DataFrame): Dataframe of fraction of travel using each fuel [mi/mi]
        fuelEfficiency (pd.DataFrame): Dataframe of vehicle's yearly average fuel efficiency [mi/gge]
        emissions (pd.DataFrame): Dataframe of vehicle's yearly average emissions
        vehicleCosts (pd.DataFrame, optional): Dataframe of vehicle components costs [Dol]. Defaults to None.
        travelCosts (pd.DataFrame, optional): Dataframe of maintenance costs [Dol/mi]. Defaults to None.
        fuelCosts (pd.DataFrame, optional): Dataframe of fuel operating costs [Dol/gge]. Defaults to None.
        insuranceCosts (pd.DataFrame, optional): Dataframe of yearly insurance costs [Dol]. Defaults to None.
        residualCosts (pd.DataFrame, optional): Dataframe of yearly residual costs [Dol]. Defaults to None.
        downtimeCosts (pd.DataFrame, optional): Dataframe of yearly downtime costs [Dol]. Defaults to None.
        write_files (bool, optional): if True, save vehicleCosts, travelCosts, fuelCosts, insuranceCosts,residualCosts, downtimeCosts . Defaults to False.

    Returns:
        stock (pd.DataFrame): Dataframe of stock model of vehicles in the market
        emissions (pd.DataFrame): Dataframe of total emissions
        ownershipCosts (pd.DataFrame): Dataframe of all ownership costs for given selection

    """
    # drop columns with *
    sales = dropCols(sales)
    marketShares = dropCols(marketShares)
    survival = dropCols(survival)
    annualTravel = dropCols(annualTravel)
    fuelSplit = dropCols(fuelSplit)
    fuelEfficiency = dropCols(fuelEfficiency)
    emissions = dropCols(emissions)
    vehicleCosts = dropCols(vehicleCosts)
    travelCosts = dropCols(travelCosts)
    fuelCosts = dropCols(fuelCosts)
    insuranceCosts = dropCols(insuranceCosts)
    residualCosts = dropCols(residualCosts)
    downtimeCosts = dropCols(downtimeCosts)

    # compute stock
    years = marketShares["Model Year"].unique()
    regionalSales = pd.merge(
        sales, marketShares
    )  # on='Model Year'  # seems to default to cross method
    regionalSales["Sales [veh]"] = (
        regionalSales["Sales [veh]"] * regionalSales["Market Share [veh/veh]"]
    )
    regionalSales = regionalSales.drop(["Market Share [veh/veh]"], axis=1)

    stock = []
    for y in years:
        df = regionalSales[regionalSales["Model Year"] <= y].copy()
        df["Year"] = y
        stock.append(df)

    stock = pd.concat(stock)
    stock["Age [yr]"] = stock["Year"] - stock["Model Year"]
    stock = pd.merge(survival, stock)
    stock["Stock [veh]"] = stock["Sales [veh]"] * stock["Surviving Vehicles [veh/veh]"]
    stock = stock.drop(["Surviving Vehicles [veh/veh]"], axis=1)

    # compute vmt
    stock = pd.merge(stock, annualTravel)
    stock["Travel [mi]"] = stock["Annual Travel [mi/yr]"] * stock["Stock [veh]"]
    # stock['Maintenance Cost [Dol/mi]'] = stock['Maintenance Cost [Dol/mi]'] * stock['Stock [veh]']
    stock = stock.drop(["Annual Travel [mi/yr]", "Age [yr]"], axis=1)

    # compute energy
    energy = pd.merge(pd.merge(stock, fuelEfficiency), fuelSplit)
    energy["Travel [mi]"] = (
        energy["Travel [mi]"] * energy["Fraction of Travel [mi/mi]"]
    )  # travel [mi] by fuel type
    energy["Energy [gge]"] = energy["Travel [mi]"] / energy["Fuel Efficiency [mi/gge]"]

    df = energy.copy()  # store for ownership costs calculations
    df["Age [yr]"] = df["Year"] - df["Model Year"]

    energy = energy.groupby(
        ["Region", "Vehicle", "Vocation", "Model Year", "Year"], as_index=False
    ).agg({"Energy [gge]": "sum"})
    stock = pd.merge(stock, energy).sort_values(
        by=["Year", "Model Year", "Region", "Vocation", "Vehicle"]
    )
    stock = stock[
        [
            "Year",
            "Region",
            "Vocation",
            "Vehicle",
            "Model Year",
            "Sales [veh]",
            "Stock [veh]",
            "Travel [mi]",
            "Energy [gge]",
        ]
    ]

    # # compute emissions if it specified
    # if emissions is not None: # quickly wrote this on 6/19/19 at 10pm at night. Probably a better way to make this more robust and optional inputs for other cost files as well
    #     emissions = pd.merge(df, emissions)
    #     emissions['Emission [g]'] = emissions['Emission Rate [g/gge]'] * emissions['Energy [gge]']
    #     emissions = emissions.drop(['Emission Rate [g/gge]'], axis=1)
    #     emissions = emissions.groupby(['Year','Region','Vocation','Vehicle','Fuel','Pollutant'], as_index=False).agg({'Stock [veh]' : np.sum, 'Travel [mi]' : np.sum, 'Energy [gge]' : np.sum, 'Emission [g]' : np.sum})

    # compute ownership costs
    vehicleCosts = pd.merge(vehicleCosts, df[df["Age [yr]"] < 0.1])
    vehicleCosts["Cost [$]"] = (
        vehicleCosts["Stock [veh]"] * vehicleCosts["Cost [$/veh]"]
    )
    vehicleCosts = vehicleCosts.drop(["Cost [$/veh]"], axis=1)

    travelCosts = pd.merge(travelCosts, df)

    travelCosts["Cost [$]"] = travelCosts["Travel [mi]"] * travelCosts["Cost [$/mi]"]
    travelCosts = travelCosts.drop(["Cost [$/mi]"], axis=1)

    fuelCosts = pd.merge(fuelCosts, df)
    fuelCosts["Cost [$]"] = fuelCosts["Energy [gge]"] * fuelCosts["Cost [$/gge]"]
    fuelCosts = fuelCosts.drop(["Cost [$/gge]"], axis=1)

    insuranceCosts = pd.merge(insuranceCosts, df)
    insuranceCosts["Cost [$]"] = insuranceCosts["Cost [$/Yr]"]
    insuranceCosts = insuranceCosts.drop(["Cost [$/Yr]"], axis=1)

    residualCosts = pd.merge(residualCosts, df)
    residualCosts["Cost [$]"] = residualCosts["Cost [$/Yr]"]
    residualCosts = residualCosts.drop(["Cost [$/Yr]"], axis=1)

    downtimeCosts = pd.merge(downtimeCosts, df)
    downtimeCosts["Cost [$]"] = downtimeCosts["Cost [$/Yr]"]
    downtimeCosts = downtimeCosts.drop(["Cost [$/Yr]"], axis=1)

    if write_files:
        vehicleCosts.to_csv(gl.TCO_INTERMEDIATES / "vehicle_costs.csv", index=False)
        travelCosts.to_csv(gl.TCO_INTERMEDIATES / "travel_costs.csv", index=False)
        fuelCosts.to_csv(gl.TCO_INTERMEDIATES / "fuel_costs.csv", index=False)
        insuranceCosts.to_csv(gl.TCO_INTERMEDIATES / "insurance_costs.csv", index=False)
        residualCosts.to_csv(gl.TCO_INTERMEDIATES / "residual_costs.csv", index=False)
        downtimeCosts.to_csv(gl.TCO_INTERMEDIATES / "downtime_costs.csv", index=False)

    # ownershipCosts = pd.concat([vehicleCosts, travelCosts, fuelCosts], sort=False)
    ownershipCosts = pd.concat(
        [
            vehicleCosts,
            travelCosts,
            fuelCosts,
            insuranceCosts,
            residualCosts,
            downtimeCosts,
        ]
    )
    ownershipCosts = ownershipCosts.groupby(
        ["Region", "Vehicle", "Vocation", "Model Year", "Year", "Category"],
        as_index=False,
    ).agg({"Cost [$]": "sum"})
    ownershipCosts = ownershipCosts.sort_values(
        by=["Year", "Model Year", "Region", "Vocation", "Vehicle"]
    )[["Year", "Region", "Vocation", "Vehicle", "Model Year", "Category", "Cost [$]"]]
    return stock, emissions, ownershipCosts
