from pathlib import Path
from typing import List

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# from t3co.run import QuickStats
from scipy.interpolate import make_interp_spline
from mpl_toolkits.axes_grid1 import make_axes_locatable

# import calplot
from matplotlib import axes


class T3COCharts:
    t3co_results: pd.DataFrame
    results_guide: pd.DataFrame
    value_cols: List[float]

    def __init__(
        self,
        filename=None,
        results_df: pd.DataFrame = None,
        results_guide: str | Path = Path(__file__).parents[1]
        / "resources"
        / "visualization"
        / "t3co_outputs_guide.csv",
    ):
        if filename is not None:
            # print(f'using filename')
            self.from_file(filename)
        else:
            self.from_df(results_df)

        # print(f't3co_results: {self.t3co_results}')
        self.parse_scenario_name()

        self.results_guide = pd.read_csv(results_guide)
        self.value_cols = self.results_guide.loc[
            self.results_guide["data_type"] == "float", "t3co_output_parameter"
        ].values

        self.group_columns = [
            "None",
            "vehicle_weight_class",
            "veh_year",
            "vehicle_type",
            "tech_progress",
            "vehicle_fuel_type",
        ]
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
            "fueling_dwell_labor_cost_dol",
            "fueling_downtime_oppy_cost_dol",
            "mr_downtime_oppy_cost_dol",
            # "discounted_downtime_oppy_cost_dol",
            "payload_capacity_cost_dol",
            # "discounted_tco_dol",
        ]
        self.t3co_results = self.t3co_results.convert_dtypes()
        for costcol in self.cost_cols:
            self.t3co_results[costcol] = self.t3co_results[costcol].astype(float)
            # print(self.t3co_results[costcol].dtype)
        self.t3co_results["discounted_tco_dol"] = self.t3co_results[
            "discounted_tco_dol"
        ].astype(float)
        # for cost_col in self.cost_cols:
        self.cost_col_names = self.results_guide["full_form"][
            self.results_guide["t3co_output_parameter"].isin(self.cost_cols)
        ]

        # print(self.cost_col_names)

    def from_file(
        self,
        filename: str | Path = None,
    ):
        self.t3co_results = pd.read_csv(filename)

    def from_df(self, results_df):
        self.t3co_results = results_df

    def to_df(self):
        return self.t3co_results

    def parse_scenario_name(self):
        # Class 8 Sleeper cab low roof (Diesel, 2035, no program)
        weight_class_ranges = {
            "1": [0, 2722],
            "2a": [2722, 3856],
            "2b": [3856, 4536],
            "3": [4536, 6350],
            "4": [6350, 7257],
            "5": [7257, 8845],
            "6": [8845, 11793],
            "7": [11793, 14969],
            "8": [14969, 50000],
        }
        self.t3co_results["vehicle_weight_class"] = ""
        for i in range(len(self.t3co_results)):
            for wt_class, lims in weight_class_ranges.items():
                if (
                    float(self.t3co_results["scenario_gvwr_kg"][i]) > lims[0]
                    and float(self.t3co_results["scenario_gvwr_kg"][i]) <= lims[1]
                ):
                    self.t3co_results.loc[[i], "vehicle_weight_class"] = (
                        "Class " + wt_class
                    )
                    break

        # print(self.t3co_results['vehicle_weight_class'])

        self.t3co_results["vehicle_type"] = (
            self.t3co_results["scenario_name"]
            .str.split("(")
            .apply(lambda x: " ".join(x[0].split(" ")[2:]))
        )
        # print( self.t3co_results['vehicle_type'] )

        self.t3co_results["tech_progress"] = (
            self.t3co_results["scenario_name"]
            .str.split("(")
            .apply(lambda x: x[1].split(",")[-1].split(")")[0])
        )
        self.t3co_results["vehicle_fuel_type"] = (
            self.t3co_results["scenario_name"]
            .str.split("(")
            .apply(lambda x: x[1].split(",")[0])
        )
        # self.t3co_results['vehicle_weight_class'] =  self.t3co_results['scenario_name'].str.split[" "]
        # print(self.t3co_results['tech_progress'])
        # print(self.t3co_results['vehicle_fuel_type'])

    def generate_tco_plots(
        self,
        x_group_col,
        y_group_col,
        subplot_group_col="vehicle_fuel_type",
        points=300,
        bins=20,
    ):
        disc_tco_label = self.results_guide["full_form"][
            self.results_guide["t3co_output_parameter"] == "discounted_tco_dol"
        ]
        legend_cols = list(disc_tco_label) + list(self.cost_col_names)
        x_groups = (
            self.t3co_results[x_group_col].unique() if x_group_col != "None" else [0]
        )
        print(f"x_groups: {x_groups}")
        y_groups = (
            self.t3co_results[y_group_col].unique() if y_group_col != "None" else [0]
        )
        print(f"y_groups: {y_groups}")
        fontsize = 25
        if (x_group_col == "None" and y_group_col == "None") or (
            len(x_groups) == 1 and len(y_groups) == 1
        ):
            fig, ax = plt.subplots()
            # bottom = np.zeros(len(groups))
            # width = 0.15
            self.t3co_results.plot.bar(
                y=self.cost_cols, stacked=True, figsize=(8, 8), ax=ax
            )
            # self.t3co_results.plot.line(x = ['scenario_name'], y= ['discounted_tco_dol'], ax= ax)
            ax.set_xlabel("Scenarios")
            ax.set_xticklabels(self.t3co_results["scenario_name"])
            ax.set_ylabel("Cost [$\$$]")
            ax.minorticks_on()

            x_values = range(
                len(self.t3co_results)
            )  # X-values based on the index of the DataFrame
            y_values = self.t3co_results["discounted_tco_dol"]

            plt.scatter(
                x_values,
                y_values,
                color="red",
                label=disc_tco_label,
                zorder=3,
                marker="D",
            )
            # print(f'legend_cols: {legend_cols}')
            ax.legend(legend_cols, bbox_to_anchor=(1, 0.8))
            # ax.legend()
            ax.set_title("Total Cost Of Ownership Breakdown")
            fig = ax.get_figure()

        elif len(x_groups) > 1 and len(y_groups) == 1:
            # print(f'x_groups: {x_groups}')

            fontsize = 25
            # plt.rcParams['font.size'] = 25

            fig, ax = plt.subplots(
                1, len(x_groups), sharey=True, figsize=(len(x_groups) * 7 + 7, 10)
            )
            # print(self.t3co_results.loc[ self.t3co_results[x_group_col] == x_groups[0]])

            maxn = 4
            # print(f'maxn = {maxn}')
            for i in range(len(x_groups)):
                self.t3co_results.loc[
                    self.t3co_results[x_group_col] == x_groups[i]
                ].plot.bar(
                    x=subplot_group_col,
                    y=self.cost_cols,
                    stacked=True,
                    ax=ax[i],
                    legend=False,
                    width=0.4,
                )
                ax[i].set_xlim(-0.5, maxn - 0.5)

                ax[i].set_xlabel(f"{x_groups[i]}", fontsize=fontsize, labelpad=10)
                # ax[i].set_ylabel("Cost [$\$$]", fontsize = fontsize)
                ax[i].tick_params(labelsize=fontsize)
                x_values = range(
                    len(
                        self.t3co_results.loc[
                            self.t3co_results[x_group_col] == x_groups[i]
                        ]
                    )
                )  # X-values based on the index of the DataFrame
                y_values = self.t3co_results.loc[
                    self.t3co_results[x_group_col] == x_groups[i], "discounted_tco_dol"
                ]
                ax[i].scatter(
                    x_values,
                    y_values,
                    color="red",
                    label=disc_tco_label,
                    zorder=3,
                    marker="D",
                )

                # if i==len(x_groups)-1:
                #     ax[i].legend(legend_cols, bbox_to_anchor=(1, 0.8))

            handles, labels = [], []
            for ax1 in ax:
                for h, l in zip(*ax1.get_legend_handles_labels()):
                    handles.append(h)
                    labels.append(l)

            fig.supylabel("Cost [$\$$]", fontsize=fontsize)
            fig.supxlabel(
                self.results_guide.loc[
                    self.results_guide["t3co_output_parameter"] == subplot_group_col,
                    "full_form",
                ].values[0],
                fontsize=fontsize,
            )
            fig.suptitle("Total Cost Of Ownership Breakdown", fontsize=fontsize * 1.25)
            fig.legend(
                handles,
                legend_cols,
                loc="center right",
                bbox_to_anchor=(1.25, 0.5),
                ncol=1,
                fontsize=fontsize,
            )

            # ax[i].set_figure(fig)
            # print(ax[0].ArtistList)

        elif len(y_groups) > 1 and len(x_groups) == 1:
            # print(f'y_groups: {y_groups}')

            fontsize = 25

            fig, ax = plt.subplots(
                len(y_groups), sharex=True, figsize=(len(y_groups) * 7 + 4, 17)
            )

            maxn = 4
            # print(f'maxn = {maxn}')
            for i in range(len(y_groups)):
                self.t3co_results.loc[
                    self.t3co_results[y_group_col] == y_groups[i]
                ].plot.bar(
                    x=subplot_group_col,
                    y=self.cost_cols,
                    stacked=True,
                    ax=ax[i],
                    legend=False,
                    width=0.25,
                )
                ax[i].set_xlim(-0.5, maxn - 0.5)

                ax[i].set_xlabel(f"{y_groups[i]}", fontsize=fontsize, labelpad=10)
                # ax[i].set_ylabel("Cost [$\$$]", fontsize = fontsize)
                ax[i].tick_params(labelsize=fontsize)
                x_values = range(
                    len(
                        self.t3co_results.loc[
                            self.t3co_results[y_group_col] == y_groups[i]
                        ]
                    )
                )  # X-values based on the index of the DataFrame
                y_values = self.t3co_results.loc[
                    self.t3co_results[y_group_col] == y_groups[i], "discounted_tco_dol"
                ]
                ax[i].scatter(
                    x_values,
                    y_values,
                    color="red",
                    label=disc_tco_label,
                    zorder=3,
                    marker="D",
                )

            handles, labels = [], []
            for ax1 in ax:
                for h, l in zip(*ax1.get_legend_handles_labels()):
                    handles.append(h)
                    labels.append(l)

            fig.supylabel("Cost [$\$$]", fontsize=fontsize)
            fig.supxlabel(
                self.results_guide.loc[
                    self.results_guide["t3co_output_parameter"] == subplot_group_col,
                    "full_form",
                ].values[0],
                fontsize=fontsize,
            )
            fig.suptitle("Total Cost Of Ownership Breakdown", fontsize=fontsize * 1.25)
            fig.legend(
                handles,
                legend_cols,
                loc="center right",
                bbox_to_anchor=(1.25, 0.5),
                ncol=1,
                fontsize=fontsize,
            )

            # ax[i].set_figure(fig)
            # print(ax[0].ArtistList)

        else:
            fig, ax = plt.subplots(
                len(y_groups),
                len(x_groups),
                sharey=True,
                sharex=True,
                figsize=(len(y_groups) * 9 + 3, len(x_groups) * 7 + 7),
            )
            maxn = 4
            # print(f'maxn = {maxn}')
            plt.ticklabel_format(style="plain")

            for i in range(len(y_groups)):
                for j in range(len(x_groups)):
                    print(f"i = {i} j={j}")
                    ax[i][j].set_xlim(-0.5, maxn - 0.5)
                    if i == len(y_groups) - 1:
                        ax[i][j].set_xlabel(
                            f"{x_groups[j]}", fontsize=fontsize, labelpad=10
                        )
                    if j == len(x_groups) - 1:
                        ax2 = ax[i][j].twinx()
                        # ax2.get_yaxis().set_ticks([])
                        ax2.set_ylabel(f"{y_groups[i]}", fontsize=fontsize, labelpad=10)
                    ax[i][j].tick_params(axis="x", labelsize=fontsize, labelrotation=90)
                    ax[i][j].tick_params(axis="y", labelsize=fontsize, labelrotation=0)

                    if self.t3co_results.loc[
                        (self.t3co_results[y_group_col] == y_groups[i])
                        & (self.t3co_results[x_group_col] == x_groups[j])
                    ].empty:
                        continue

                    self.t3co_results.loc[
                        (self.t3co_results[y_group_col] == y_groups[i])
                        & (self.t3co_results[x_group_col] == x_groups[j])
                    ].plot.bar(
                        x=subplot_group_col,
                        y=self.cost_cols,
                        stacked=True,
                        ax=ax[i][j],
                        legend=False,
                        width=0.25,
                    )
                    x_values = range(
                        len(
                            self.t3co_results.loc[
                                (self.t3co_results[y_group_col] == y_groups[i])
                                & (self.t3co_results[x_group_col] == x_groups[j])
                            ]
                        )
                    )  # X-values based on the index of the DataFrame
                    y_values = self.t3co_results.loc[
                        (self.t3co_results[y_group_col] == y_groups[i])
                        & (self.t3co_results[x_group_col] == x_groups[j]),
                        "discounted_tco_dol",
                    ]
                    ax[i][j].scatter(
                        x_values,
                        y_values,
                        color="red",
                        label=disc_tco_label,
                        zorder=3,
                        marker="D",
                    )

            handles, labels = [], []
            for ax1 in ax[0]:
                for h, l in zip(*ax1.get_legend_handles_labels()):
                    handles.append(h)
                    labels.append(l)

            fig.supylabel("Cost [$\$$]", fontsize=fontsize)
            fig.supxlabel(
                self.results_guide.loc[
                    self.results_guide["t3co_output_parameter"] == subplot_group_col,
                    "full_form",
                ].values[0],
                fontsize=fontsize,
            )
            fig.suptitle("Total Cost Of Ownership Breakdown", fontsize=fontsize * 1.25)
            fig.legend(
                handles,
                legend_cols,
                loc="center right",
                bbox_to_anchor=(1.25, 0.5),
                ncol=1,
                fontsize=fontsize,
            )

        return fig
