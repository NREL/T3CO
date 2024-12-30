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
    disc_tco_per_year: list[TCOCalc] = []
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

    def __str__(self):
        return obj_to_string(self)
