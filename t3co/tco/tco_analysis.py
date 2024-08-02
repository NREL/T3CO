from t3co.objectives import fueleconomy
from t3co.run import Global as gl
from t3co.tco import tco_stock_emissions
from t3co.tco import tcocalc as tcocalc

# for debugging
# import importlib
# fueleconomy = importlib.reload(fueleconomy)

STD_VAR_NAMES = "stdVarNames"


def get_operating_costs(ownershipCosts, TCO_switch="DIRECT"):
    """
    This function creates a dataframe of operating cost from ownershipCosts dataframe based on TCO_switch ('DIRECT' or 'EFFICIENCY')

    Args:
        ownershipCosts (pd.DataFrame): Dataframe containing year-wise ownership costs estimations like Fuel, maintenance, insurance, etc
        TCO_switch (str, optional): Switch between different TCO calculations - 'DIRECT' or 'EFFICIENCY'. Defaults to 'DIRECT'.

    Returns:
        operatingCosts_df (pd.DataFrame): Dataframe containing operating cost categories based on TCO_switch
    """
    if TCO_switch == "DIRECT":
        operating_costs_categories = [
            "Fuel",
            "maintenance",
            "insurance",
            "fueling downtime cost",
            "MR downtime cost",
        ]
        operatingCosts_df = ownershipCosts[
            ownershipCosts["Category"].isin(operating_costs_categories)
        ]

    elif TCO_switch == "EFFICIENCY":
        operating_costs_categories = [
            "Fuel",
            "maintenance",
            "insurance",
            "fueling downtime cost",
        ]

        operatingCosts_df = ownershipCosts[
            ownershipCosts["Category"].isin(operating_costs_categories)
        ]
    return operatingCosts_df


def discounted_costs(scenario, ownershipCosts):
    """
    This function calculates the yearly discounted costs for each category of ownershipCosts based on scenario.discount_rate_pct_per_yr

    Args:
        scenario (run_scenario.Scenario): Scenario object for current selection
        ownershipCosts (pd.DataFrame): Dataframe containing year-wise ownership costs estimations like Fuel, maintenance, insurance, etc

    Returns:
        ownershipCosts (pd.DataFrame): ownershipCosts dataframe with additional 'Discounted Cost [$]' column
    """
    ownershipCosts["Discounted Cost [$]"] = ownershipCosts["Cost [$]"] / (
        1.0 + scenario.discount_rate_pct_per_yr
    ) ** (ownershipCosts["Year"] - ownershipCosts["Model Year"])
    # veh_opp_cost_set['Discounted Cost [$]'] = veh_opp_cost_set['Cost [$]'] / (1. + scenario.discount_rate_pct_per_yr) ** (veh_opp_cost_set['Year'] - veh_opp_cost_set['Model Year'])
    # veh_residual_df['Discounted Cost [$]'] = veh_residual_df['Cost [$]'] / (1. + scenario.discount_rate_pct_per_yr) ** (veh_residual_df['Year'] - veh_residual_df['Model Year'])

    return ownershipCosts


def calc_discountedTCO(
    scenario,
    discounted_costs_df,
    veh_cost_set,
    veh_opp_cost_set,
    sim_drive,
    TCO_switch="DIRECT",
):
    """
    This function calculates the discounted Total Cost of Ownerhip (discounted to account for time-value of money).
    There are two methods to calculate discounted TCO - 'DIRECT' and 'EFFICIENCY'

    Args:
        scenario (run_scenario.Scenario): Scenario object for current selection
        discounted_costs_df (pd.DataFrame): discounted operating costs dataframe
        veh_cost_set (dict): Dictionary containing MSRP breakdown
        veh_opp_cost_set (dict): Dictionary containing opportunity costs breakdown
        sim_drive (fastsim.simdrive.SimDrive): FASTSim.simdrive.SimDrive object containing inputs and outputs from vehicle simulation over a cycle
        TCO_switch (str, optional): Switch between different TCO calculations - 'DIRECT' or 'EFFICIENCY'. Defaults to 'DIRECT'.

    Returns:
        discountedTCO (float): Discounted Total Cost of Ownership value
        oppy_cost_Dol_set (dict): Dictionary containing discounted opportunity costs breakdown
        veh_oper_cost_set (dict): Dictionary containing discounted operating costs breakdown
    """
    operatingCosts_df = get_operating_costs(discounted_costs_df, TCO_switch)
    totaloperatingCosts_df = operatingCosts_df.groupby(["Year", "Model Year"]).sum(
        "Cost [$]"
    )

    payloadmultiplier = veh_opp_cost_set["payload_cap_cost_multiplier"] or 1
    disc_operating_costs = totaloperatingCosts_df["Discounted Cost [$]"].sum()
    disc_residual_costs = discounted_costs_df[
        discounted_costs_df["Category"].isin(["residual cost"])
    ]["Discounted Cost [$]"].sum()
    disc_opportunity_costs = discounted_costs_df[
        discounted_costs_df["Category"].isin(
            ["fueling downtime cost", "MR downtime cost"]
        )
    ]["Discounted Cost [$]"].sum()
    sum_operating_costsdf = operatingCosts_df.groupby("Category", as_index=False).sum(
        "Discounted Cost [$]"
    )
    veh_oper_cost_set = dict(
        zip(
            sum_operating_costsdf["Category"],
            sum_operating_costsdf["Discounted Cost [$]"],
        )
    )
    if TCO_switch == "DIRECT":
        discountedTCO = payloadmultiplier * (
            veh_cost_set["msrp"]
            + veh_cost_set["Purchase tax"]
            + disc_operating_costs
            + disc_residual_costs
        )
        payload_capacity_cost = (
            (payloadmultiplier - 1) / payloadmultiplier * discountedTCO
        )
        oppy_cost_Dol_set = {
            "downtime_oppy_cost_Dol": disc_opportunity_costs,
            "payload_capacity_cost_Dol": payload_capacity_cost,
        }

    elif TCO_switch == "EFFICIENCY":
        disc_VMT_sum = sum(
            [
                scenario.vmt[i] / (1 + scenario.discount_rate_pct_per_yr) ** (i)
                for i in range(scenario.vehicle_life_yr)
            ]
        )
        disc_downtime_sum = sum(
            [
                veh_opp_cost_set["total_downtime_hrPerYr"][i]
                / (1 + scenario.discount_rate_pct_per_yr) ** (i + 1)
                for i in range(scenario.vehicle_life_yr)
            ]
        )
        avg_speed_mph = (
            sum(sim_drive.cyc.mps) / max(sim_drive.cyc.time_s) * gl.mps_to_mph
        )
        downtime_efficiency = 1 / (1 + avg_speed_mph * disc_downtime_sum / disc_VMT_sum)
        # print(f'downtime_efficiency = {downtime_efficiency}')
        discountedTCO = payloadmultiplier * (
            (veh_cost_set["msrp"] + veh_cost_set["Purchase tax"] + disc_operating_costs)
            / downtime_efficiency
            + disc_residual_costs
        )
        downtime_oppy_cost_Dol = (
            veh_cost_set["msrp"]
            + veh_cost_set["Purchase tax"]
            + disc_operating_costs
            + disc_opportunity_costs
        ) * (1 / downtime_efficiency - 1)
        payload_capacity_cost = (
            (payloadmultiplier - 1) / payloadmultiplier * discountedTCO
        )
        oppy_cost_Dol_set = {
            "downtime_oppy_cost_Dol": downtime_oppy_cost_Dol,
            "payload_capacity_cost_Dol": payload_capacity_cost,
        }

    return discountedTCO, oppy_cost_Dol_set, veh_oper_cost_set


def get_tco_of_vehicle(vehicle, range_cyc, scenario, write_tsv=False):
    """
    This function calculates the Total Cost of Ownership of a vehicle and scenario for a given cycle. The three main components are:
    - Opportunity Costs
    - MSRP
    - Operating Costs

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object of selected vehicle
        range_cyc (fastsim.cycle.Cycle): FASTSim range cycle object 
        scenario (run_scenario.Scenario): Scenario object for current selection
        write_tsv (bool, optional): if True, save intermediate files as TSV. Defaults to False.

    Returns:
        tot_cost_Dol (float): TCO in dollars
        discounted_TCO_Dol (float): discounted TCO in dollars
        oppy_cost_set (dict): Dictionary of opportunity cost breakdown
        ownership_costs_df (pd.DataFrame): Ownerhip Costs dataframe containing different categories per year
        discounted_costs_df (pd.DataFrame): discounted Ownerhip Costs dataframe containing different categories per year
        mpgge (dict): Dictionary containing MPGGEs
        veh_cost_set (dict): Dictionary containing MSRP breakdown
        design_cycle_sdr (fastsim.simdrive.SimDrive): FASTSim SimDrive object for design drivecycle
        veh_oper_cost_set (dict): Dictionary containing operating costs breakdown
        veh_opp_cost_set (dict): Dictionary containing opportunity costs breakdown
        tco_files (dict): Dictionary containing TCO intermediate dataframes
    """

    mpgge, sim_drives = fueleconomy.get_mpgge(range_cyc, vehicle, scenario)
    range_dict = fueleconomy.get_range_mi(mpgge, vehicle, scenario)
    veh_opp_cost_set = tcocalc.calculate_opp_costs(vehicle, scenario, range_dict)
    veh_cost_set = tcocalc.calculate_dollar_cost(vehicle, scenario)
    veh_eff_df = tcocalc.fill_fuel_eff_file(vehicle, scenario, mpgge)
    veh_exp_df = tcocalc.fill_veh_expense_file(scenario, veh_cost_set)
    veh_spt_df = tcocalc.fill_fuel_split_tsv(vehicle, scenario, mpgge)
    veh_txp_df = tcocalc.fill_trav_exp_tsv(vehicle, scenario)
    veh_fxp_df = tcocalc.fill_fuel_expense_tsv(vehicle, scenario)
    veh_shr_df = tcocalc.fill_market_share_tsv(scenario)
    ann_trv_df = tcocalc.fill_annual_tsv(scenario)
    reg_sls_df = tcocalc.fill_reg_sales_tsv(scenario)
    survivl_df = tcocalc.fill_survival_tsv(scenario)
    veh_insurance_df = tcocalc.fill_insurance_tsv(scenario, veh_cost_set)
    veh_residual_df = tcocalc.fill_residual_cost_tsc(vehicle, scenario, veh_cost_set)
    veh_downtime_labor_df = tcocalc.fill_downtimelabor_cost_tsv(
        scenario, veh_opp_cost_set
    )

    # emission_df = pd.read_csv(gl.TCO_INTERMEDIATES / gl.EMISSION_RATE_TSV, index_col=None, header=0, sep='\t')
    emission_df = None

    # run stock model
    stock, emissions, ownership_costs_df = tco_stock_emissions.stockModel(
        reg_sls_df,
        veh_shr_df,
        survivl_df,
        ann_trv_df,
        veh_spt_df,
        veh_eff_df,
        emission_df,
        veh_exp_df,
        veh_txp_df,
        veh_fxp_df,
        veh_insurance_df,
        veh_residual_df,
        veh_downtime_labor_df,
        write_files=gl.write_files,
    )

    # discountRate = float(scenario.discount_rate_pct_per_yr)
    # discounted_costs_df = DCF(ownership_costs_df.copy(), rate=discountRate)
    # print(discounted_costs_df)
    discounted_costs_df = discounted_costs(scenario, ownership_costs_df)
    # should only be one vocation in these files but this as good a thing to aggregate on as any
    tot_cost_Dol = discounted_costs_df["Cost [$]"].sum()

    # discounted_TCO_Dol, downtime_oppy_cost_Dol, veh_oper_cost_set = calc_discountedTCO(scenario, discounted_costs_df, veh_cost_set, veh_opp_cost_set, sim_drives[-1], TCO_switch = 'DIRECT')
    # print(f'New disc DIRECT TCO: {discounted_TCO_Dol}')
    discounted_TCO_Dol, oppy_cost_set, veh_oper_cost_set = calc_discountedTCO(
        scenario,
        discounted_costs_df,
        veh_cost_set,
        veh_opp_cost_set,
        sim_drives[-1],
        TCO_switch="EFFICIENCY",
    )
    # print(f'New disc EFFICIENCY TCO: {discounted_TCO_Dol}')

    # if veh_opp_cost_set['payload_cap_cost_multiplier'] is not None:
    #     discounted_costs_df["Payload Corrected Discounted Cost [$]"] = \
    #       discounted_costs_df["Discounted Cost [$]"] * veh_opp_cost_set['payload_cap_cost_multiplier']
    #     disc_cost = discounted_costs_df["Payload Corrected Discounted Cost [$]"].sum()

    # write output files
    tco_files = {}
    if write_tsv:
        tco_files = {
            "veh_eff_df": veh_eff_df,
            "veh_exp_df": veh_exp_df,
            "veh_txp_df": veh_txp_df,
            "veh_shr_df": veh_shr_df,
            "veh_fxp_df": veh_fxp_df,
            "ann_trv_df": ann_trv_df,
            "reg_sls_df": reg_sls_df,
            "survivl_df": survivl_df,
            "veh_spt_df": veh_spt_df,
            "stock": stock,
            "ownership_costs_df": ownership_costs_df,
            "discounted_costs_df": discounted_costs_df,
        }

    return (
        tot_cost_Dol,
        discounted_TCO_Dol,
        oppy_cost_set,
        ownership_costs_df,
        discounted_costs_df,
        mpgge,
        veh_cost_set,
        sim_drives,
        veh_oper_cost_set,
        veh_opp_cost_set,
        tco_files,
    )

    # print(operatingCosts_df)
