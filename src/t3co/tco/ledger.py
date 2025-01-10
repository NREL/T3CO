import json
from pathlib import Path
from typing import Union
import numpy as np
import pandas as pd
from t3co.constants import Global as gl
from t3co.energy_models.energy import Energy
from t3co.input_data.config import Config
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle
from t3co.tco.tcocalc import TCOCalc
from t3co.utils.print_class_objects import (
    custom_default,
    handle_nan,
    obj_to_string,
    to_flat_dict,
)


class Ledger:
    selection: Union[int, str] = None
    scenario_name: str = ""
    discounted_tco_dol: float = None
    vehicle_life_yr: int = None
    tco_method: str = "DIRECT"
    tco_per_year: list[TCOCalc] = []
    discounted_total_cap_cost_dol: float = 0.0
    discounted_total_oper_cost_dol: float = 0.0
    discounted_downtime_oppy_cost_dol: float = 0.0
    cumu_disc_tco_dol_per_yr: list[float] = []
    cumu_tco_dol_per_mi: list[float] = []
    cumu_levelized_tco_dol_per_mi: list[float] = []
    total_vmt: float = 0.0
    disc_total_vmt: float = 0.0

    glider_cost_dol: float = 0.0
    fuel_converter_cost_dol: float = 0.0
    fuel_storage_cost_dol: float = 0.0
    motor_control_power_elecs_cost_dol: float = 0.0
    plug_cost_dol: float = 0.0
    battery_cost_dol: float = 0.0
    purchase_tax_dol: float = 0.0
    msrp_total_dol: float = 0.0
    total_fuel_cost_dol: float = 0.0
    total_maintenance_cost_dol: float = 0.0
    total_fuel_used_gal_ge: float = 0.0
    total_fuel_used_gal_de: float = 0.0
    total_purchasing_interest_cost_dol: float = 0.0
    mpgge: float = 0.0
    grid_mpgge: float = 0.0
    mpgde: float = 0.0
    kwh_per_mi: float = 0.0
    payload_cap_cost_multiplier: float = 1.0
    total_fueling_dwell_time_hr: float = 0.0
    total_mr_downtime_hr: float = 0.0
    total_downtime_hr: float = 0.0
    fueling_dwell_labor_cost_dol: float = 0.0
    fueling_downtime_oppy_cost_dol: float = 0.0
    mr_downtime_oppy_cost_dol: float = 0.0
    discounted_downtime_oppy_cost_dol: float = 0.0
    payload_capacity_cost_dol: float = 0.0
    insurance_cost_dol: float = 0.0
    residual_cost_dol: float = 0.0

    scenario: Scenario = None
    vehicle: Vehicle = None
    config: Config = None
    energy: Energy = None

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the Ledger class.
        """
        instance = super(Ledger, cls).__new__(cls)
        return instance
    
    def __init__(
        self,
        vehicle: Vehicle,
        scenario: Scenario,
        energy: Energy = None,
        config: Config = None,
    ):
        """
        Initializes the Ledger instance.

        Args:
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance.
            energy (Energy, optional): The energy instance. Defaults to None.
            config (Config, optional): The configuration instance. Defaults to None.
        """
        self.scenario = scenario
        self.vehicle = vehicle
        self.selection = scenario.selection
        self.scenario_name = scenario.scenario_name

        self.tco_per_year = []
        if config:
            self.config = config
            self.vehicle_life_yr = config.vehicle_life_yr
            self.tco_method = config.TCO_method
        else:
            self.vehicle_life_yr = scenario.vehicle_life_yr
            self.tco_method = "DIRECT"

        if energy:
            self.energy = energy

        for year_index in range(self.vehicle_life_yr):
            self.tco_per_year.append(
                TCOCalc(
                    year_index=year_index,
                    vehicle=self.vehicle,
                    scenario=self.scenario,
                    energy=self.energy,
                    cap_costs=(
                        self.tco_per_year[year_index - 1].cap_costs_dol
                        if year_index
                        else None
                    ),
                    payload_cap_cost_multiplier=(
                        self.tco_per_year[
                            year_index - 1
                        ].oppy_costs_dol.payload_cap_cost_multiplier
                        if year_index
                        else None
                    ),
                )
            )

        self.set_cost_components()
        self.set_discounted_costs()
        self.set_discounted_tco()

    def set_discounted_costs(self):
        """
        Sets the discounted cost components for the Ledger instance.
        """
        self.payload_cap_cost_multiplier = self.tco_per_year[
            0
        ].oppy_costs_dol.payload_cap_cost_multiplier
        self.discounted_total_cap_cost_dol = self.tco_per_year[
            0
        ].cap_costs_dol.net_capital_cost_dol

        self.total_vmt, self.disc_total_vmt = 0.0, 0.0
        for year_index in range(self.vehicle_life_yr):
            self.discounted_total_oper_cost_dol += self.tco_per_year[
                year_index
            ].oper_costs_dol.disc_oper_cost_dol_per_yr
            self.discounted_downtime_oppy_cost_dol += self.tco_per_year[
                year_index
            ].oppy_costs_dol.disc_downtime_oppy_cost_dol
            self.total_vmt += self.scenario.vmt[year_index]
            self.disc_total_vmt += self.scenario.get_discounted_value(
                self.scenario.vmt[year_index], year_number=year_index + 1
            )
            self.cumu_disc_tco_dol_per_yr.append(
                (self.cumu_disc_tco_dol_per_yr[year_index - 1] if year_index else 0)
                + (self.discounted_total_cap_cost_dol if year_index == 0 else 0)
                + self.discounted_total_oper_cost_dol
                + self.discounted_downtime_oppy_cost_dol
                + (
                    self.tco_per_year[year_index].cap_costs_dol.disc_residual_cost_dol
                    if year_index == self.scenario.vehicle_life_yr
                    else 0
                )
            )

            self.cumu_tco_dol_per_mi.append(
                self.cumu_disc_tco_dol_per_yr[year_index] / self.total_vmt
            )

            self.cumu_levelized_tco_dol_per_mi.append(
                self.cumu_disc_tco_dol_per_yr[year_index] / self.disc_total_vmt
            )        

        self.total_fuel_cost_dol = sum(
            self.scenario.get_discounted_value(
                self.tco_per_year[year_index].oper_costs_dol.fuel_cost_dol_per_yr,
                year_number=year_index + 1,
            )
            for year_index in range(self.vehicle_life_yr)
        )

        self.total_maintenance_cost_dol = sum(
            self.scenario.get_discounted_value(
                self.tco_per_year[
                    year_index
                ].oper_costs_dol.maintenance_cost_dol_per_yr,
                year_number=year_index + 1,
            )
            for year_index in range(self.vehicle_life_yr)
        )
        self.total_purchasing_interest_cost_dol = sum(
            self.scenario.get_discounted_value(
                (
                    self.tco_per_year[
                    year_index
                ].oper_costs_dol.purchasing_interest_cost_dol_per_yr if self.tco_per_year[
                    year_index
                ].oper_costs_dol.purchasing_interest_cost_dol_per_yr
                else self.tco_per_year[
                    year_index
                ].oper_costs_dol.purchasing_leasing_cost_dol_per_yr)
                ,
                year_number=year_index + 1,
            )
            for year_index in range(self.vehicle_life_yr)
        )

        self.total_downtime_hr = sum(
            self.tco_per_year[year_index].oppy_costs_dol.net_downtime_hr_per_yr
            for year_index in range(self.vehicle_life_yr)
        )
        self.total_fueling_dwell_time_hr = sum(
            self.tco_per_year[year_index].oppy_costs_dol.fueling_dwell_time_hr_per_yr
            for year_index in range(self.vehicle_life_yr)
        )
        self.total_mr_downtime_hr = sum(
            self.tco_per_year[year_index].oppy_costs_dol.mr_downtime_hr_per_yr
            for year_index in range(self.vehicle_life_yr)
        )
        self.insurance_cost_dol = sum(
            self.scenario.get_discounted_value(
                self.tco_per_year[year_index].oper_costs_dol.insurance_cost_dol_per_yr,
                year_number=year_index + 1,
            )
            for year_index in range(self.vehicle_life_yr)
        )
        self.fueling_dwell_labor_cost_dol = sum(
            self.scenario.get_discounted_value(
                self.tco_per_year[
                    year_index
                ].oper_costs_dol.fueling_dwell_labor_cost_dol_per_yr,
                year_number=year_index + 1,
            )
            for year_index in range(self.vehicle_life_yr)
        )
        self.fueling_downtime_oppy_cost_dol = sum(
            self.scenario.get_discounted_value(
                self.tco_per_year[
                    year_index
                ].oppy_costs_dol.fueling_downtime_oppy_cost_dol_per_yr,
                year_number=year_index + 1,
            )
            for year_index in range(self.vehicle_life_yr)
        )
        self.mr_downtime_oppy_cost_dol = sum(
            self.scenario.get_discounted_value(
                self.tco_per_year[
                    year_index
                ].oppy_costs_dol.mr_downtime_oppy_cost_dol_per_yr,
                year_number=year_index + 1,
            )
            for year_index in range(self.vehicle_life_yr)
        )
        self.residual_cost_dol = self.tco_per_year[
            -1
        ].cap_costs_dol.disc_residual_cost_dol

    def set_discounted_tco(self):
        """
        Sets the discounted TCO for the Ledger instance.
        """
        self.undiscounted_tco_dol = self.payload_cap_cost_multiplier * sum(
                self.tco_per_year[
                    year_index
                ].total_cost_dol_per_yr
            
            for year_index in range(self.vehicle_life_yr)
        )    
        
        if self.tco_method == "DIRECT":
            self.discounted_tco_dol = self.payload_cap_cost_multiplier * (
                self.discounted_total_cap_cost_dol
                + self.discounted_total_oper_cost_dol
                + self.discounted_downtime_oppy_cost_dol
                + self.residual_cost_dol
            )
            self.payload_capacity_cost_dol = (
                (self.payload_cap_cost_multiplier - 1)
                / self.payload_cap_cost_multiplier
                * self.discounted_tco_dol
            )

        elif self.tco_method == "EFFICIENCY":
            downtime_efficiency = 1 / (
                1
                + self.scenario.avg_speed_mph
                * self.discounted_downtime_oppy_cost_dol
                / self.disc_total_vmt
            )
            self.discounted_tco_dol = self.payload_cap_cost_multiplier * (
                (
                    self.discounted_total_cap_cost_dol
                    + self.discounted_total_oper_cost_dol
                )
                / downtime_efficiency
                + self.residual_cost_dol
            )
            self.disc_downtime_oppy_cost_dol = (
                self.discounted_total_cap_cost_dol
                + self.discounted_total_oper_cost_dol
                + self.discounted_downtime_oppy_cost_dol
            ) * (1 / downtime_efficiency - 1)

            self.payload_capacity_cost_dol = (
                (self.payload_cap_cost_multiplier - 1)
                / self.payload_cap_cost_multiplier
                * self.discounted_tco_dol
            )

    def set_cost_components(self):
        """
        Sets the cost components for the Ledger instance.
        """
        self.glider_cost_dol = self.tco_per_year[0].cap_costs_dol.glider_cost_dol
        self.fuel_converter_cost_dol = self.tco_per_year[
            0
        ].cap_costs_dol.fuel_converter_cost_dol
        self.fuel_storage_cost_dol = self.tco_per_year[
            0
        ].cap_costs_dol.fuel_storage_cost_dol
        self.motor_control_power_elecs_cost_dol = self.tco_per_year[
            0
        ].cap_costs_dol.motor_control_power_elecs_cost_dol
        self.plug_cost_dol = self.tco_per_year[0].cap_costs_dol.plug_cost_dol
        self.battery_cost_dol = self.tco_per_year[0].cap_costs_dol.battery_cost_dol
        self.purchase_tax_dol = self.tco_per_year[0].cap_costs_dol.purchase_tax_dol
        self.msrp_total_dol = self.tco_per_year[0].cap_costs_dol.msrp_total_dol

        self.scenario.fuel_prices_dol_per_gge = [
            self.tco_per_year[year_index].oper_costs_dol.fuel_price_dol_per_gge
                for year_index in range(self.vehicle_life_yr)
                ]
        self.total_fuel_used_gal_ge = sum(
            [
                self.tco_per_year[year_index].oper_costs_dol.fuel_used_gal_gge_per_yr
                for year_index in range(self.vehicle_life_yr)
            ]
        )

        self.total_fuel_used_gal_de = self.total_fuel_used_gal_ge / gl.DGE_TO_GGE
        self.total_energy_used_kwh = self.total_fuel_used_gal_ge * gl.KWH_PER_GGE

        self.mpgge = self.energy.mpgge
        self.grid_mpgge = (
            self.energy.mpgge * self.vehicle.chg_eff if self.vehicle.chg_eff else None
        )
        self.mpgde = self.energy.mpgge / gl.DieselGalPerGasGal
        self.kwh_per_mi = None

    def to_dict(self, include_prefix: bool = True, flatten: bool = True) -> dict:
        """
        Exports the Ledger instance to a dictionary.

        Args:
            include_prefix (bool, optional): If True, exported column names contain the T3CO submodule names as prefix. Defaults to True.
            flatten (bool, optional): If True, the nested dict output flattens to a single dictionary. Defaults to True.

        Returns:
            dict: The Ledger instance as a dictionary.
        """
        self.scenario.delete_dataframes()
        if self.config:
            self.config.delete_dataframes()
            
        if flatten:
            t3co_dict = to_flat_dict(self, include_predix=include_prefix, delimiter="_")
        else:
            t3co_dict = json.loads(json.dumps(self, default=custom_default))
        return t3co_dict

    def to_json(self, filepath: Union[str, Path], include_prefix: bool = True, flatten: bool = True) -> None:
        """
        Saves the Ledger instance to a JSON file.

        Args:
            filepath (Union[str, Path]): The file path where the JSON will be saved.
            include_prefix (bool, optional): If True, exported column names contain the T3CO submodule names as prefix. Defaults to True.
            flatten (bool, optional): If True, the nested dict output flattens to a single dictionary. Defaults to True.
        """
        t3co_dict = self.to_dict(include_prefix=include_prefix, flatten=flatten)

        if filepath:
            filepath = Path(filepath)
            if not filepath.parent.exists():
                filepath.parent.mkdir()
            with open(filepath, "w") as f:
                json.dump(handle_nan(t3co_dict), f, indent=4)
                print(f"Saved to {str(filepath.resolve())}")
        else:
            raise Exception("Filepath must be provided.")

    def to_df(self) -> pd.DataFrame:
        """
        Converts the Ledger instance to a DataFrame.

        Returns:
            pd.DataFrame: The Ledger instance as a DataFrame.
        """
        t3co_dict = self.to_dict(include_prefix=True, flatten=True)
        t3co_dict.pop("tco_per_year")
        return pd.DataFrame([t3co_dict])

    def to_csv(self, filepath: Union[str, Path]) -> None:
        """
        Saves the Ledger instance to a CSV file.

        Args:
            filepath (Union[str, Path]): The file path where the CSV will be saved.
        """
        if filepath:
            filepath = Path(filepath)
            if not filepath.parent.exists():
                filepath.parent.mkdir()
            print(f"Saved to {str(filepath.resolve())}")
            self.to_df().to_csv(filepath)
        else:
            raise Exception("Filepath must be provided.")

    def __str__(self) -> str:
        """
        Returns a string representation of the Ledger instance.

        Returns:
            str: String representation of the Ledger instance.
        """
        return obj_to_string(self)