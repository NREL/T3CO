from __future__ import annotations

import ast
from math import ceil
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from scipy.integrate import trapezoid
from t3co.constants import Global as gl
from t3co.energy_models.energy import Energy
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle
from t3co.utils.print_class_objects import obj_to_string


class OpportunityCosts:
    payload_cap_cost_multiplier: float = 1.0
    fueling_dwell_time_hr_per_yr: float = 0.0
    mr_planned_downtime_hr: float = 0.0
    mr_unplanned_downtime_hr: float = 0.0
    mr_tire_replacement_downtime_hr: float = 0.0
    mr_downtime_hr_per_yr: float = 0.0
    net_downtime_hr_per_yr: float = 0.0
    fueling_dwell_labor_cost_dol_per_yr: float = 0.0
    fueling_downtime_oppy_cost_dol_per_yr: float = 0.0
    mr_downtime_oppy_cost_dol_per_yr: float = 0.0
    payload_capacity_cost_dol: float = 0.0
    shifts_per_year: float = 0.0
    trip_distance_mi: float = 0.0
    net_downtime_oppy_cost_dol_per_yr: float = 0.0
    disc_downtime_oppy_cost_dol: float = 0.0

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the OpportunityCosts class.
        """
        instance = super(OpportunityCosts, cls).__new__(cls)
        return instance

    def __init__(
        self, year_number: int, vehicle: Vehicle, scenario: Scenario, energy: Energy
    ):
        """
        Initializes the OpportunityCosts instance.

        Args:
            year_number (int): The year number for which the opportunity costs are calculated.
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
            energy (Energy): The energy model instance.
        """
        if year_number == 1 and scenario.activate_tco_payload_cap_cost_multiplier:
            self.set_payload_cap_cost_multiplier(vehicle=vehicle, scenario=scenario)

        if scenario.activate_tco_fueling_dwell_time_cost:
            self.set_fueling_dwell_time_cost(
                year_number=year_number,
                vehicle=vehicle,
                scenario=scenario,
                energy=energy,
            )
        if scenario.activate_mr_downtime_cost:
            self.set_mr_downtime_cost(
                year_number=year_number, vehicle=vehicle, scenario=scenario
            )

        self.set_net_downtime_oppy_cost()
        self.set_disc_downtime_oppy_cost(year_number=year_number, scenario=scenario)

    def set_payload_cap_cost_multiplier(
        self, vehicle: Vehicle, scenario: Scenario
    ) -> None:
        """
        Sets the payload capacity cost multiplier for the vehicle.

        This method calculates the payload capacity cost multiplier based on the vehicle's weight and the scenario's weight distribution.

        Inputs from scenario:
        - plf_weight_distribution_file
        - plf_ref_veh_empty_mass_kg
        - gvwr_kg
        - gvwr_credit_kg

        Inputs from vehicle:
        - veh_kg
        - cargo_kg

        Estimated class variables:
        - payload_cap_cost_multiplier

        Args:
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        df_veh_wt = pd.read_csv(
            (
                Path(scenario.plf_weight_distribution_file).resolve(strict=True)
                if Path(scenario.plf_weight_distribution_file).is_absolute()
                else gl.RESOURCES_FOLDERPATH / scenario.plf_weight_distribution_file
            ),
            index_col=0,
        )

        def set_kdes(
            df_veh_wt: pd.DataFrame,
            bw_method: float = 0.15,
            verbose: bool = False,
        ) -> tuple[np.ndarray, np.ndarray]:
            """
            Sets the kernel density estimation (KDE) for vehicle weights.

            Args:
                df_veh_wt (pd.DataFrame): DataFrame containing vehicle weights.
                bw_method (float, optional): Kernel bandwidth method used by gaussian_kde. Defaults to 0.15.
                verbose (bool, optional): If True, prints process steps. Defaults to False.

            Returns:
                tuple[np.ndarray, np.ndarray]: Normalized probabilities and vehicle weight bins in kg.
            """
            if verbose:
                print("Initializing kernels.")

            df_veh_wt = df_veh_wt[~df_veh_wt["WEIGHTAVG"].isnull()]
            df_veh_wt = df_veh_wt[~df_veh_wt["WEIGHTEMPTY"].isnull()]
            df_veh_wt = df_veh_wt[df_veh_wt["WEIGHTAVG"] < 120000]

            weights = df_veh_wt["TAB_MILES"] / np.nansum(df_veh_wt["TAB_MILES"])
            kernel = gaussian_kde(
                df_veh_wt["WEIGHTAVG"], weights=weights, bw_method=bw_method
            )
            vehicle_weights_bins_lb = np.linspace(
                df_veh_wt["WEIGHTAVG"].min(),
                df_veh_wt["WEIGHTAVG"].max(),
                1000,
            )
            vehicle_weights_bins_kg = gl.lbs_to_kgs(vehicle_weights_bins_lb)

            # get probability of each vehicle weight
            p_of_weights = kernel(vehicle_weights_bins_lb)

            probability_payload = pd.DataFrame(
                [vehicle_weights_bins_kg, p_of_weights],
                index=["vehicle_weights_bins_kg", "p_of_weights"],
            ).T
            if verbose:
                probability_payload.to_csv(
                    (
                        Path(scenario.plf_weight_distribution_file).resolve(strict=True)
                        if Path(scenario.plf_weight_distribution_file).is_absolute()
                        else gl.RESOURCES_FOLDERPATH
                        / scenario.plf_weight_distribution_file
                    ).parents[0]
                    / "payload_pdf.csv"
                )
            normalization_factor = probability_payload[
                probability_payload["vehicle_weights_bins_kg"].between(
                    scenario.plf_ref_veh_empty_mass_kg, scenario.gvwr_kg
                )
            ]["p_of_weights"].sum()
            p_of_weights_normalized = p_of_weights / (
                normalization_factor if normalization_factor else 1
            )

            return p_of_weights_normalized, vehicle_weights_bins_kg

        p_of_weights_normalized, vehicle_weights_bins_kg = set_kdes(
            df_veh_wt=df_veh_wt, verbose=False
        )

        new_empty_weight_kg = vehicle.veh_kg - vehicle.cargo_kg
        empty_increase_kg = new_empty_weight_kg - scenario.plf_ref_veh_empty_mass_kg
        new_cargo_cieling_kg = (
            scenario.gvwr_kg - empty_increase_kg + scenario.gvwr_credit_kg
        )

        if empty_increase_kg >= scenario.gvwr_credit_kg:
            a = vehicle_weights_bins_kg - new_cargo_cieling_kg
            minidx = (
                np.where(vehicle_weights_bins_kg == a[a > 0][0] + new_cargo_cieling_kg)
            )[0][0]
            a = vehicle_weights_bins_kg - scenario.gvwr_kg
            maxidx = (
                np.where(vehicle_weights_bins_kg == a[a > 0][0] + scenario.gvwr_kg)
            )[0][0]

            estimated_lost_payload_per_bin_kg = p_of_weights_normalized[
                minidx:maxidx
            ] * (vehicle_weights_bins_kg[minidx:maxidx] - new_cargo_cieling_kg)
            estimated_lost_payload_kg = trapezoid(estimated_lost_payload_per_bin_kg)

            # payload cost multiplier
            self.payload_cap_cost_multiplier = 1 + estimated_lost_payload_kg / (
                scenario.gvwr_kg - new_empty_weight_kg + scenario.gvwr_credit_kg
            )

            scenario.estimated_lost_payload_kg = estimated_lost_payload_kg
        else:
            self.payload_cap_cost_multiplier = 1
        # recording final report data on vehicle empty weights and cargo capcities
        scenario.plf_scenario_vehicle_empty_kg = new_empty_weight_kg
        scenario.plf_reference_vehicle_cargo_capacity_kg = (
            scenario.gvwr_kg - scenario.plf_ref_veh_empty_mass_kg
        )
        scenario.plf_scenario_vehicle_cargo_capacity_kg = (
            scenario.gvwr_kg + scenario.gvwr_credit_kg - new_empty_weight_kg
        )

    def set_fueling_dwell_time_cost(
        self, year_number: int, vehicle: Vehicle, scenario: Scenario, energy: Energy
    ) -> None:
        """
        Calculates the fueling dwell time cost for a vehicle based on fuel fill rate/charging power and shifts per year.

        Inputs from scenario:
        - fdt_frac_full_charge_bounds
        - shifts_per_year
        - constant_trip_distance_mi
        - vmt
        - fdt_dwpt_fraction_power_pct
        - ess_max_charging_power_kw
        - fs_fueling_rate_gasoline_gpm
        - fs_fueling_rate_diesel_gpm
        - fdt_num_free_dwell_trips
        - fdt_avg_overhead_hr_per_dwell_hr
        - fdt_available_freetime_hr
        - downtime_oppy_cost_dol_per_hr

        Inputs from vehicle:
        - veh_pt_type
        - ess_max_kwh
        - fs_kwh

        Inputs from energy:
        - primary_fuel_range_mi

        Estimated OpportunityCosts variables:
        - fdt_frac_full_charge_bounds
        - shifts_per_year
        - fdt_full_dwell_hr
        - trip_distance_mi
        - fdt_num_of_dwells
        - fueling_dwell_time_hr_per_yr
        - fueling_downtime_oppy_cost_dol_per_yr

        Args:
        year_number (int): The year number for which the fueling dwell time cost is calculated.
        vehicle (Vehicle): The vehicle instance.
        scenario (Scenario): The scenario instance containing configuration data.
        energy (Energy): The energy model instance.
        """
        self.fdt_frac_full_charge_bounds = (
            ast.literal_eval(scenario.fdt_frac_full_charge_bounds)
            if isinstance(scenario.fdt_frac_full_charge_bounds, str)
            else scenario.fdt_frac_full_charge_bounds
        )

        if (
            "0" in str(scenario.shifts_per_year) or np.isnan(scenario.shifts_per_year)
        ) and scenario.constant_trip_distance_mi:
            self.shifts_per_year = round(
                scenario.vmt[year_number - 1] / scenario.constant_trip_distance_mi
            )
        else:
            self.shifts_per_year = scenario.shifts_per_year[year_number - 1]

        # dwellparams = np.array(
        #     [
        #         scenario.fdt_dwpt_fraction_power_pct,
        #         scenario.fdt_frac_full_charge_bounds,
        #         scenario.fdt_avg_overhead_hr_per_dwell_hr,
        #         scenario.downtime_oppy_cost_dol_per_hr,
        #     ]
        # )

        if vehicle.veh_pt_type in ["BEV"]:
            self.fdt_full_dwell_hr = (1 - scenario.fdt_dwpt_fraction_power_pct) * (
                vehicle.ess_max_kwh / scenario.ess_max_charging_power_kw
            )
        elif vehicle.veh_pt_type in ["Conv"]:
            if scenario.fuel_type in ["gasoline"]:
                self.fdt_full_dwell_hr = (
                    vehicle.fs_kwh
                    / (gl.KWH_PER_GGE)
                    / scenario.fs_fueling_rate_gasoline_gpm
                ) / 60
            else:
                self.fdt_full_dwell_hr = (
                    vehicle.fs_kwh
                    / (gl.KWH_PER_GGE / gl.DieselGalPerGasGal)
                    / scenario.fs_fueling_rate_diesel_gpm
                ) / 60
        else:
            self.fdt_full_dwell_hr = (
                (1 - scenario.fdt_dwpt_fraction_power_pct)
                * (
                    vehicle.fs_kwh
                    / (gl.KWH_PER_GGE / gl.kgH2_per_gge)
                    / scenario.fs_fueling_rate_kg_per_min
                )
                / 60
            )

        self.trip_distance_mi = scenario.vmt[year_number - 1] / self.shifts_per_year
        self.fdt_num_of_dwells = max(
            0,
            (
                (self.trip_distance_mi)
                * (1 - scenario.fdt_dwpt_fraction_power_pct)
                / energy.primary_fuel_range_mi
                - scenario.fdt_num_free_dwell_trips
            ),
        )

        if self.fdt_num_of_dwells != 0:
            remaining_dwells = self.fdt_num_of_dwells % 1
            if remaining_dwells < self.fdt_frac_full_charge_bounds[0]:
                self.fdt_num_of_dwells += (
                    self.fdt_frac_full_charge_bounds[0] - remaining_dwells
                )
            elif (
                self.fdt_frac_full_charge_bounds[0]
                < remaining_dwells
                < self.fdt_frac_full_charge_bounds[1]
            ):
                self.fdt_num_of_dwells += 0
            else:
                self.fdt_num_of_dwells += 1 - remaining_dwells

        if (self.fdt_num_of_dwells < 1 and not scenario.fdt_num_free_dwell_trips) or (
            scenario.fuel_type
        ):
            self.fueling_dwell_time_hr_per_yr = (
                scenario.vmt[year_number - 1]
                * (1 - scenario.fdt_dwpt_fraction_power_pct)
                / energy.primary_fuel_range_mi
                * (self.fdt_full_dwell_hr + scenario.fdt_avg_overhead_hr_per_dwell_hr)
            )
        else:
            dwell_time_hr = (
                self.fdt_num_of_dwells * self.fdt_full_dwell_hr
                + ceil(self.fdt_num_of_dwells)
                * scenario.fdt_avg_overhead_hr_per_dwell_hr
            )
            self.fueling_dwell_time_hr_per_yr = self.shifts_per_year * max(
                0,
                (dwell_time_hr - max(0, scenario.fdt_available_freetime_hr)),
            )

        self.fueling_downtime_oppy_cost_dol_per_yr = (
            self.fueling_dwell_time_hr_per_yr * scenario.downtime_oppy_cost_dol_per_hr
        )

    def set_mr_downtime_cost(
        self, year_number: int, vehicle: Vehicle, scenario: Scenario
    ) -> None:
        """
        Calculates the Maintenance and Repair (M&R) downtime cost based on planned, unplanned, and tire replacement downtime inputs.

        Inputs from scenario:
        - mr_planned_downtime_hr_per_yr
        - mr_unplanned_downtime_hr_per_mi
        - vmt
        - mr_avg_tire_life_mi
        - mr_tire_replace_downtime_hr_per_event
        - downtime_oppy_cost_dol_per_hr

        Estimated OpportunityCosts variables:
        - mr_planned_downtime_hr
        - mr_unplanned_downtime_hr
        - mr_tire_replacement_downtime_hr
        - mr_downtime_hr_per_yr
        - mr_downtime_oppy_cost_dol_per_yr

        Args:
            year_number (int): The year number for which the M&R downtime cost is calculated.
            vehicle (Vehicle): The vehicle instance.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        self.mr_planned_downtime_hr = scenario.mr_planned_downtime_hr_per_yr
        self.mr_unplanned_downtime_hr = (
            scenario.mr_unplanned_downtime_hr_per_mi[year_number - 1]
            * scenario.vmt[year_number - 1]
        )

        self.mr_tire_replacement_downtime_hr = (
            scenario.vmt[year_number - 1]
            / scenario.mr_avg_tire_life_mi
            * scenario.mr_tire_replace_downtime_hr_per_event
        )

        self.mr_downtime_hr_per_yr = (
            self.mr_planned_downtime_hr
            + self.mr_unplanned_downtime_hr
            + self.mr_tire_replacement_downtime_hr
        )
        self.mr_downtime_oppy_cost_dol_per_yr = (
            self.mr_downtime_hr_per_yr * scenario.downtime_oppy_cost_dol_per_hr
        )

    def set_net_downtime_oppy_cost(self) -> None:
        """
        Sets the net downtime opportunity cost for the vehicle.

        This method calculates the net downtime opportunity cost by summing the fueling downtime and MR downtime opportunity costs.
        The calculation uses the following OpportunityCosts elements:
        - fueling_downtime_oppy_cost_dol_per_yr
        - mr_downtime_oppy_cost_dol_per_yr
        - fueling_dwell_time_hr_per_yr
        - mr_downtime_hr_per_yr

        Estimated OpportunityCosts variables:
        - net_downtime_oppy_cost_dol_per_yr
        - net_downtime_hr_per_yr
        """
        self.net_downtime_oppy_cost_dol_per_yr = (
            self.fueling_downtime_oppy_cost_dol_per_yr
            + self.mr_downtime_oppy_cost_dol_per_yr
        )
        self.net_downtime_hr_per_yr = (
            self.fueling_dwell_time_hr_per_yr + self.mr_downtime_hr_per_yr
        )

    def set_disc_downtime_oppy_cost(self, year_number: int, scenario: Scenario) -> None:
        """
        Sets the discounted downtime opportunity cost for the given year.

        Inputs from scenario:
        - discount_rate_pct_per_yr

        Estimated class variables:
        - disc_downtime_oppy_cost_dol

        Args:
            year_number (int): The year number for which the discounted downtime opportunity cost is calculated.
            scenario (Scenario): The scenario instance containing configuration data.
        """
        self.disc_downtime_oppy_cost_dol = scenario.get_discounted_value(
            value=self.net_downtime_oppy_cost_dol_per_yr, year_number=year_number
        )

    def __str__(self) -> str:
        """
        Returns a string representation of the OpportunityCosts instance.

        Returns:
            str: String representation of the OpportunityCosts instance.
        """
        return obj_to_string(self)
