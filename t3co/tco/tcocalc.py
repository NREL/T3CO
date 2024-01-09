import numpy as np
import pandas as pd

from t3co.run import Global as gl
from t3co.run import run_scenario
from t3co.tco import opportunity_cost

KG_2_LB = 2.20462


def kg_to_lbs(kgs):
    return kgs * KG_2_LB


# keeping this for when we do Emissions work
# with open(gl.TCO_INTERMEDIATES / gl.EMISSION_RATE_TSV, 'w', newline='') as er_file:
#         writer = csv.writer(er_file, delimiter='\t')
#         writer.writerow(["Vehicle", "Model Year", "Fuel", "Age [yr]", "Region", "Pollutant", "Emission Rate [g/gge]", "Vocation" ])


def find_residual_rates(
    vehicle, scenario
):  # finds residual rate at end of vehicle life
    """
    This helper method gets the residual rates from ResidualValues.csv

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object of analysis vehicle
        scenario (run_scenario.Scenario): Scenario object of current selection

    Returns:
        residual_rates (float): Residual rate as percentage of MSRP
    """
    residual_rates_all = pd.read_csv(gl.RESIDUAL_VALUE_PER_YEAR)
    vehicle_class = scenario.vehicle_class
    powertrain_type = vehicle.veh_pt_type.lower()
    year = str(scenario.vehLifeYears)
    residual_rates = residual_rates_all.loc[
        (residual_rates_all["VehicleClass"].str.lower() == vehicle_class)
        & (residual_rates_all["PowertrainType"].str.lower() == powertrain_type)
    ][year].values[0]
    return residual_rates


def calculate_dollar_cost(veh, scenario):
    """
    This helper method calculates the MSRP breakdown dictionary from
    -   Glider
    -   Fuel converter
    -   Fuel Storage
    -   Motor & power electronics
    -   Plug
    -   Battery
    -   Battery replacement
    -   Purchase tax

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object of analysis vehicle
        scenario (run_scenario.Scenario): Scenario object of current selection

    Returns:
        cost_set (dict): Dictionary containing MSRP breakdown
    """
    chargingOn = False

    iceBaseCost = scenario.iceBaseCost
    markup = scenario.markup
    iceDolPerKw = scenario.iceDolPerKw
    peAndMcBaseCost = scenario.peAndMcBaseCost
    peAndMcDolPerKw = scenario.peAndMcDolPerKw
    essPackageCost = scenario.essPackageCost
    essDolPerKwh = scenario.essDolPerKwh
    plugPrice = scenario.plugCost
    tax = scenario.tax
    # TODO add fuelCellDolPerKw in this list?

    # vehicle glider price does not have markup applied to it
    # on 11/23/2021 it was discussed but we decided it's fine to keep it this way. Glider price is an input that could
    # already have this factored in, especially for TDA, the current main user of T3CO
    vehGliderPrice = scenario.vehGliderPrice

    veh_pt_type = veh.veh_pt_type

    fc_max_kw = veh.fc_max_kw

    # old python fcEffType maps
    # if self.fcEffType == 1:    # SI:         SI engine
    # elif self.fcEffType == 2:  # Atkinson:   Atkinson cycle SI engine -- greater expansion
    # elif self.fcEffType == 3:  # Diesel:     Diesel (compression ignition) engine
    # elif self.fcEffType == 4:  # H2FC:       H2 fuel cell
    # elif self.fcEffType == 5:  # HD_Diesel:  heavy duty Diesel engine
    # new enumeration for types
    # FC_EFF_TYPES = ("SI", "Atkinson", "Diesel", "H2FC", "HD_Diesel")

    # #  TODO, need an assert for veh.fcEffType in vehicle.effTypes []
    # fcPrice
    if veh.veh_pt_type == gl.BEV or veh.fc_max_kw == 0:
        fcPrice = 0

    elif veh.fc_eff_type == "H2FC":
        fcPrice = scenario.fuelCellDolPerKw * fc_max_kw
    # TODO, what should 9 map too??
    elif veh.fc_eff_type == 9:
        fcPrice = (scenario.cngIceDolPerKw * fc_max_kw) + iceBaseCost

    else:
        fcPrice = (iceDolPerKw * fc_max_kw) + iceBaseCost
    fcPrice *= markup

    # TODO,this should get handled in fastsim.vehicle on INPUT VALIDATION
    # that code has a bug and some logic errors, needs fixing
    # if fcPrice != 0:
    #     eff_type_err_msg = f"ERROR: veh.fc_eff_type {veh.fc_eff_type} must be part of vehicle.FC_EFF_TYPES {vehicle.FC_EFF_TYPES}"
    #     eff_type_err_msg += """\n\toverwrite 1 with 'SI'\n\toverwrite 2 with 'Atkinson'"""
    #     eff_type_err_msg += """\n\toverwrite 3 with 'Diesel'\n\toverwrite 4 with 'H2FC'"""
    #     eff_type_err_msg += """\n\toverwrite 5 with 'HD_Diesel'"""
    #     assert veh.fc_eff_type in vehicle.FC_EFF_TYPES, eff_type_err_msg

    # fuelStorPrice
    if veh.veh_pt_type == gl.BEV:
        fuelStorPrice = 0
    elif veh.veh_pt_type == gl.HEV and scenario.fuel[0] == "hydrogen":
        fuelStorPrice = scenario.fuelStorH2DolPerKwh * veh.fs_kwh
    elif veh.veh_pt_type in [gl.CONV, gl.HEV, gl.PHEV] and scenario.fuel[0] == "cng":
        fuelStorPrice = scenario.fuelStorCngDolPerKwh * veh.fs_kwh
    elif veh.veh_pt_type in [gl.CONV, gl.HEV, gl.PHEV]:
        fuelStorPrice = scenario.fuelStorDolPerKwh * veh.fs_kwh
    fuelStorPrice *= markup

    # calculate mcPrice
    mc_max_kw = veh.mc_max_kw
    if mc_max_kw == 0:
        mcPrice = 0
    else:
        mcPrice = peAndMcBaseCost + (peAndMcDolPerKw * mc_max_kw)
    mc_max_kw *= markup

    # calc ESS price
    if veh.ess_max_kwh == 0:
        essPrice = 0
    else:
        essPrice = essPackageCost + (essDolPerKwh * veh.ess_max_kwh)
    essPrice *= markup

    # calc plugPrice
    if (
        veh_pt_type == gl.PHEV
        or veh_pt_type == gl.BEV
        or (veh_pt_type == gl.HEV and chargingOn)
    ):
        plugPrice = plugPrice
    else:
        plugPrice = 0
    plugPrice *= markup

    if veh_pt_type == gl.CONV:
        msrp = vehGliderPrice + fuelStorPrice + fcPrice
    # could be HEV or FCEV
    elif veh_pt_type == gl.HEV:
        msrp = vehGliderPrice + fuelStorPrice + fcPrice + mcPrice + essPrice
    elif veh_pt_type == gl.PHEV:
        msrp = vehGliderPrice + fuelStorPrice + fcPrice + mcPrice + essPrice + plugPrice
    elif veh_pt_type == gl.BEV:
        msrp = vehGliderPrice + mcPrice + essPrice + plugPrice

    pTaxCost = tax * msrp

    # insurance_cost = calc_insurance_costs(scenario=scenario, msrp=msrp)
    # residual_cost = calc_residual_cost(vehicle=veh, scenario=scenario, msrp=msrp)
    cost_set = {
        "Glider": vehGliderPrice,
        "Fuel converter": fcPrice,
        "Fuel Storage": fuelStorPrice,
        "Motor & power electronics": mcPrice,
        "Plug": plugPrice,
        "Battery": essPrice,
        "Battery replacement": 0,
        "Purchase tax": pTaxCost,
        "msrp": msrp,
        # "Insurance": insurance_cost,
        # "Residual Cost": residual_cost
    }
    return cost_set


def calculate_opp_costs(vehicle, scenario, range_dict):
    """
    This helper method calculates opportunity costs and generates veh_opp_cost_set from
    -   Payload Lost Capacity Cost/Multiplier
    -   Fueling Downtime
    -   Maintenance and Repair Downtime

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object of analysis vehicle
        scenario (run_scenario.Scenario): Scenario object of current selection
        range_dict (dict): Dictionary containing range values from fueleconomy.get_range_mi()
    """
    oppcostobj = opportunity_cost.OpportunityCost(scenario, range_dict)
    if scenario.activate_tco_payload_cap_cost_multiplier:
        # assert optvehicle.veh_pt_type in [gl.BEV, gl.HEV], "payload cap loss factor TCO element only available for BEVs and FCEV HEVs"
        assert gl.not_falsy(scenario.plf_reference_vehicle_empty_kg)
        assert np.isnan(scenario.plf_reference_vehicle_empty_kg) == False
        oppcostobj.get_payload_loss_factor(vehicle, scenario)

    if scenario.activate_dwell_time_loss_factor:
        # assert optvehicle.veh_pt_type in [gl.BEV, gl.HEV], "payload cap loss factor TCO element only available for BEVs and FCEV HEVs"
        assert gl.not_falsy(scenario.dlf_cost_dolperhr)
        assert not np.isnan(scenario.dlf_free_dwell_trips)
        assert not np.isnan(scenario.dlf_fraction_dwpt)
        assert not np.isnan(scenario.dlf_freetime_dwell_hr)
        assert not np.isnan(scenario.dlf_avg_noncharge_per_dwell_hr)
        assert (
            gl.not_falsy(scenario.shifts_per_year)
            and len(oppcostobj.shifts_per_year) >= scenario.vehLifeYears
        ), f"Provide scenario.shifts_per_year as a vector of length > scenario.vehLifeYears. Currently {len(oppcostobj.shifts_per_year)}"
        assert gl.not_falsy(scenario.dlf_frac_fullcharge_bounds)
        oppcostobj.get_dwell_time_cost(vehicle, scenario)

    if scenario.activate_mr_downtime_cost:
        assert gl.not_falsy(scenario.mr_regular_hrPerYear)
        assert any(np.isnan(scenario.mr_unplanned_hrPerMile)) == False
        assert np.isnan(scenario.mr_tire_replace_downtime_hrPerEvent) == False
        assert gl.not_falsy(scenario.mr_tire_life_mi)
        oppcostobj.get_M_R_downtime_cost(vehicle, scenario)

    # veh_opp_cost_set = {'payload_cap_cost_multiplier' : None, 'net_dwell_time_hr' : 0., 'dwell_time_cost_Dol' : 0.}
    veh_opp_cost_set = {
        "payload_cap_cost_multiplier": oppcostobj.payload_cap_cost_multiplier,
        "net_dwell_time_hr": oppcostobj.net_dwell_time_hr,
        "dwell_time_cost_Dol": oppcostobj.dwell_time_cost_Dol,
        "MR_downtime_hr": oppcostobj.net_MR_downtime_hrPerYr,
        "MR_downtime_cost_Dol": oppcostobj.net_MR_downtime_oppcosts_DolPerYr,
        "total_downtime_hrPerYr": np.array(oppcostobj.net_dwell_time_hr)
        + np.array(oppcostobj.net_MR_downtime_hrPerYr),
        # 'avg_speed_mph': oppcostobj.v_mean_mph,
    }
    return veh_opp_cost_set


def fill_fuel_eff_file(vehicle, scenario, mpgge_dict):
    """
    This helper method generates a dataframe of Fuel Efficiency [mi/gge]
    For PHEV, cd_grid_electric_mpgge, cd_fuel_mpgge, and cs_fuel_mpgge
    For BEV, grid_mpgge
    For HEV and CONV, mpgge

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object of analysis vehicle
        scenario (run_scenario.Scenario): Scenario object of current selection
        mpgge_dict (dict): MPGGE dictionary from fueleconomy.get_mpgge()

    Returns:
        fefdata (pd.DataFrame): Dictionary containing Fuel Efficiency [mi/gge]
    """
    # this fuel efficiency value is for over all fuel costs
    # so it needs to factor in charging efficiency, if applicable

    if vehicle.veh_pt_type == gl.PHEV:
        # grid efficiency charge depleting mpgge first, then charge sustaining
        mpgges = [
            mpgge_dict["cd_grid_electric_mpgge"],
            mpgge_dict["cd_fuel_mpgge"],
            mpgge_dict["cs_fuel_mpgge"],
        ]
    if vehicle.veh_pt_type == gl.BEV:
        mpgges = [mpgge_dict["grid_mpgge"]]
    if vehicle.veh_pt_type in [gl.HEV, gl.CONV]:
        mpgges = [mpgge_dict["mpgge"]]
    vehicle_segment_name = scenario.segmentName
    model_year = int(scenario.modelYear)
    region = scenario.region
    vocation = scenario.vocation

    # get age of vehicle
    # if age < 0: age = "*"
    # can ignore age, so always make it "*" - Kevin Bennion, 8/12/2019
    age = "*"

    fuels = scenario.fuel

    assert len(fuels) == len(mpgges), f"fuels/mpgges: {fuels}/{mpgges}"
    if (
        vehicle.veh_pt_type == gl.PHEV
    ):  # FIXME: this assumes the PHEV is plug-in hybrid electric with diesel. In future, scenario.fuel should be parsed to see if it is a electric/gasoline PHEV, for example.
        assert (
            "cd_electricity" in fuels[0]
        ), r'fuels for electric/diesel PHEVs must be of format: ["cd_electricity", "cd_diesel", "cs_diesel"]'
        assert (
            "cd_diesel" in fuels[1]
        ), r'fuels for electric/diesel PHEVs must be of format: ["cd_electricity", "cd_diesel", "cs_diesel"]'
        assert (
            "cs_diesel" in fuels[2]
        ), r'fuels for electric/diesel PHEVs must be of format: ["cd_electricity", "cd_diesel", "cs_diesel"]'

    data = []
    for fuel, mpgge in zip(fuels, mpgges):
        data.append(
            [model_year, region, vehicle_segment_name, vocation, fuel, mpgge, age]
        )
    fefdata = pd.DataFrame(
        data,
        columns=[
            "Model Year",
            "Region",
            "Vehicle",
            "Vocation",
            "Fuel",
            "Fuel Efficiency [mi/gge]",
            "Age [yr]",
        ],
    )

    return fefdata


def fill_veh_expense_file(scenario, cost_set):
    """
    This helper method generates a dataframe of MSRP breakdown costs as Cost [$/veh]

    Args:
        scenario (run_scenario.Scenario): Scenario object of current selection
        cost_set (dict): Dictionary containing MSRP breakdown cost components

    Returns:
        vexpdf (pd.DataFrame): Dataframe containing MSRP components costs as Cost [$/veh]
    """
    # read in scenario values needed, such as segment name, vocation, etc.
    vehicle = scenario.segmentName
    vocation = scenario.vocation
    model_year = int(scenario.modelYear)

    data = [
        [vehicle, vocation, model_year, cost_set["Glider"], "Glider"],
        [vehicle, vocation, model_year, cost_set["Fuel converter"], "Fuel converter"],
        [vehicle, vocation, model_year, cost_set["Fuel Storage"], "Fuel Storage"],
        [
            vehicle,
            vocation,
            model_year,
            cost_set["Motor & power electronics"],
            "Motor & power electronics",
        ],
        [vehicle, vocation, model_year, cost_set["Plug"], "Plug"],
        [vehicle, vocation, model_year, cost_set["Battery"], "Battery"],
        [
            vehicle,
            vocation,
            model_year,
            cost_set["Battery replacement"],
            "Battery replacement",
        ],
        [vehicle, vocation, model_year, cost_set["Purchase tax"], "Purchase tax"],
        # [vehicle, vocation, model_year, cost_set["Insurance"], "Insurance"],
        # [vehicle, vocation, model_year, cost_set["Residual Cost"], "Residual Cost"],
    ]
    vexpdf = pd.DataFrame(
        data, columns=["Vehicle", "Vocation", "Model Year", "Cost [$/veh]", "Category"]
    )

    return vexpdf


def fill_trav_exp_tsv(vehicle, scenario):
    """
    This helper method generates a dataframe containing maintenance costs in Cost [$/mi]

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object of analysis vehicle
        scenario (run_scenario.Scenario): Scenario object of current selection

    Returns:
        df (pd.DataFrame): Dataframe containing maintenance costs in Cost [$/mi]
    """

    columns = ["Year", "Region", "Vocation", "Vehicle", "Category", "Cost [$/mi]"]
    region = scenario.region
    vocation = scenario.vocation
    vehicle_name = scenario.segmentName
    maint = scenario.maintDolPerMi
    maint = list(np.float_(maint.strip(" ][").split(",")))
    veh_life_years = int(scenario.vehLifeYears)

    assert len(maint) == veh_life_years, (
        f"vehLifeYears of {veh_life_years} & length of input maintDolPerMi {len(maint)} do not align; "
        f"vehLifeYears life years & number of years in vmt should match\n"
        f"[vehLifeYears/[maintDolPerMi_1,...,maintDolPerMi_N]]:[{veh_life_years}/{maint}]"
    )
    data = []
    for i, yr in enumerate(
        range(int(scenario.modelYear), int(scenario.modelYear + veh_life_years))
    ):
        l1 = [yr, region, vocation, vehicle_name, "maintenance", maint[i]]
        data.append(l1)
        # data.append([yr, region, vocation, vehicle,  "payload opp cost", np.nan])
        # data.append([yr, region, vocation, vehicle,  "time opp cost",    np.nan])
        # data.append([yr, region, vocation, vehicle,  "labor opp cost",   np.nan])

    df = pd.DataFrame(data=data, columns=columns)

    return df


def fill_downtimelabor_cost_tsv(scenario, oppy_cost_set):
    """
    This helper method generates a dataframe containing fueling downtime and M&R downtime costs in Cost [$/Yr]

    Args:
        scenario (run_scenario.Scenario): Scenario object of current selection
        oppy_cost_set (dict): Dictionary containing dwell_time_cost_Dol and MR_downtime_cost_Dol

    Returns:
        df (pd.DataFrame): Dataframe containing fueling and MR downtime costs in Cost [$/Yr]
    """
    columns = ["Age [yr]", "Category", "Cost [$/Yr]"]
    data = []

    veh_life_years = int(scenario.vehLifeYears)

    dwell_time_cost_Dol = oppy_cost_set["dwell_time_cost_Dol"]
    MR_downtime_cost_Dol = oppy_cost_set["MR_downtime_cost_Dol"]
    # assert len(insurance_rates) >= veh_life_years, (f"vehLifeYears of {veh_life_years} & length of input insurance rates {len(insurance_rates)} do not align; "
    # f"vehLifeYears life years & number of years in vmt should match\n"
    # f"[vehLifeYears/[VMT_1,...,VMT_N]]:[{veh_life_years}/{insurance_rates}]")
    # \
    for i in range(0, veh_life_years):
        # downtime_costs_Dol = dwell_time_cost_Dol[i] + MR_downtime_cost_Dol[i]
        # i is age, give it a VMT value for each entry in VMT or defer to last VMT entry
        data.append([i, "fueling downtime cost", dwell_time_cost_Dol[i]])
        data.append([i, "MR downtime cost", MR_downtime_cost_Dol[i]])

    df = pd.DataFrame(data, columns=columns)

    # print(f'insurance: {df}')
    return df


def fill_market_share_tsv(scenario, num_vs=1):
    """
    This helper method generates a dataframe containing market share of current vehicle selection per vehicle sold

    Args:
        scenario (run_scenario.Scenario): Scenario object of current selection
        num_vs (int, optional): Number of vehicles. Defaults to 1.

    Returns:
        df (pd.DataFrame): Dataframe containing market share of current vehicle in Market Share [veh/veh]
    """

    vocation = scenario.vocation
    vehicle = scenario.segmentName
    reg = scenario.region

    veh_life_years = int(scenario.vehLifeYears)
    model_year = int(scenario.modelYear)
    # maint = list(np.float_(scenario.maintDolPerMi.strip('][').split(',')))
    data = []
    columns = ["Vehicle", "Vocation", "Model Year", "Region", "Market Share [veh/veh]"]
    data.append([vehicle, vocation, model_year, reg, 1 / num_vs])
    for yr in range(model_year + 1, model_year + veh_life_years):
        data.append([vehicle, vocation, yr, reg, 0])

    df = pd.DataFrame(data, columns=columns)

    return df


def fill_fuel_expense_tsv(vehicle, scenario):
    """
    This helper method generates a dataframe of fuel operating costs in Cost [$/gge]

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object of analysis vehicle
        scenario (run_scenario.Scenario): Scenario object of current selection

    Raises:
        Exception: Invalid fuel type

    Returns:
        df (pd.DataFrame): Dataframe containing fuel operating costs in Cost [$/gge]
    """

    fuels = scenario.fuel

    if vehicle.veh_pt_type in [gl.CONV, gl.HEV]:
        assert scenario.fuel[0].lower() in ["cng", "gasoline", "diesel", "hydrogen"]
    elif vehicle.veh_pt_type in [gl.BEV]:
        assert scenario.fuel[0].lower() in ["electricity"]
    elif vehicle.veh_pt_type == gl.PHEV:
        assert (
            "cd_electricity" in fuels[0]
        ), r'fuels must be of format: ["cd_electricity", "cd_diesel", "cs_diesel"]'
        assert (
            "cd_diesel" in fuels[1]
        ), r'fuels must be of format: ["cd_electricity", "cd_diesel", "cs_diesel"]'
        assert (
            "cs_diesel" in fuels[2]
        ), r'fuels must be of format: ["cd_electricity", "cd_diesel", "cs_diesel"]'

    veh_life_span = int(scenario.vehLifeYears)
    cat = "Fuel"
    columns = ["Year", "Fuel", "Category", "Cost [$/gge]"]
    data = []
    regdf = pd.read_csv(gl.REGIONAL_FUEL_PRICES_BY_TYPE_BY_YEAR)
    regdf = regdf.set_index("Fuel")
    for fuel in fuels:
        # cat = fuel
        for yr in range(
            int(scenario.modelYear), int(scenario.modelYear + veh_life_span)
        ):
            regdf = regdf[regdf["Region"] == scenario.region]
            # all costs are converted to $ per gallon gasoline equivalent
            # TODO, may want to be more explicit than just finding substrings
            if "diesel" in fuel.lower() and "bio" not in fuel.lower():
                dieselDolPerGal = regdf.loc["dieselDolPerGal", str(yr)]
                Dslgge = 1 * (33.7 / 37.95)
                cost = dieselDolPerGal * Dslgge
            elif "gasoline" in fuel.lower():
                gasolineDolPerGal = regdf.loc["gasolineDolPerGal", str(yr)]
                cost = gasolineDolPerGal
            elif "electricity" in fuel.lower():
                dolPerKwh = regdf.loc["dolPerKwh", str(yr)]
                cost = dolPerKwh * 33.7  # 33.41 kwh per gallon of gasoline
            elif fuel.lower() == "cng":
                CNGDolPerGge = regdf.loc["CNGDolPerGge", str(yr)]
                cost = CNGDolPerGge
            elif fuel.lower() == "hydrogen":
                hydrogenDolPerGGE = regdf.loc["hydrogenDolPerGGE", str(yr)]
                cost = hydrogenDolPerGGE
            else:
                raise Exception(
                    f"TCO fuel calc: fill_fuel_expense_tsv:: unknown fuel type {fuel}"
                )
            data.append([yr, fuel, cat, cost])

            # scenario.scenario_gge_regional_temporal_fuel_price += f"fuel: {fuel}; region: {scenario.region}; year: {yr}; $_gge: {cost}"

    df = pd.DataFrame(data, columns=columns)

    return df


def fill_annual_tsv(scenario):
    """
    This helper method generates a dataframe of annual vehicle miles traveled (VMT) - Annual Travel [mi/yr]

    Args:
        scenario (run_scenario.Scenario): Scenario object of current selection

    Returns:
        df (pd.DataFrame): Dataframe containing Annual Travel [mi/yr]
    """
    columns = ["Age [yr]", "Annual Travel [mi/yr]"]
    data = []

    veh_life_years = int(scenario.vehLifeYears)

    vmt = scenario.VMT
    assert len(vmt) == veh_life_years, (
        f"vehLifeYears of {veh_life_years} & length of input VMT {len(vmt)} do not align; "
        f"vehLifeYears life years & number of years in vmt should match\n"
        f"[vehLifeYears/[VMT_1,...,VMT_N]]:[{veh_life_years}/{vmt}]"
    )

    for i in range(0, veh_life_years):
        miles = vmt[i]
        # i is age, give it a VMT value for each entry in VMT or defer to last VMT entry
        data.append([i, miles])

    df = pd.DataFrame(data, columns=columns)

    return df


def fill_reg_sales_tsv(scenario, num_vs=1):
    """
    This helper method generates a dataframe containing vehicle sales per year - Sales [veh]

    Args:
        scenario (run_scenario.Scenario): Scenario object of current selection
        num_vs (int, optional): Number of vehicles. Defaults to 1.

    Returns:
        df (pd.DataFrame): Dataframe containing vehicle sales in Sales [veh]
    """
    veh_life_years = int(scenario.vehLifeYears)
    model_year = int(scenario.modelYear)
    reg = scenario.region

    columns = ["Model Year", "Region", "Sales [veh]"]
    data = []
    for yr in range(model_year, veh_life_years + model_year):
        if yr == model_year:
            data.append([yr, reg, num_vs])
        else:
            data.append([yr, reg, 0])

    df = pd.DataFrame(data, columns=columns)

    return df


def fill_insurance_tsv(scenario, veh_cost_set):
    """
    This helper method generates a dataframe containing vehicle insurance costs as Cost [$/Yr]

    Args:
        scenario (run_scenario.Scenario): Scenario object of current selection
        veh_cost_set (dict): Dictionary containing MSRP costs

    Returns:
        df (pd.DataFrame): Dataframe containing insurance costs in Cost [$/Yr]
    """
    columns = ["Age [yr]", "Category", "Cost [$/Yr]"]
    data = []

    veh_life_years = int(scenario.vehLifeYears)

    insurance_rates = scenario.insurance_rates_pctPerYr
    assert len(insurance_rates) >= veh_life_years, (
        f"vehLifeYears of {veh_life_years} & length of input insurance rates {len(insurance_rates)} do not align; "
        f"vehLifeYears life years & number of years in vmt should match\n"
        f"[vehLifeYears/[VMT_1,...,VMT_N]]:[{veh_life_years}/{insurance_rates}]"
    )

    MSRP = veh_cost_set["msrp"]
    for i in range(0, veh_life_years):
        insurance_costperyear = insurance_rates[i] * MSRP / 100
        # i is age, give it a VMT value for each entry in VMT or defer to last VMT entry
        data.append([i, "insurance", insurance_costperyear])

    df = pd.DataFrame(data, columns=columns)

    # print(f'insurance: {df}')
    return df


def fill_residual_cost_tsc(vehicle, scenario, veh_cost_set):
    """
    This helper method generates a dataframe of residual costs as Cost [$/Yr]

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object of analysis vehicle
        scenario (run_scenario.Scenario): Scenario object of current selection
        veh_cost_set (dict): Dictionary containing MSRP costs

    Returns:
        df (pd.DataFrame): Dataframe containing vehicle residual costs as Cost [$/Yr]
    """
    columns = ["Age [yr]", "Category", "Cost [$/Yr]"]
    data = []

    veh_life_years = int(scenario.vehLifeYears)

    residual_rate = find_residual_rates(vehicle, scenario)

    # assert len(insurance_rates) >= veh_life_years, (f"vehLifeYears of {veh_life_years} & length of input insurance rates {len(insurance_rates)} do not align; "
    # f"vehLifeYears life years & number of years in vmt should match\n"
    # f"[vehLifeYears/[VMT_1,...,VMT_N]]:[{veh_life_years}/{insurance_rates}]")

    MSRP = veh_cost_set["msrp"]
    for i in range(0, veh_life_years):
        if i == veh_life_years - 1:
            residual_cost = -residual_rate * MSRP
        else:
            residual_cost = 0
        data.append([i, "residual cost", residual_cost])

    df = pd.DataFrame(data, columns=columns)

    # print(f'residual: {df}')
    return df


def fill_survival_tsv(scenario, num_vs=1):
    """
    This helper method generates a dataframe containing surviving vehicles as Surviving Vehicles [veh/veh]

    Args:
        scenario (run_scenario.Scenario): Scenario object of current selection
        num_vs (int, optional): Number of vehicles. Defaults to 1.

    Returns:
        df (pd.DataFrame): Dataframe containing number of surviving vehicles on road in Surviving Vehicles [veh/veh]
    """

    columns = ["Age [yr]", "Surviving Vehicles [veh/veh]"]
    data = []
    veh_life_span = int(scenario.vehLifeYears)
    for yr in range(0, veh_life_span):
        data.append([yr, num_vs / num_vs])

    df = pd.DataFrame(data, columns=columns)

    return df


def fill_fuel_split_tsv(vehicle, scenario, mpgge):
    """
    This helper method generates a dataframe of fraction of travel in each fuel type as Fraction of Travel [mi/mi]

    Args:
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object of analysis vehicle
        scenario (run_scenario.Scenario): Scenario object of current selection
        mpgge (dict): MPGGE dictionary from fueleconomy.get_mpgge()

    Returns:
        df (pd.DataFrame): Dataframe containing fraction of travel in each fuel type as Fraction of Travel [mi/mi]
    """
    columns = ["Vehicle", "Fuel", "Vocation", "Fraction of Travel [mi/mi]"]
    vocation = scenario.vocation
    vehicle_segment = scenario.segmentName
    fuels = scenario.fuel

    if vehicle.veh_pt_type == gl.PHEV:
        uf = run_scenario.get_phev_util_factor(scenario, vehicle, mpgge)

    if vehicle.veh_pt_type != gl.PHEV:
        frac_time_traveled_mi_mi = 1
        data = [[vehicle_segment, fuels[0], vocation, frac_time_traveled_mi_mi]]
    else:
        data = [
            [vehicle_segment, fuels[0], vocation, uf],  # cd_electricity
            [vehicle_segment, fuels[1], vocation, uf],  # cd_diesel
            [vehicle_segment, fuels[2], vocation, 1 - uf],  # cs_diesel
        ]

    df = pd.DataFrame(data, columns=columns)

    return df
