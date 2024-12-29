import numpy as np
import pandas as pd

from t3co.constants import Global as gl
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle


class CapitalCosts:
    glider_cost_dol: float = np.nan
    fuel_converter_cost_dol: float = np.nan
    fuel_storage_cost_dol: float = np.nan
    motor_control_power_elecs_cost_dol: float = np.nan
    plug_cost_dol: float = np.nan
    battery_cost_dol: float = np.nan
    purchase_tax_dol: float = np.nan
    msrp_total_dol: float = np.nan
    residual_cost_dol: float = np.nan

    def __init__(self, vehicle: Vehicle, scenario: Scenario):
        self.set_glider_cost(vehicle, scenario)
        self.set_fuel_converter_cost_dol(vehicle, scenario)
        self.set_fuel_storage_cost(vehicle, scenario)
        self.set_motor_control_power_elecs_cost(vehicle, scenario)
        self.set_plug_cost(vehicle, scenario)
        self.set_battery_cost(vehicle, scenario)
        self.set_msrp(vehicle, scenario)
        self.set_purchase_tax(vehicle, scenario)
        self.set_residual_cost(vehicle, scenario)
        

    def set_glider_cost(self, vehicle: Vehicle, scenario: Scenario):
        self.glider_cost_dol = scenario.vehicle_glider_cost_dol

    def set_fuel_converter_cost_dol(self, vehicle: Vehicle, scenario: Scenario):
        if vehicle.veh_pt_type == gl.BEV or vehicle.fc_max_kw == 0:
            self.fuel_converter_cost_dol = 0

        elif vehicle.veh_pt_type == gl.HEV:
            self.fuel_converter_cost_dol = (
                scenario.fc_fuelcell_cost_dol_per_kw * vehicle.fc_max_kw
            )

        elif vehicle.veh_pt_type == gl.CONV:
            self.fuel_converter_cost_dol = (
                scenario.fc_cng_ice_cost_dol_per_kw * vehicle.fc_max_kw
            ) + scenario.fc_ice_base_cost_dol

        else:
            self.fuel_converter_cost_dol = (
                scenario.fc_ice_cost_dol_per_kw * vehicle.fc_max_kw
            ) + scenario.fc_ice_base_cost_dol

        self.fuel_converter_cost_dol *= (
            scenario.markup_pct if scenario.markup_pct else 1
        )

    def set_fuel_storage_cost(self, vehicle: Vehicle, scenario: Scenario):
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
            self.fuel_storage_cost_dol = (
                0  # TODO test that there are no other fuel types
            )
        self.fuel_storage_cost_dol *= scenario.markup_pct if scenario.markup_pct else 1

    def set_motor_control_power_elecs_cost(self, vehicle: Vehicle, scenario: Scenario):
        if vehicle.mc_max_kw == 0 or vehicle.mc_max_kw is None:
            self.motor_control_power_elecs_cost_dol = 0
        else:
            self.motor_control_power_elecs_cost_dol = scenario.pe_mc_base_cost_dol + (
                scenario.pe_mc_cost_dol_per_kw * vehicle.mc_max_kw
            )
        vehicle.mc_max_kw *= scenario.markup_pct if scenario.markup_pct else 1

    def set_plug_cost(self, vehicle: Vehicle, scenario: Scenario):
        if vehicle.veh_pt_type in [gl.PHEV, gl.BEV, gl.HEV] and vehicle.has_plugin:
            self.plug_cost_dol = scenario.plug_base_cost_dol
        else:
            self.plug_cost_dol = 0
        self.plug_cost_dol *= scenario.markup_pct if scenario.markup_pct else 1

    def set_battery_cost(self, vehicle: Vehicle, scenario: Scenario):
        if vehicle.ess_max_kwh == 0:
            self.battery_cost_dol = 0
        else:
            self.battery_cost_dol = scenario.ess_base_cost_dol + (
                scenario.ess_cost_dol_per_kwh * vehicle.ess_max_kwh
            )
        self.battery_cost_dol *= scenario.markup_pct if scenario.markup_pct else 1

    def set_msrp(self, vehicle: Vehicle, scenario: Scenario):
        self.msrp_total_dol = (
            self.glider_cost_dol
            + self.fuel_storage_cost_dol
            + self.fuel_converter_cost_dol
            + self.motor_control_power_elecs_cost_dol
            + self.battery_cost_dol
            + self.plug_cost_dol
        )

    def set_purchase_tax(self, vehicle: Vehicle, scenario: Scenario):
        self.purchase_tax_dol = self.msrp_total_dol * scenario.tax_rate_pct

    def set_residual_cost(self, vehicle: Vehicle, scenario: Scenario):
        residual_rates_all = pd.read_csv(scenario.residual_rates_file)
        vehicle_class = scenario.vehicle_class
        powertrain_type = vehicle.veh_pt_type.lower()
        year = str(scenario.vehicle_life_yr)
        scenario.residual_rate_pct = residual_rates_all.loc[
            (residual_rates_all["VehicleClass"].str.lower() == vehicle_class)
            & (residual_rates_all["PowertrainType"].str.lower() == powertrain_type)
        ][year].values[0]

        self.residual_cost_dol = -self.msrp_total_dol * scenario.residual_rate_pct
