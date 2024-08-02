# %%

import warnings
from math import ceil
from pathlib import Path

import fastsim
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import trapz
from scipy.stats import gaussian_kde
import os
from t3co.run import Global as gl
from t3co.run import run_scenario

# TODO: think about this stuff
# Thoughts about how to improve this:
# 1 - maybe $/lb should be in terms of profit and not raw shipping fees
# 2 - could consider scaling number of vehicles by some function of opportunity cost
#     such that fungible goods are shipped at same rate.  This would bump up capital
#     expenses but lower lost revenue.  At the other end, we could just lose some revenue.
#     I would think they'd work out pretty similarly, but it'd be interesting to compare
#     two approaches.


class OpportunityCost:
    """
    This class is used to calculate the different opportunity costs for a scenario and vehicle
    - Payload Capacity Cost Multiplier
    - Fueling Downtime Cost
    - Maintenance and Repair Downtime Cost
    """

    def __init__(self, scenario, range_dict=None, **kwargs):
        """
        Initializes OpportunityCost object using Scenario object, range_dict (from fueleconomy module), and other arguments

        Args:
            scenario (run_scenario.Scenario): Scenario object
            range_dict (dict, optional): dictionary containing primary_fuel_range_mi from fueleconomy.get_range_mi function. Defaults to None.
        """

        # maybe this should be on a profit basis (it's currently not)
        ### All params below here are experimental and not to be used for now
        self.cost_per_lb_mi = kwargs.pop("cost_per_lb_mi", 0.0003)
        # trip distance[mi] for typical point A to point B trip
        # self.d_trip_mi = kwargs.pop('d_trip_mi', 500)
        # self.d_trip_mi = scenario.vmt[0]/scenario.shifts_per_year
        self.payload_cap_cost_multiplier = None
        # distance[mi] that can be traveled with a full battery.
        # self.total_range_mi = kwargs.pop('d_fullbatt_mi', 300)
        if range_dict:
            self.total_range_mi = range_dict["primary_fuel_range_mi"]
            # print('primary_fuel_range_mi')
        else:
            self.total_range_mi = scenario.target_range_mi
        # print(range_dict)
        # self.cycle_distance_mi = range_dict['cycle_distance_mi']
        # average vehicle speed[mph] over trip, should come from FASTSim
        # self.v_mean_mph = range_dict['mean_cyc_speed_mph']
        # driver hourly labor rate[$/hr].
        # self.labor_rate_dol_per_hr = kwargs.pop('labor_rate_dol_per_hr', 30.60) # labor cost from Alicia.  Expect a report that can be cited for this.
        self.labor_rate_dol_per_hr = scenario.fdt_oppy_cost_dol_per_hr
        # self.free_dwell_time_hr = scenario.fdt_available_freetime_hr
        # dwell time [hr] driven by non-charging needs (e.g. required work breaks) that can be used for charging.
        # self.free_dwell_time_hr = kwargs.pop('free_dwell_time_hr', 3)
        # fraction of dwell time that can actually be used for charging
        # self.dwell_time_efficiency = kwargs.pop('dwell_time_efficiency', 1.)
        if scenario.activate_tco_fueling_dwell_time_cost:
            self.dwell_time_efficiency = scenario.dlf_dwell_efficiency_pct
            self.time_available_charge_hr = scenario.dlf_time_available_charge_hr
            self.dwell_overhead_hr = scenario.fdt_avg_overhead_hr_per_dwell_hr
            self.frac_of_fullcharge_bounds = list(
                np.float_(scenario.fdt_frac_full_charge_bounds.strip(" ][").split(","))
            )
            self.shifts_per_year = list(
                np.float_(scenario.shifts_per_year.strip(" ][").split(","))
            )

        self.payload_cap_cost_multiplier = 0
        self.net_dwell_time_hr = np.zeros(scenario.vehicle_life_yr)
        self.dwell_time_cost_Dol = np.zeros(scenario.vehicle_life_yr)
        self.net_MR_downtime_hrPerYr = np.zeros(scenario.vehicle_life_yr)
        self.net_MR_downtime_oppcosts_DolPerYr = np.zeros(scenario.vehicle_life_yr)

        # rate[kW] at which battery is recharged
        self.charge_rate_kW = kwargs.pop("charge_rate_kW", 200)
        # battery capacity [kilowatt-hours]
        self.battery_capacity_kWhr = kwargs.pop("batt_cap_kW_hr", 300)
        # number of full battery trips that don't incur dwell time penalty
        # battery is allowed `num_free_trips` charging events without penalty
        # self.num_free_trips = kwargs.pop('num_free_trips', 1.)
        self.num_free_trips = scenario.fdt_num_free_dwell_trips
        # number of weight weight bins
        self.num_bins = kwargs.pop("num_bins", 1_000)

        if len(kwargs) > 0:
            warnings.warn(f"Invalid kwargs: {list(kwargs.keys())}")

        # weight distribution file to load
        self.wt_dist_file = kwargs.pop(
            "wt_dist_file",
            Path(os.path.abspath(__file__)).parents[1] / "resources" / "auxiliary" / "tractorweightvars.csv",
        )
        self.df_veh_wt = pd.read_csv(self.wt_dist_file, index_col=0)

    def set_kdes(self, scenario, bw_method=0.15, verbose=False):
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
        self.vehicle_weights_bins_lb = np.linspace(
            self.df_veh_wt["WEIGHTAVG"].min(), self.df_veh_wt["WEIGHTAVG"].max(), 1000
        )
        self.vehicle_weights_bins_kg = gl.lbs_to_kgs(self.vehicle_weights_bins_lb)

        # get probability of each vehicle weight
        self.p_of_weights = kernel(self.vehicle_weights_bins_lb)
        # self.p_of_weights_normalized =

        probability_payload = pd.DataFrame(
            [self.vehicle_weights_bins_kg, self.p_of_weights],
            index=["vehicle_weights_bins_kg", "p_of_weights"],
        ).T
        probability_payload.to_csv(Path(self.wt_dist_file).parents[0]/"payload_pdf.csv")
        normalization_factor = probability_payload[
            probability_payload["vehicle_weights_bins_kg"].between(
                scenario.plf_ref_veh_empty_mass_kg, scenario.gvwr_kg
            )
        ]["p_of_weights"].sum()
        self.p_of_weights_normalized = self.p_of_weights / normalization_factor
        # print(f'plf_ref_veh_empty_mass_kg {scenario.plf_ref_veh_empty_mass_kg}')

    def get_payload_loss_factor(
        self,
        a_vehicle: fastsim.vehicle,
        scenario,
        plots=False,
        plots_dir=None,
    ):
        """
        This method runs teh kernel density estimation function set_kdes and calculates the payload capacity loss factor (payload_cap_cost_multiplier) \
            of the new vehicle compared to a conventional vehicle's reference empty weight.

        Args:
            a_vehicle (fastsim.vehicle): FASTSim vehicle object of the analysis vehicle
            scenario (run_scenario.Scenario): Scenario object of current selection
            plots (bool, optional): if True, creates histogram of KDE weight bins. Defaults to False.
            plots_dir (str, optional): output diretory for saving plot figure. Defaults to None.
        """
        self.set_kdes(scenario, verbose=False)

        new_empty_weight_kg = a_vehicle.veh_kg - a_vehicle.cargo_kg
        empty_increase_kg = (
            new_empty_weight_kg - scenario.plf_ref_veh_empty_mass_kg
        )
        new_cargo_cieling_kg = (
            scenario.gvwr_kg - empty_increase_kg + scenario.gvwr_credit_kg
        )
        # print(new_cargo_cieling_lb)

        # determine indices where lost cargo capacity is bounded in vehicle_weights
        # and get the corresponding indices for p_of_weights
        # based on current vehicle's new_cargo_cieling_lb and base_vehicle_gvwr_lb

        if empty_increase_kg >= scenario.gvwr_credit_kg:
            a = self.vehicle_weights_bins_kg - new_cargo_cieling_kg
            # print(a)
            minidx = (
                np.where(
                    self.vehicle_weights_bins_kg == a[a > 0][0] + new_cargo_cieling_kg
                )
            )[0][0]
            a = self.vehicle_weights_bins_kg - scenario.gvwr_kg
            maxidx = (
                np.where(self.vehicle_weights_bins_kg == a[a > 0][0] + scenario.gvwr_kg)
            )[0][0]
            # print(f'Vehicle bin limits: {self.vehicle_weights_bins_kg[minidx]}, {self.vehicle_weights_bins_kg[maxidx]}')

            # print( f' PDF bounds: {minidx}, {maxidx}' )
            # print( f' PDF weight bounds: {self.vehicle_weights_bins_lb[minidx]}, {self.vehicle_weights_bins_lb[maxidx]}' )

            estimated_lost_payload_per_bin_kg = self.p_of_weights_normalized[
                minidx:maxidx
            ] * (self.vehicle_weights_bins_kg[minidx:maxidx] - new_cargo_cieling_kg)
            # estimated_lost_payload_lb = sum(estimated_lost_payload_per_bin_lb)
            estimated_lost_payload_kg = trapz(estimated_lost_payload_per_bin_kg)
            # print(f'estimated_lost_payload_kg: {estimated_lost_payload_kg}')

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

        def make_plots(save_dir=None):
            """
            This function generates a histogram of the payload KDE weight distribution

            Args:
                save_dir (str, optional): Output directory path to save plot figure. Defaults to None.
            """
            if save_dir and not Path(save_dir).exists():
                save_dir.mkdir()

            fig, ax = plt.subplots(figsize=(9, 6))
            ax.hist(
                gl.lbs_to_kgs(self.df_veh_wt["WEIGHTAVG"]),
                bins=50,
                label="WEIGHTAVG: operating weight [kg]",
            )
            ax2 = ax.twinx()
            ax2.plot(
                self.vehicle_weights_bins_kg,
                self.p_of_weights,
                color="red",
                linewidth=3,
                label="KDE",
            )
            ax2.fill_between(
                x=self.vehicle_weights_bins_kg[minidx:maxidx],
                y1=self.p_of_weights[minidx:maxidx],
                y2=[0] * len(self.p_of_weights[minidx:maxidx]),
                color="red",
                alpha=0.3,
                label=f"estimated cargo lost [kg]: {round(estimated_lost_payload_kg)}",
            )
            ax2.axvline(
                scenario.gvwr_kg,
                label=f"GVWR [kg] {round(scenario.gvwr_kg)}",
                color="orange",
            )
            ax2.axvline(
                new_cargo_cieling_kg,
                label=f"GVWR + credit - empty weight increase [kg] : {round(scenario.gvwr_kg)} + {round(scenario.gvwr_credit_kg)}  - {round(empty_increase_kg)} = {round(new_cargo_cieling_kg)}",
                color="purple",
            )
            fig.suptitle(
                f"payload cost multiplier: {round(self.payload_cap_cost_multiplier,2)}"
            )
            fig.legend()
            plt.show()

        if plots:
            make_plots(plots_dir)

    # Old Dwell time calculation
    # def get_dwell_loss_factor(self,
    #         a_vehicle:fastsim.vehicle,
    #         scenario) :
    #     self.dwell_time_hr = max(
    #     0, self.d_trip_mi / self.total_range_mi - self.num_free_trips) * \
    #     (a_vehicle.ess_max_kwh / a_vehicle.ess_max_kw)
    #     # (nominal time + additional non-driving time to charge) / nominal time

    #     # TODO: need to add separate labor and payload dwell penalties starting here
    #     self.net_dwell_time_hr = max(
    #         0, (self.dwell_time_hr - max(0, self.free_dwell_time_hr)) * self.dwell_time_efficiency)

    #     # number of original trip time durations after correcting for EV time penalty
    #     # (e.g. 1.8 means 80% longer trip duration)
    #     self.dwell_time_factor = max(1, (self.d_trip_mi / self.v_mean_mph + self.net_dwell_time_hr) /
    #         (self.d_trip_mi / self.v_mean_mph))

    def get_dwell_time_cost(self, a_vehicle: fastsim.vehicle, scenario):
        """
        This function calculates the fueling dwell time cost for a vehicle based on fuel fill rate/charging power and shifts_per_year

        Args:
            a_vehicle (fastsim.vehicle): FASTSim vehicle object of analysis vehicle
            scenario (run_scenario.Scenario): Scenario object for current selection
        """
        self.dwell_time_cost_Dol, self.total_dwell_time_hr = 0, 0
        self.net_dwell_time_hr = []
        self.dwell_time_cost_Dol = []
        dwellparams = np.array(
            [
                scenario.fdt_dwpt_fraction_power_pct,
                scenario.fdt_frac_full_charge_bounds,
                scenario.fdt_avg_overhead_hr_per_dwell_hr,
                scenario.fdt_oppy_cost_dol_per_hr,
            ]
        )
        assert any(
            dwellparams
        ), f"Missing parameters in {str(dwellparams)}: {np.isnan(dwellparams)}"

        if a_vehicle.veh_pt_type in ["BEV"]:
            self.full_dwell_hr = (1 - scenario.fdt_dwpt_fraction_power_pct) * (
                a_vehicle.ess_max_kwh / scenario.ess_max_charging_power_kw
            )
        elif a_vehicle.veh_pt_type in ["Conv"]:
            if scenario.fuel_type in ["gasoline"]:
                self.full_dwell_hr = (
                    a_vehicle.fs_kwh
                    / (gl.kwh_per_gge)
                    / scenario.fs_fueling_rate_gasoline_gpm
                ) / 60
            else:
                self.full_dwell_hr = (
                    a_vehicle.fs_kwh
                    / (gl.kwh_per_gge / gl.DieselGalPerGasGal)
                    / scenario.fs_fueling_rate_diesel_gpm
                ) / 60
        else:
            self.full_dwell_hr = (
                (1 - scenario.fdt_dwpt_fraction_power_pct)
                * (
                    a_vehicle.fs_kwh
                    / (gl.kwh_per_gge / gl.kgH2_per_gge)
                    / scenario.fs_fueling_rate_kg_per_min
                )
                / 60
            )

        for i in range(scenario.vehicle_life_yr):
            # self.shifts_per_year = (scenario.vmt[i])/ self.cycle_distance_mi
            self.d_trip_mi = scenario.vmt[i] / self.shifts_per_year[i]
            self.num_of_dwells = max(
                0,
                (
                    (self.d_trip_mi)
                    * (1 - scenario.fdt_dwpt_fraction_power_pct)
                    / self.total_range_mi
                    - self.num_free_trips
                ),
            )
            # print(f'num_of_dwells: {self.num_of_dwells}\n vmt: {scenario.vmt[i]}')
            # print(f'd_trip_mi: {self.d_trip_mi}')
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
            # else:

            if (self.num_of_dwells < 1 and not self.num_free_trips) or (scenario.fuel_type):
                self.net_dwell_time_hr.append(
                    scenario.vmt[i]
                    * (1 - scenario.fdt_dwpt_fraction_power_pct)
                    / self.total_range_mi
                    * (self.full_dwell_hr + self.dwell_overhead_hr)
                )
            else:
                self.dwell_time_hr = (
                    self.num_of_dwells * self.full_dwell_hr
                    + ceil(self.num_of_dwells) * self.dwell_overhead_hr
                )
                self.net_dwell_time_hr.append(
                    self.shifts_per_year[i]
                    * max(
                        0, (self.dwell_time_hr - max(0, scenario.fdt_available_freetime_hr))
                    )
                )

            self.dwell_time_cost_Dol.append(self.net_dwell_time_hr[i] * self.labor_rate_dol_per_hr)
            self.total_dwell_time_hr += self.net_dwell_time_hr[i]

        # self.dwell_time_factor = max(1, (self.d_trip_mi / self.v_mean_mph + self.net_dwell_time_hr[i]) /
        #     (self.d_trip_mi / self.v_mean_mph))

    # def get_dwell_time_cost #Old calculation
    #           (self,
    #         a_vehicle:fastsim.vehicle,
    #         scenario):

    #     self.dwell_time_hr = 0 if self.d_trip_mi< self.total_range_mi else \
    #                           max((self.d_trip_mi - self.total_range_mi)* (a_vehicle.ess_max_kwh / a_vehicle.ess_max_kw), scenario.dlf_min_charge_time_hr)
    #     self.time_full_charge_hr = self.total_range_mi * a_vehicle.ess_max_kwh / a_vehicle.ess_max_kw
    #     self.time_frac_charge_hr = self.time_full_charge_hr *(1- (self.dwell_time_hr/self.time_full_charge_hr - floor(self.dwell_time_hr/self.time_full_charge_hr) ))
    #     self.dwell_time_hr = self.dwell_time_hr if self.time_frac_charge_hr < self.time_available_charge_hr else (self.dwell_time_hr+ self.time_frac_charge_hr)

    #     self.dwell_time_cost_Dol = self.dwell_time_hr/self.dwell_time_efficiency * self.labor_rate_dol_per_hr
    #     print(f'Dwell time hr per year: {self.dwell_time_hr}')
    #     print(f'Dwell cost dol: {self.dwell_time_cost_Dol}')

    def get_M_R_downtime_cost(self, a_vehicle: fastsim.vehicle, scenario):
        """
        This function calculates the Maintenance and Repair (M&R) downtime cost based on planned, unplanned, and tire replacement downtime inputs

        Args:
            a_vehicle (fastsim.vehicle): FASTSim object of the analysis vehicle
            scenario (run_scenario.Scenario): Scenario object for the current selection
        """
        self.planned_downtime_hr = [
            scenario.mr_planned_downtime_hr_per_yr for _ in range(scenario.vehicle_life_yr)
        ]  # regular maintenance and inspections
        self.unplanned_downtime_hr = [
            scenario.mr_unplanned_downtime_hr_per_mi[i] * scenario.vmt[i]
            for i in range(scenario.vehicle_life_yr)
        ]  # increases with age
        self.tire_replacement_downtime_hr = [
            (scenario.vmt[i])
            / scenario.mr_avg_tire_life_mi
            * scenario.mr_tire_replace_downtime_hr_per_event
            for i in range(scenario.vehicle_life_yr)
        ]
        self.net_MR_downtime_hrPerYr = np.array(
            [
                self.planned_downtime_hr[i]
                + self.unplanned_downtime_hr[i]
                + self.tire_replacement_downtime_hr[i]
                for i in range(scenario.vehicle_life_yr)
            ]
        )
        self.net_MR_downtime_oppcosts_DolPerYr = (
            self.net_MR_downtime_hrPerYr * self.labor_rate_dol_per_hr
        )
        # print(f'Total M&R downtime hr: {self.net_MR_downtime_hr}')
        # print(f'M&R Downtime cost Dol: {self.net_MR_downtime_oppcosts_Dol}')


# %%
def main():
    """
    Runs the opportunity cost module as a standalone code based on input vehicles and scenarios
    """
    print("opportunity cost main()")
    vehicles_file = Path(
        "./resources/inputs/tda_example/TDA_FY22_vehicle_model_assumptions.csv"
    )
    scenarios_file = Path(
        "./resources/inputs/tda_example/TDA_FY22_scenario_assumptions.csv"
    )
    s, c = run_scenario.get_scenario_and_cycle(33, scenarios_file)
    v = run_scenario.get_vehicle(33, vehicles_file)
    oc = OpportunityCost(v, s)

    print("GVWRlb", gl.kg_to_lbs(s.gvwr_kg))
    print("GvwrCreditlb", gl.kg_to_lbs(s.gvwr_credit_kg))
    print("veh_lb", gl.kg_to_lbs(v.veh_kg))
    print("ess_mass_lb", gl.kg_to_lbs(v.ess_mass_kg))
    print("original empty lb", gl.kg_to_lbs(v.veh_kg - v.cargo_kg))
    run_scenario.set_max_battery_kwh(v, v.ess_max_kwh * 2)
    print("next ess_mass_lb", gl.kg_to_lbs(v.ess_mass_kg))
    print("next veh_lb", gl.kg_to_lbs(v.veh_kg))

    print("GVWRlb", oc.GVWRlb)
    print("gvwr_credit_lb", oc.gvwr_credit_lb)
    print("oc.base_vehicle_veh_lb", gl.kg_to_lbs(oc.base_vehicle_veh_kg))
    print("oc.base_vehicle_cargo_lb", gl.kg_to_lbs(oc.base_vehicle_cargo_kg))
    print("oc.original_empty_lb", gl.kg_to_lbs(oc.reference_vehicle_empty_kg))

    plf = oc.get_payload_loss_factor(v, plots=True)
    print(plf)
    oc.get_dwell_time_cost(v, s)
    print(oc.dwell_time_cost)
    print(oc.net_dwell_time_hr)
    print(oc.__dict__["payload_cap_cost_multiplier"])
    oc.get_M_R_downtime_cost(v, s)


# %%
if __name__ == "__main__":
    oc = main()
