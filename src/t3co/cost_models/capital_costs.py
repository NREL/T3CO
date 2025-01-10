from pathlib import Path

import numpy as np
import pandas as pd

from t3co.constants import Global as gl
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle


class CapitalCosts:
    glider_cost_dol: float = 0.0
    fuel_converter_cost_dol: float = 0.0
    fuel_storage_cost_dol: float = 0.0
    motor_control_power_elecs_cost_dol: float = 0.0
    plug_cost_dol: float = 0.0
    battery_cost_dol: float = 0.0
    purchase_tax_dol: float = 0.0
    msrp_total_dol: float = 0.0
    residual_cost_dol: float = 0.0
    purchasing_downpayment_dol: float = 0.0
    purchasing_initial_principal_dol: float = 0.0
    net_capital_cost_dol: float = None
    disc_residual_cost_dol: float = None

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the CapitalCosts class.
        """
        instance = super(CapitalCosts, cls).__new__(cls)
        return instance
    
    def __init__(self, vehicle: Vehicle, scenario: Scenario):
        """
        Initializes the CapitalCosts instance.

        Args:
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        self.set_glider_cost(vehicle=vehicle, scenario=scenario)
        self.set_fuel_converter_cost_dol(vehicle=vehicle, scenario=scenario)
        self.set_fuel_storage_cost(vehicle=vehicle, scenario=scenario)
        self.set_motor_control_power_elecs_cost(vehicle=vehicle, scenario=scenario)
        self.set_plug_cost(vehicle=vehicle, scenario=scenario)
        self.set_battery_cost(vehicle=vehicle, scenario=scenario)
        self.set_msrp(vehicle=vehicle, scenario=scenario)
        self.set_purchase_tax(vehicle=vehicle, scenario=scenario)
        self.set_downpayment(vehicle=vehicle, scenario=scenario)
        self.set_residual_cost(vehicle=vehicle, scenario=scenario)
        self.set_disc_residual_cost(scenario=scenario)
        self.set_total_cap_cost()

    def set_glider_cost(self, vehicle: Vehicle, scenario: Scenario) -> None:
        """
        Sets the glider cost for the vehicle.

        Args:
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        self.glider_cost_dol = scenario.vehicle_glider_cost_dol

    def set_fuel_converter_cost_dol(self, vehicle: Vehicle, scenario: Scenario) -> None:
        """
        Sets the fuel converter cost for the vehicle.

        Args:
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        if vehicle.veh_pt_type == gl.BEV or vehicle.fc_max_kw == 0:
            self.fuel_converter_cost_dol = 0
        elif vehicle.veh_pt_type == gl.HEV:
            self.fuel_converter_cost_dol = (
                scenario.fc_fuelcell_cost_dol_per_kw * vehicle.fc_max_kw
            )
        elif vehicle.veh_pt_type == gl.CONV and scenario.fuel_type == "cng":
            self.fuel_converter_cost_dol = (
                scenario.fc_cng_ice_cost_dol_per_kw * vehicle.fc_max_kw
            ) + scenario.fc_ice_base_cost_dol
        else:
            self.fuel_converter_cost_dol = (
                scenario.fc_ice_cost_dol_per_kw * vehicle.fc_max_kw
            ) + scenario.fc_ice_base_cost_dol

        self.fuel_converter_cost_dol = self.get_marked_up_value(self.fuel_converter_cost_dol, scenario)

    def set_fuel_storage_cost(self, vehicle: Vehicle, scenario: Scenario) -> None:
        """
        Sets the fuel storage cost for the vehicle.

        Args:
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        if vehicle.veh_pt_type == gl.BEV:
            self.fuel_storage_cost_dol = 0
        elif vehicle.veh_pt_type == gl.HEV and scenario.fuel_type[0] == "hydrogen":
            self.fuel_storage_cost_dol = (
                scenario.fs_h2_cost_dol_per_kwh * vehicle.fs_kwh
            )
        elif (
            vehicle.veh_pt_type in [gl.CONV, gl.HEV, gl.PHEV]
            and scenario.fuel_type[0] == "cng"
        ):
            self.fuel_storage_cost_dol = (
                scenario.fs_cng_cost_dol_per_kwh * vehicle.fs_kwh
            )
        elif vehicle.veh_pt_type in [gl.CONV, gl.HEV, gl.PHEV]:
            self.fuel_storage_cost_dol = scenario.fs_cost_dol_per_kwh * vehicle.fs_kwh
        else:
            self.fuel_storage_cost_dol = 0

        self.fuel_storage_cost_dol = self.get_marked_up_value(self.fuel_storage_cost_dol, scenario)

    def set_motor_control_power_elecs_cost(self, vehicle: Vehicle, scenario: Scenario) -> None:
        """
        Sets the motor control and power electronics cost for the vehicle.

        Args:
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        if vehicle.mc_max_kw == 0 or vehicle.mc_max_kw is None:
            self.motor_control_power_elecs_cost_dol = 0
        else:
            self.motor_control_power_elecs_cost_dol = scenario.pe_mc_base_cost_dol + (
                scenario.pe_mc_cost_dol_per_kw * vehicle.mc_max_kw
            )
        self.motor_control_power_elecs_cost_dol = self.get_marked_up_value(self.motor_control_power_elecs_cost_dol, scenario)

    def set_plug_cost(self, vehicle: Vehicle, scenario: Scenario) -> None:
        """
        Sets the plug cost for the vehicle.

        Args:
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        if vehicle.veh_pt_type in [gl.PHEV, gl.BEV, gl.HEV] and vehicle.chg_eff:
            self.plug_cost_dol = scenario.plug_base_cost_dol
        else:
            self.plug_cost_dol = 0

        self.plug_cost_dol = self.get_marked_up_value(self.plug_cost_dol, scenario)

    def set_battery_cost(self, vehicle: Vehicle, scenario: Scenario) -> None:
        """
        Sets the battery cost for the vehicle.

        Args:
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        if vehicle.ess_max_kwh == 0:
            self.battery_cost_dol = 0
        else:
            self.battery_cost_dol = scenario.ess_base_cost_dol + (
                scenario.ess_cost_dol_per_kwh * vehicle.ess_max_kwh
            )

        self.battery_cost_dol = self.get_marked_up_value(self.battery_cost_dol, scenario)

    def set_msrp(self, vehicle: Vehicle, scenario: Scenario) -> None:
        """
        Sets the Manufacturer's Suggested Retail Price (MSRP) for the vehicle.

        Args:
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        self.msrp_total_dol = (
            self.glider_cost_dol
            + self.fuel_storage_cost_dol
            + self.fuel_converter_cost_dol
            + self.motor_control_power_elecs_cost_dol
            + self.battery_cost_dol
            + self.plug_cost_dol
        )

    def set_purchase_tax(self, vehicle: Vehicle, scenario: Scenario) -> None:
        """
        Sets the purchase tax for the vehicle.

        Args:
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        self.purchase_tax_dol = self.msrp_total_dol * scenario.tax_rate_pct

    def set_downpayment(self, vehicle: Vehicle, scenario: Scenario) -> None:
        if scenario.purchasing_method =='cash':
            self.purchasing_downpayment_dol = self.msrp_total_dol + self.purchase_tax_dol
            self.purchasing_initial_principal_dol = 0.0

        elif scenario.purchasing_method == 'loan':
            self.purchasing_downpayment_dol = (self.msrp_total_dol + self.purchase_tax_dol) * scenario.purchasing_down_payment_pct
            self.purchasing_initial_principal_dol = (self.msrp_total_dol + self.purchase_tax_dol) * (1 - scenario.purchasing_down_payment_pct)
        
        elif scenario.purchasing_method == 'lease':
            scenario.leasing_money_factor = scenario.purchasing_interest_rate_pct_per_yr/24
            self.purchasing_downpayment_dol = (self.msrp_total_dol + self.purchase_tax_dol) * scenario.purchasing_down_payment_pct
            self.purchasing_initial_principal_dol = 0.0

    def set_residual_cost(self, vehicle: Vehicle, scenario: Scenario) -> None:
        """
        Sets the residual cost for the vehicle.

        Args:
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        
        scenario.residual_rate_pct *= np.prod([(1-scenario.depreciation_rates_pct_per_yr[i]) for i in range(scenario.vehicle_life_yr)])
        self.residual_cost_dol = - self.msrp_total_dol * scenario.residual_rate_pct

    def set_total_cap_cost(self) -> None:
        """
        Sets the total capital cost for the vehicle.
        """
        self.net_capital_cost_dol = self.purchasing_downpayment_dol

    def set_disc_residual_cost(self, scenario: Scenario) -> None:
        """
        Sets the discounted residual cost for the vehicle.

        Args:
            scenario (Scenario): The scenario instance containing configuration data.
        """
        self.disc_residual_cost_dol = scenario.get_discounted_value(self.residual_cost_dol, year_number=scenario.vehicle_life_yr)

    def get_marked_up_value(self, value: float, scenario: Scenario) -> float:
        """
        Returns the marked up value.

        Args:
            value (float): The value to mark up.
            scenario (Scenario): The scenario instance containing configuration data.

        Returns:
            float: The marked up value.
        """
        return value * (1+ scenario.markup_pct if scenario.markup_pct else 1)