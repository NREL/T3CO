# %%
from __future__ import annotations

import ast
import os
import warnings
from math import ceil
from pathlib import Path

import fastsim
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

from t3co.energy_models.energy import Energy
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle
from t3co.constants import Global as gl

class OpportunityCosts:
    payload_cap_cost_multiplier: float = None
    fueling_dwell_time_hr_per_yr: float = None
    mr_planned_downtime_hr: float = None
    mr_unplanned_downtime_hr: float = None
    mr_tire_replacement_downtime_hr: float = None
    mr_downtime_hr_per_yr: float = None
    net_downtime_hr_per_yr: float =None
    fueling_dwell_labor_cost_dol_per_yr: float =None
    fueling_downtime_oppy_cost_dol_per_yr: float =None
    mr_downtime_oppy_cost_dol_per_yr: float =None
    payload_capacity_cost_dol: float =None
    shifts_per_year: float = None
    trip_distance_mi: float = None
    def __init__(self, year_number:int, vehicle:Vehicle, scenario: Scenario, energy: Energy ):
        self.set_payload_cap_cost_multiplier(year_number=year_number, vehicle=vehicle, scenario=scenario)
        self.set_fueling_dwell_time_cost(year_number=year_number, vehicle=vehicle, scenario=scenario)
        self.set_mr_downtime_cost(year_number=year_number, vehicle=vehicle, scenario=scenario)

    def set_payload_cap_cost_multiplier(self, year_number:int,  vehicle:Vehicle, scenario:Scenario):
        if scenario.activate_tco_fueling_dwell_time_cost:
            self.frac_of_fullcharge_bounds = list(
                np.float_(scenario.fdt_frac_full_charge_bounds.strip(" ][").split(","))
            )
            if (
                "0" in str(scenario.shifts_per_year)
                or np.isnan(scenario.shifts_per_year)
            ) and scenario.constant_trip_distance_mi:
                self.shifts_per_year = round(scenario.vmt[year_number] / scenario.constant_trip_distance_mi)
            else:
                self.shifts_per_year = ast.literal_eval(scenario.shifts_per_year)[year_number]

            self.df_veh_wt = pd.read_csv(scenario.plf_weight_distribution_file, index_col=0)
            def set_kdes(
                bw_method: float = 0.15,
                verbose: bool = False,
            ) -> None:
                """
                This method sets tje kde kernel. This is time-consuming, only call this once, if possible.

                Args:
                    scenario (run_scenario.Scenario): Scenario object
                    bw_method (float, optional):  kernel bandwidth method used by guassian_kde. Defaults to .15.
                    verbose (bool, optional): if True, prints process sets. Defaults to False.
                """

                if verbose:
                    print("Initializing kernels.")

                self.df_veh_wt = self.df_veh_wt[~self.df_veh_wt["WEIGHTAVG"].isnull()]
                self.df_veh_wt = self.df_veh_wt[~self.df_veh_wt["WEIGHTEMPTY"].isnull()]
                self.df_veh_wt = self.df_veh_wt[self.df_veh_wt["WEIGHTAVG"] < 120000]

                weights = self.df_veh_wt["TAB_MILES"] / np.nansum(self.df_veh_wt["TAB_MILES"])
                kernel = gaussian_kde(
                    self.df_veh_wt["WEIGHTAVG"], weights=weights, bw_method=bw_method
                )
                vehicle_weights_bins_lb = np.linspace(
                    self.df_veh_wt["WEIGHTAVG"].min(), self.df_veh_wt["WEIGHTAVG"].max(), 1000
                )
                vehicle_weights_bins_kg = gl.lbs_to_kgs(vehicle_weights_bins_lb)

                # get probability of each vehicle weight
                p_of_weights = kernel(vehicle_weights_bins_lb)

                probability_payload = pd.DataFrame(
                    [vehicle_weights_bins_kg, p_of_weights],
                    index=["vehicle_weights_bins_kg", "p_of_weights"],
                ).T
                probability_payload.to_csv(
                    Path(scenario.plf_weight_distribution_file).parents[0] / "payload_pdf.csv"
                )
                normalization_factor = probability_payload[
                    probability_payload["vehicle_weights_bins_kg"].between(
                        scenario.plf_ref_veh_empty_mass_kg, scenario.gvwr_kg
                    )
                ]["p_of_weights"].sum()
                p_of_weights_normalized = p_of_weights / normalization_factor
                
                return p_of_weights_normalized, vehicle_weights_bins_kg

            
            p_of_weights_normalized, vehicle_weights_bins_kg = set_kdes(scenario, verbose=False)

            new_empty_weight_kg = vehicle.veh_kg - vehicle.cargo_kg
            empty_increase_kg = new_empty_weight_kg - scenario.plf_ref_veh_empty_mass_kg
            new_cargo_cieling_kg = (
                scenario.gvwr_kg - empty_increase_kg + scenario.gvwr_credit_kg
            )

            # determine indices where lost cargo capacity is bounded in vehicle_weights
            # and get the corresponding indices for p_of_weights
            # based on current vehicle's new_cargo_cieling_lb and base_vehicle_gvwr_lb

            if empty_increase_kg >= scenario.gvwr_credit_kg:
                a = vehicle_weights_bins_kg - new_cargo_cieling_kg
                # print(a)
                minidx = (
                    np.where(
                        vehicle_weights_bins_kg == a[a > 0][0] + new_cargo_cieling_kg
                    )
                )[0][0]
                a = vehicle_weights_bins_kg - scenario.gvwr_kg
                maxidx = (
                    np.where(vehicle_weights_bins_kg == a[a > 0][0] + scenario.gvwr_kg)
                )[0][0]

                estimated_lost_payload_per_bin_kg = p_of_weights_normalized[
                    minidx:maxidx
                ] * (vehicle_weights_bins_kg[minidx:maxidx] - new_cargo_cieling_kg)
                estimated_lost_payload_kg = np.trapz(estimated_lost_payload_per_bin_kg)

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
        else:
            self.payload_cap_cost_multiplier = 1

    def set_fueling_dwell_time_cost(self, year_number: int, vehicle: Vehicle, scenario: Scenario, energy: Energy):
        """
        This function calculates the fueling dwell time cost for a vehicle based on fuel fill rate/charging power and shifts_per_year

        Args:
            vehicle (fastsim.vehicle): FASTSim vehicle object of analysis vehicle
            scenario (run_scenario.Scenario): Scenario object for current selection
        """
        self.net_fueling_dwell_time_hr_per_yr = []
        self.fueling_downtime_oppy_cost_dol_per_yr = []
        self.fueling_dwell_labor_cost_dol_per_yr = []
        dwellparams = np.array(
            [
                scenario.fdt_dwpt_fraction_power_pct,
                scenario.fdt_frac_full_charge_bounds,
                scenario.fdt_avg_overhead_hr_per_dwell_hr,
                scenario.downtime_oppy_cost_dol_per_hr,
            ]
        )
        assert any(
            dwellparams
        ), f"Missing parameters in {str(dwellparams)}: {np.isnan(dwellparams)}"

        if vehicle.veh_pt_type in ["BEV"]:
            self.full_dwell_hr = (1 - scenario.fdt_dwpt_fraction_power_pct) * (
                vehicle.ess_max_kwh / scenario.ess_max_charging_power_kw
            )
        elif vehicle.veh_pt_type in ["Conv"]:
            if scenario.fuel_type in ["gasoline"]:
                self.full_dwell_hr = (
                    vehicle.fs_kwh
                    / (gl.kwh_per_gge)
                    / scenario.fs_fueling_rate_gasoline_gpm
                ) / 60
            else:
                self.full_dwell_hr = (
                    vehicle.fs_kwh
                    / (gl.kwh_per_gge / gl.DieselGalPerGasGal)
                    / scenario.fs_fueling_rate_diesel_gpm
                ) / 60
        else:
            self.full_dwell_hr = (
                (1 - scenario.fdt_dwpt_fraction_power_pct)
                * (
                    vehicle.fs_kwh
                    / (gl.kwh_per_gge / gl.kgH2_per_gge)
                    / scenario.fs_fueling_rate_kg_per_min
                )
                / 60
            )

        # for year_number in range(scenario.vehicle_life_yr):
        self.trip_distance_mi = scenario.vmt[year_number] / self.shifts_per_year
        self.num_of_dwells = max(
            0,
            (
                (self.trip_distance_mi)
                * (1 - scenario.fdt_dwpt_fraction_power_pct)
                / energy.primary_fuel_range_mi
                - scenario.fdt_num_free_dwell_trips
            ),
        )

        if self.num_of_dwells != 0:
            self.remaining_dwells = self.num_of_dwells % 1
            if self.remaining_dwells < self.frac_of_fullcharge_bounds[0]:
                self.num_of_dwells += (
                    self.frac_of_fullcharge_bounds[0] - self.remaining_dwells
                )
            elif (
                self.frac_of_fullcharge_bounds[0]
                < self.remaining_dwells
                < self.frac_of_fullcharge_bounds[1]
            ):
                self.num_of_dwells += 0
            else:
                self.num_of_dwells += 1 - self.remaining_dwells

        if (self.num_of_dwells < 1 and not scenario.fdt_num_free_dwell_trips) or (
            scenario.fuel_type
        ):
            self.net_fueling_dwell_time_hr_per_yr = (
                scenario.vmt[year_number]
                * (1 - scenario.fdt_dwpt_fraction_power_pct)
                / energy.primary_fuel_range_mi
                * (self.full_dwell_hr + scenario.fdt_avg_overhead_hr_per_dwell_hr)
            )
        else:
            self.dwell_time_hr = (
                self.num_of_dwells * self.full_dwell_hr
                + ceil(self.num_of_dwells)
                * scenario.fdt_avg_overhead_hr_per_dwell_hr
            )
            self.net_fueling_dwell_time_hr_per_yr = (
                self.shifts_per_year
                * max(
                    0,
                    (
                        self.dwell_time_hr
                        - max(0, scenario.fdt_available_freetime_hr)
                    ),
                )
            )

        self.fueling_dwell_labor_cost_dol_per_yr = (
            self.net_fueling_dwell_time_hr_per_yr
            * scenario.labor_rate_dol_per_hr
        )
        self.fueling_downtime_oppy_cost_dol_per_yr = (
            self.net_fueling_dwell_time_hr_per_yr
            * scenario.downtime_oppy_cost_dol_per_hr
        )

    def set_mr_downtime_cost(self, year_number:int, vehicle: Vehicle, scenario:Scenario ):
        """
        This function calculates the Maintenance and Repair (M&R) downtime cost based on planned, unplanned, and tire replacement downtime inputs

        Args:
            a_vehicle (fastsim.vehicle): FASTSim object of the analysis vehicle
            scenario (run_scenario.Scenario): Scenario object for the current selection
        """
        self.mr_planned_downtime_hr = scenario.mr_planned_downtime_hr_per_yr[year_number]  # regular maintenance and inspections
        self.mr_unplanned_downtime_hr = scenario.mr_unplanned_downtime_hr_per_mi[year_number] * scenario.vmt[year_number]

        self.mr_tire_replacement_downtime_hr = (
            (scenario.vmt[year_number])
            / scenario.mr_avg_tire_life_mi
            * scenario.mr_tire_replace_downtime_hr_per_event
        )
        self.mr_downtime_hr_per_yr = (
            self.mr_planned_downtime_hr
            + self.mr_unplanned_downtime_hr
            + self.mr_tire_replacement_downtime_hr
        )
        self.mr_downtime_oppy_cost_dol_per_yr = (
            self.mr_downtime_hr_per_yr
            * scenario.downtime_oppy_cost_dol_per_hr
        )
