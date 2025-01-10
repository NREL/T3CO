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
    purchasing_payment_dol_per_yr: float = None
    purchasing_interest_cost_dol_per_yr: float = None
    purchasing_remaining_principal_dol: float = None
    fueling_dwell_labor_cost_dol_per_yr: float = None
    net_oper_cost_dol_per_yr: float = None
    disc_oper_cost_dol_per_yr: float = None

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the OperatingCosts class.
        """
        instance = super(OperatingCosts, cls).__new__(cls)
        return instance
    
    def __init__(
        self,
        year_number: int,
        cap_costs: CapitalCosts,
        vehicle: Vehicle,
        scenario: Scenario,
        energy: Energy = None,
        oppy_costs: OpportunityCosts = None,
    ):
        """
        Initializes the OperatingCosts instance.

        Args:
            year_number (int): The year number for which the operating costs are calculated.
            cap_costs (CapitalCosts): The capital costs associated with the vehicle.
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
            energy (Energy): The energy model instance.
            oppy_costs (OpportunityCosts): The opportunity costs associated with the vehicle.
        """
        if energy: self.mpgge = energy.mpgge
        self.distance_traveled_mi_per_yr = scenario.vmt[year_number - 1]

        self.set_fuel_cost(year_number=year_number, vehicle=vehicle, scenario=scenario)
        self.set_maintenance_oper_cost(year_number=year_number, vehicle=vehicle, scenario=scenario)
        self.set_insurance_cost(year_number=year_number, cap_cost=cap_costs, vehicle=vehicle, scenario=scenario)

        if scenario.activate_tco_fueling_dwell_time_cost and oppy_costs:
            self.set_fueling_dwell_labor_cost(scenario=scenario, oppy_costs=oppy_costs)
        else:
            self.fueling_dwell_labor_cost_dol_per_yr = 0.0

        self.set_purchasing_payment_cost(year_number=year_number, scenario=scenario, cap_costs=cap_costs)
        self.set_net_oper_cost()
        self.set_disc_oper_cost(year_number=year_number, scenario=scenario)

    def set_fuel_cost(self, year_number: int, vehicle: Vehicle, scenario: Scenario) -> None:
        """
        Sets the fuel cost for the given year.

        Args:
            year_number (int): The year number for which the fuel cost is calculated.
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
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
            print(scenario.fuel_prices_df)
            dolPerKwh = scenario.fuel_prices_df.loc[
                "dolPerKwh", str(scenario.model_year + year_number - 1)
            ]
            self.fuel_price_dol_per_gge = (
                dolPerKwh * gl.KWH_PER_GGE
            )  
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
    ) -> None:
        """
        Sets the maintenance operating cost for the given year.

        Args:
            year_number (int): The year number for which the maintenance cost is calculated.
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
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
    ) -> None:
        """
        Sets the insurance cost for the given year.

        Args:
            year_number (int): The year number for which the insurance cost is calculated.
            cap_cost (CapitalCosts): The capital costs associated with the vehicle.
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        self.insurance_rates_pct_per_yr = (
            ast.literal_eval(
            scenario.insurance_rates_pct_per_yr
            )[year_number - 1] if isinstance(scenario.insurance_rates_pct_per_yr, str) else scenario.insurance_rates_pct_per_yr[year_number - 1]
        )

        self.insurance_cost_dol_per_yr = (
            cap_cost.msrp_total_dol * self.insurance_rates_pct_per_yr
        )

    def set_purchasing_payment_cost(self, year_number: int, scenario: Scenario, cap_costs: CapitalCosts):
        if scenario.purchasing_method.lower() in ['cash', 'upfront', 'fullpayment']:
            self.purchasing_payment_dol_per_yr = 0
            self.purchasing_interest_cost_dol_per_yr = 0
            
        elif scenario.purchasing_method.lower() in ['financing', 'loan']:
            interest_rate_pct_per_frequency = scenario.financing_interest_rate_pct_per_yr/12*scenario.financing_payment_frequency_months
            loan_amount_dol = (cap_costs.msrp_total_dol + cap_costs.purchase_tax_dol) * (1 - scenario.financing_down_payment_pct)
            total_number_of_payments = int(scenario.financing_tenure_yr * 12 /scenario.financing_payment_frequency_months) #TODO check for missing payment
            annual_number_of_payments = int(12/scenario.financing_payment_frequency_months)
            purchasing_payment_dol_per_freq = (
                (
                loan_amount_dol
                * interest_rate_pct_per_frequency * (1 + interest_rate_pct_per_frequency) ** total_number_of_payments)
                /(
                (1 + interest_rate_pct_per_frequency) ** total_number_of_payments - 1)
            )
            self.purchasing_remaining_principal_dol = (
                 (loan_amount_dol * (1 + interest_rate_pct_per_frequency)** (year_number * annual_number_of_payments))
                - purchasing_payment_dol_per_freq / interest_rate_pct_per_frequency *((1+interest_rate_pct_per_frequency)**(year_number * annual_number_of_payments) - 1)
            )
            self.purchasing_interest_cost_dol_per_yr  =  sum([interest_rate_pct_per_frequency * (loan_amount_dol * (1 + interest_rate_pct_per_frequency)**n - purchasing_payment_dol_per_freq / interest_rate_pct_per_frequency *((1+interest_rate_pct_per_frequency)**n - 1))
                                            for n in range((year_number-1)*annual_number_of_payments, (year_number * annual_number_of_payments + 1))])
            
            self.purchasing_payment_dol_per_yr = (
                purchasing_payment_dol_per_freq * int(12 / scenario.financing_payment_frequency_months)
            )


    def set_fueling_dwell_labor_cost(
        self, scenario: Scenario, oppy_costs: OpportunityCosts
    ) -> None:
        """
        Sets the fueling dwell labor cost for the given year.

        Args:
            scenario (Scenario): The scenario instance containing configuration data.
            oppy_costs (OpportunityCosts): The opportunity costs associated with the vehicle.
        """
        self.fueling_dwell_labor_cost_dol_per_yr = (
            oppy_costs.fueling_dwell_time_hr_per_yr * scenario.labor_rate_dol_per_hr
        )

    def set_net_oper_cost(self) -> None:
        """
        Sets the net operating cost for the given year.
        """
        self.net_oper_cost_dol_per_yr = (
            self.fuel_cost_dol_per_yr
            + self.fueling_dwell_labor_cost_dol_per_yr
            + self.maintenance_cost_dol_per_yr
            + self.insurance_cost_dol_per_yr
            + self.purchasing_interest_cost_dol_per_yr
        )

    def set_disc_oper_cost(self, year_number: int, scenario: Scenario) -> None:
        """
        Sets the discounted operating cost for the given year.

        Args:
            year_number (int): The year number for which the discounted operating cost is calculated.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        self.disc_oper_cost_dol_per_yr = scenario.get_discounted_value(value=self.net_oper_cost_dol_per_yr, year_number=year_number)

    def __str__(self) -> str:
        """
        Returns a string representation of the OperatingCosts instance.

        Returns:
            str: String representation of the OperatingCosts instance.
        """
        return obj_to_string(self)