import ast
from pathlib import Path

import pandas as pd

from t3co.constants import Global as gl
from t3co.cost_models.capital_costs import CapitalCosts
from t3co.cost_models.opportunity_costs import OpportunityCosts
from t3co.energy_models.energy import Energy
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle
from t3co.utils.print_class_objects import obj_to_string


class OperatingCosts:
    fuel_cost_dol_per_yr: float = None
    fuel_price_dol_per_gge: float = None
    fuel_used_gal_gge_per_yr: float = None
    fuel_used_gal_gde_per_yr: float = None
    energy_used_kwh_per_yr: float = None
    maintenance_cost_dol_per_yr: float = None
    maintenance_cost_dol_per_mi: float = None
    insurance_cost_dol_per_yr: float = None
    distance_traveled_mi_per_yr: float = None
    fueling_dwell_labor_cost_dol_per_yr: float = None
    net_oper_cost_dol_per_yr: float = None
    disc_oper_cost_dol_per_yr: float = None

    def __init__(
        self,
        year_number: int,
        cap_costs: CapitalCosts,
        vehicle: Vehicle,
        scenario: Scenario,
        energy: Energy,
        oppy_costs: OpportunityCosts,
    ):
        self.mpgge = energy.mpgge
        self.distance_traveled_mi_per_yr = scenario.vmt[year_number - 1]

        self.set_fuel_cost(year_number=year_number, vehicle=vehicle, scenario=scenario)
        self.set_maintenance_oper_cost(year_number=year_number, vehicle=vehicle, scenario=scenario)
        self.set_insurance_cost(year_number=year_number, cap_cost=cap_costs, vehicle=vehicle, scenario=scenario)

        if scenario.activate_tco_fueling_dwell_time_cost and oppy_costs:
            self.set_fueling_dwell_labor_cost(scenario=scenario, oppy_costs=oppy_costs)

        self.set_net_oper_cost()
        self.set_disc_oper_cost(year_number=year_number, scenario=scenario)

    def set_fuel_cost(self, year_number: int, vehicle: Vehicle, scenario: Scenario):
        if scenario.fuel_prices_df is None:
            scenario.fuel_prices_df = pd.read_csv(
                (
                    Path(scenario.fuel_prices_file)
                    if Path(scenario.fuel_prices_file).is_absolute()
                    else gl.RESOURCES_FOLDERPATH / scenario.fuel_prices_file
                )
            )
            scenario.fuel_prices_df.set_index("Fuel", inplace=True)
            
        scenario.fuel_prices_df = scenario.fuel_prices_df[scenario.fuel_prices_df["Region"] == scenario.region]

        if (
            "diesel" in scenario.fuel_type.lower()
            and "bio" not in scenario.fuel_type.lower()
        ):
            dieselDolPerGal = scenario.fuel_prices_df.loc[
                "dieselDolPerGal", str(scenario.model_year + year_number - 1)
            ]
            self.fuel_price_dol_per_gge = dieselDolPerGal * gl.DGE_TO_GGE
        elif "gasoline" in scenario.fuel_type.lower():
            gasolineDolPerGal = scenario.fuel_prices_df.loc[
                "gasolineDolPerGal", str(scenario.model_year + year_number - 1)
            ]
            self.fuel_price_dol_per_gge = gasolineDolPerGal
        elif "electricity" in scenario.fuel_type.lower():
            dolPerKwh = scenario.fuel_prices_df.loc[
                "dolPerKwh", str(scenario.model_year + year_number - 1)
            ]
            self.fuel_price_dol_per_gge = (
                dolPerKwh * gl.KWH_PER_GGE
            )  # 33.41 kwh per gallon of gasoline
        elif scenario.fuel_type.lower() == "cng":
            CNGDolPerGge = scenario.fuel_prices_df.loc[
                "CNGDolPerGge", str(scenario.model_year + year_number - 1)
            ]
            self.fuel_price_dol_per_gge = CNGDolPerGge
        elif scenario.fuel_type.lower() == "hydrogen":
            hydrogenDolPerGGE = scenario.fuel_prices_df.loc[
                "hydrogenDolPerGGE", str(scenario.model_year + year_number - 1)
            ]
            self.fuel_price_dol_per_gge = hydrogenDolPerGGE
        else:
            raise Exception(f"Operating Costs calculation: Unknown fuel type {scenario.fuel_type}")

        self.fuel_used_gal_gge_per_yr = self.distance_traveled_mi_per_yr / self.mpgge
        self.fuel_used_gal_gde_per_yr = self.fuel_used_gal_gge_per_yr / gl.DGE_TO_GGE
        self.energy_used_kwh_per_yr = self.fuel_used_gal_gge_per_yr * gl.KWH_PER_GGE

        self.fuel_cost_dol_per_yr = (
            self.fuel_price_dol_per_gge * self.fuel_used_gal_gge_per_yr
        )

    def set_maintenance_oper_cost(
        self, year_number: int, vehicle: Vehicle, scenario: Scenario
    ):
        self.maintenance_cost_dol_per_mi = scenario.maint_oper_cost_dol_per_mi[
            year_number - 1
        ]

        self.maintenance_cost_dol_per_yr = (
            self.maintenance_cost_dol_per_mi * self.distance_traveled_mi_per_yr
        )

    def set_insurance_cost(
        self,
        year_number: int,
        cap_cost: CapitalCosts,
        vehicle: Vehicle,
        scenario: Scenario,
    ):
        self.insurance_rate_per_yr = ast.literal_eval(
            scenario.insurance_rates_pct_per_yr
        )[year_number - 1]
        self.insurance_cost_dol_per_yr = (
            cap_cost.msrp_total_dol * self.insurance_rate_per_yr
        )

    def set_fueling_dwell_labor_cost(
        self, scenario: Scenario, oppy_costs: OpportunityCosts
    ):
        self.fueling_dwell_labor_cost_dol_per_yr = (
            oppy_costs.fueling_dwell_time_hr_per_yr * scenario.labor_rate_dol_per_hr
        )

    def set_net_oper_cost(self):
        self.net_oper_cost_dol_per_yr = (
            self.fuel_cost_dol_per_yr
            + self.fueling_dwell_labor_cost_dol_per_yr
            + self.maintenance_cost_dol_per_yr
            + self.insurance_cost_dol_per_yr
        )

    def set_disc_oper_cost(self, year_number: int, scenario: Scenario):
        self.disc_oper_cost_dol_per_yr = scenario.get_discounted_value(value=self.net_oper_cost_dol_per_yr, year_number=year_number)

    def __str__(self):
        return obj_to_string(self)
