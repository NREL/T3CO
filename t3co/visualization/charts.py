from pathlib import Path
from typing import List

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
# from t3co.run import QuickStats
from scipy.interpolate import make_interp_spline
from mpl_toolkits.axes_grid1 import make_axes_locatable
# import calplot


class T3COCharts:
    t3co_results: pd.DataFrame
    results_guide: pd.DataFrame
    value_cols: List[float]

    def __init__(self):
        pass

    def from_file(
        self,
        filename: str | Path,
        results_guide: str | Path = Path(__file__).parents[1]
        / "resources" / "visualization"
        / "t3co_outputs_guide.csv",
    ):
        self.t3co_results = pd.read_csv(filename)

        self.results_guide = pd.read_csv(results_guide)
        self.value_cols = self.results_guide.loc[
            self.results_guide["data_type"] == "float", "t3co_output_parameter"
        ].values

        self.group_columns = [ "veh_year", "veh_pt_type"]
        self.cost_cols = [
            "glider_cost_dol",
            "fuel_converter_cost_dol",
            "fuel_storage_cost_dol",
            "motor_control_power_elecs_cost_dol",
            "plug_cost_dol",
            "battery_cost_dol",
            "purchase_tax_dol",
            # "msrp_total_dol",
            "total_fuel_cost_dol",
            "total_maintenance_cost_dol",
            "insurance_cost_dol",
            "residual_cost_dol",
            # "total_fueling_dwell_time_hr",
            # "total_mr_downtime_hr",
            # "total_downtime_hr",
            "fueling_dwell_labor_cost_dol",
            "fueling_downtime_oppy_cost_dol",
            "mr_downtime_oppy_cost_dol",
            # "discounted_downtime_oppy_cost_dol",
            "payload_capacity_cost_dol",
            # "discounted_tco_dol",
        ]
        # for cost_col in self.cost_cols:
        self.cost_col_names = self.results_guide['full_form'][self.results_guide["t3co_output_parameter"].isin(self.cost_cols)]

        print(self.cost_col_names)
        return self.t3co_results

    def generate_tco_plots(self, group_col, points=300, bins=20):
        
        if group_col!="None":
            # groups = tuple(set(self.t3co_results[group_col]))
            # print(f'groups: {groups}')
            fig, ax = plt.subplots()
            # bottom = np.zeros(len(groups))
            # width = 0.15
            ax = self.t3co_results.plot.bar(y= self.cost_cols, stacked=True, figsize=(8,8))
            # self.t3co_results.plot.line(x = ['scenario_name'], y= ['discounted_tco_dol'], ax= ax)
            ax.set_xlabel(f"Scenarios")
            ax.set_xticklabels(self.t3co_results['scenario_name'])
            ax.set_ylabel("Cost [$\$$]")
            ax.minorticks_on()

            x_values = range(len(self.t3co_results))  # X-values based on the index of the DataFrame
            y_values = self.t3co_results['discounted_tco_dol']

            disc_tco_label = self.results_guide['full_form'][self.results_guide["t3co_output_parameter"]=='discounted_tco_dol']
            plt.scatter(x_values, y_values, color='red', label=disc_tco_label, zorder=3, marker='D',)
            legend_cols = list(disc_tco_label) + list(self.cost_col_names)
            print(f'legend_cols: {legend_cols}')
            ax.legend(legend_cols, bbox_to_anchor=(1, 0.8))
            # ax.legend()
            ax.set_title("Total Cost Of Ownership Breakdown")
            fig = ax.get_figure()
        # else:
            # fig, ax = plt.subplots()
            # bottom = 0
            # width = 0.15
            # for i in range(len(self.cost_cols)):
            #     p = ax.bar(groups, self.t3co_results[self.cost_cols[i]], width, label=self.cost_col_names[i], bottom=bottom)
            #     bottom += self.t3co_results[self.cost_cols[i]]
            
            # ax.set_xlabel(f"Grouped by {group_col}")
            # ax.set_ylabel("Cost [$\$$]")
            # ax.legend()
            # ax.title("Total Cost Of Ownership Breakdown")
        return fig

    