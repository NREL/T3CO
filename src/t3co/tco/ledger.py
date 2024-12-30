from dataclasses import dataclass, field
from typing import List
import numpy as np

from t3co.energy_models.energy import Energy
from t3co.input_data.config import Config
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle
from t3co.tco.tcocalc import TCOCalc
from t3co.utils.print_class_objects import obj_to_string


class Ledger:
    discounted_tco_dol: float = None
    vehicle_life_yr: int = None
    tco_per_year: list[TCOCalc] = []
    disc_total_cap_cost_dol: float = None
    disc_total_oper_cost_dol: float = None
    disc_total_oppy_cost_dol: float = None
    cumu_tco_dol_per_yr: list[float] = []
    cumu_tco_dol_per_mi: list[float] = []
    payload_capacity_cost_dol: float = None
    
    scenario: Scenario = None
    vehicle: Vehicle = None
    config: Config = None
    energy: Energy = None

    def __init__(
        self,
        vehicle: Vehicle,
        scenario: Scenario,
        energy: Energy = None,
        config: Config = None,
    ):
        self.vehicle = vehicle
        self.scenario = scenario
        self.tco_per_year = []
        if config:
            self.config = config
            self.vehicle_life_yr = config.vehicle_life_yr
        else:
            self.vehicle_life_yr = scenario.vehicle_life_yr

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
                        self.tco_per_year[year_index - 1].oppy_costs_dol.payload_cap_cost_multiplier
                        if year_index
                        else None
                    )
                    # payload_cap_cost_multiplier = None
                )
            )

        self.set_disc_total_costs()
        self.set_discounted_tco(TCO_switch=(config.TCO_method if config else "DIRECT"))

    def set_disc_total_costs(self):
        self.disc_total_cap_cost_dol = 0
        self.disc_total_oper_cost_dol = 0
        self.disc_total_oppy_cost_dol = 0
        self.payload_cap_cost_multiplier = self.tco_per_year[0].oppy_costs_dol.payload_cap_cost_multiplier
        self.disc_total_cap_cost_dol+=self.tco_per_year[0].cap_costs_dol.net_capital_cost_dol
        for year_index in range(self.vehicle_life_yr):
            self.disc_total_oper_cost_dol+=self.tco_per_year[year_index].oper_costs_dol.disc_oper_cost_dol_per_yr
            self.disc_total_oppy_cost_dol+=self.tco_per_year[year_index].oppy_costs_dol.disc_downtime_oppy_cost_dol
            
    def set_discounted_tco(self, TCO_switch:str = "DIRECT"):
        if TCO_switch == "DIRECT":
            self.disc_total_cost_dol_per_yr = self.payload_cap_cost_multiplier * (
                self.disc_total_cap_cost_dol
                + self.disc_total_oper_cost_dol
                + self.disc_total_oppy_cost_dol
            )
            self.payload_capacity_cost_dol = (
                (self.payload_cap_cost_multiplier - 1) / self.payload_cap_cost_multiplier * self.disc_total_cost_dol_per_yr
            )

        elif TCO_switch == "EFFICIENCY":
            disc_VMT_sum = sum(
                    [
                        self.scenario.vmt[year_number] / (1 + self.scenario.discount_rate_pct_per_yr) ** (year_number) for year_number in range(self.vehicle_life_yr)
                    ]

            )

            downtime_efficiency = 1 / (1 + self.scenario.avg_speed_mph * self.disc_total_oppy_cost_dol / disc_VMT_sum)
            self.disc_total_cost_dol_per_yr = self.payload_cap_cost_multiplier * (
                (self.disc_total_cap_cost_dol + self.disc_total_oper_cost_dol)
                / downtime_efficiency
                + self.tco_per_year[-1].cap_costs_dol.disc_residual_cost_dol
            )
            self.disc_downtime_oppy_cost_dol = (
                self.disc_total_cap_cost_dol
                + self.disc_total_oper_cost_dol
                + self.disc_total_oppy_cost_dol
            ) * (1 / downtime_efficiency - 1)

            self.payload_capacity_cost_dol = (
                (self.payload_cap_cost_multiplier - 1) / self.payload_cap_cost_multiplier * self.disc_total_cost_dol_per_yr 
            )

    def __str__(self):
        return obj_to_string(self)
