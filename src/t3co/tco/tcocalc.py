from t3co.cost_models.capital_costs import CapitalCosts
from t3co.cost_models.operating_costs import OperatingCosts
from t3co.cost_models.opportunity_costs import OpportunityCosts
from t3co.energy_models.energy import Energy
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle
from t3co.utils.print_class_objects import obj_to_string


class TCOCalc:
    year_number: int = None
    total_cost_dol_per_yr: float = None
    disc_total_cost_dol_per_yr: float = None
    cap_costs_dol: CapitalCosts = None
    oper_costs_dol: OperatingCosts = None
    oppy_costs_dol: OpportunityCosts = None

    def __init__(
        self,
        year_index: int,
        vehicle: Vehicle,
        scenario: Scenario,
        energy: Energy,
        payload_cap_cost_multiplier: float = None,
        cap_costs: CapitalCosts = None,
    ):
        self.year_number = year_index + 1
        if self.year_number == 1:
            self.calculate_capital_costs(vehicle=vehicle, scenario=scenario)

        if cap_costs:
            self.cap_costs_dol = cap_costs
        else:
            self.calculate_capital_costs(vehicle=vehicle, scenario=scenario)

        self.calculate_opportunity_costs(
            vehicle=vehicle, scenario=scenario, energy=energy
        )
        if payload_cap_cost_multiplier:
            self.oppy_costs_dol.payload_cap_cost_multiplier = (
                payload_cap_cost_multiplier
            )

        self.calculate_operating_costs(
            vehicle=vehicle, scenario=scenario, energy=energy
        )
        self.set_total_cost(scenario=scenario)
        self.set_disc_total_cost(
            vehicle=vehicle,
            scenario=scenario,
            payload_cap_cost_multiplier=payload_cap_cost_multiplier,
        )

    def calculate_capital_costs(self, vehicle: Vehicle, scenario: Scenario):
        self.cap_costs_dol = CapitalCosts(vehicle=vehicle, scenario=scenario)

    def calculate_opportunity_costs(
        self, vehicle: Vehicle, scenario: Scenario, energy: Energy
    ):
        self.oppy_costs_dol = OpportunityCosts(
            year_number=self.year_number,
            vehicle=vehicle,
            scenario=scenario,
            energy=energy,
        )

    def calculate_operating_costs(
        self, vehicle: Vehicle, scenario: Scenario, energy: Energy
    ):
        self.oper_costs_dol = OperatingCosts(
            year_number=self.year_number,
            cap_costs=self.cap_costs_dol,
            vehicle=vehicle,
            scenario=scenario,
            energy=energy,
            oppy_costs=self.oppy_costs_dol,
        )

    def set_total_cost(self, scenario: Scenario):
        self.total_cost_dol_per_yr = (
            (self.cap_costs_dol.net_capital_cost_dol if self.year_number == 1 else 0)
            + self.oper_costs_dol.net_oper_cost_dol_per_yr
            + self.oppy_costs_dol.net_downtime_oppy_cost_dol_per_yr
            + (
                self.cap_costs_dol.residual_cost_dol
                if self.year_number == scenario.vehicle_life_yr
                else 0
            )
        )

    def set_disc_total_cost(
        self,
        vehicle: Vehicle,
        scenario: Scenario,
        payload_cap_cost_multiplier: float = None,
        TCO_switch="DIRECT",
    ):
        if (
            payload_cap_cost_multiplier is not None
            and not self.oppy_costs_dol.payload_cap_cost_multiplier
        ):
            self.oppy_costs_dol.payload_cap_cost_multiplier = (
                payload_cap_cost_multiplier
            )
        elif self.oppy_costs_dol.payload_cap_cost_multiplier:
            pass
        else:
            self.oppy_costs_dol.set_payload_cap_cost_multiplier(
                vehicle=vehicle, scenario=scenario
            )

        if TCO_switch == "DIRECT":
            self.disc_total_cost_dol_per_yr = (
                self.oppy_costs_dol.payload_cap_cost_multiplier
                * (
                    self.cap_costs_dol.net_capital_cost_dol
                    + self.oper_costs_dol.disc_oper_cost_dol_per_yr
                    + self.oppy_costs_dol.disc_downtime_oppy_cost_dol
                )
            )
            self.oppy_costs_dol.payload_capacity_cost_dol = (
                (self.oppy_costs_dol.payload_cap_cost_multiplier - 1)
                / self.oppy_costs_dol.payload_cap_cost_multiplier
                * self.disc_total_cost_dol_per_yr
            )

        elif TCO_switch == "EFFICIENCY":
            disc_VMT_sum = scenario.vmt[self.year_number - 1] / (
                1 + scenario.discount_rate_pct_per_yr
            ) ** (self.year_number - 1)

            downtime_efficiency = 1 / (
                1
                + scenario.avg_speed_mph
                * self.oppy_costs_dol.disc_downtime_oppy_cost_dol
                / disc_VMT_sum
            )
            self.disc_total_cost_dol_per_yr = (
                self.oppy_costs_dol.payload_cap_cost_multiplier
                * (
                    (
                        self.cap_costs_dol.net_capital_cost_dol
                        + self.oper_costs_dol.disc_oper_cost_dol_per_yr
                    )
                    / downtime_efficiency
                    + self.cap_costs_dol.residual_cost_dol
                )
            )
            self.oppy_costs_dol.disc_downtime_oppy_cost_dol = (
                self.cap_costs_dol.net_capital_cost_dol
                + self.oper_costs_dol.disc_oper_cost_dol_per_yr
                + self.oppy_costs_dol.disc_downtime_oppy_cost_dol
            ) * (1 / downtime_efficiency - 1)

            self.oppy_costs_dol.payload_capacity_cost_dol = (
                (self.oppy_costs_dol.payload_cap_cost_multiplier - 1)
                / self.oppy_costs_dol.payload_cap_cost_multiplier
                * self.disc_total_cost_dol_per_yr
            )

    def __str__(self):
        return obj_to_string(self)
