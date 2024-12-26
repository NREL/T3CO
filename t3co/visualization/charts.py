from pathlib import Path
from textwrap import wrap
from typing import List

import numpy as np
import pandas as pd
import seaborn as sns

# import calplot
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

# from t3co.run import QuickStats


class T3COCharts:
    t3co_results: pd.DataFrame
    results_guide: pd.DataFrame
    value_cols: List[float]

    def __init__(
        self,
        filename: str = None,
        results_df: pd.DataFrame = None,
        results_guide: str | Path = Path(__file__).parents[1]
        / "resources"
        / "visualization"
        / "t3co_outputs_guide.csv",
    ):
        print("Initializing T3COCharts")
        if filename is not None:
            self.from_file(filename)
        else:
            self.from_df(results_df)

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
        self.cost_cols = {
            "residual_cost_dol": "#6C7B8B",
            "glider_cost_dol": "#8b7355",
            "fuel_converter_cost_dol": "#228B22",
            "fuel_storage_cost_dol": "#8B4513",
            "motor_control_power_elecs_cost_dol": "#1874CD",
            "plug_cost_dol": "#6A5ACD",
            "battery_cost_dol": "#7EC0EE",
            "purchase_tax_dol": "#CD5B45",
            "insurance_cost_dol": "#CDC673",
            "total_maintenance_cost_dol": "#DAA520",
            "total_fuel_cost_dol": "#4682B4",
            "fueling_dwell_labor_cost_dol": "#CD2626",
            "discounted_downtime_oppy_cost_dol": "#8B0000",
            "payload_capacity_cost_dol": "#CD8C95",
        }
        self.t3co_results = self.t3co_results.convert_dtypes()
        for costcol in self.cost_cols.keys():
            self.t3co_results[costcol] = self.t3co_results[costcol].astype(float)
        self.t3co_results["discounted_tco_dol"] = self.t3co_results[
            "discounted_tco_dol"
        ].astype(float)
        self.full_form_dict = dict(
            zip(
                self.results_guide["t3co_output_parameter"],
                self.results_guide["full_form"],
            )
        )
        self.cost_col_names = self.results_guide["full_form"][
            self.results_guide["t3co_output_parameter"].isin(self.cost_cols.keys())
        ]

        self.edgecolors = [
            "none",
            "black",
            "gray",
            "white",
        ]

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

        self.t3co_results["vehicle_type"] = (
            self.t3co_results["scenario_name"]
            .str.split("(")
            .apply(lambda x: " ".join(x[0].split(" ")[2:]))
        )

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

    def generate_tco_plots(
        self,
        x_group_col,
        y_group_col,
        subplot_group_col="vehicle_fuel_type",
        fig_x_size=8,
        fig_y_size=8,
        bar_width=0.8,
        legend_pos=0.25,
        edgecolor="none",
    ):
        print("running generate_tco_plots")
        disc_tco_label = self.results_guide["full_form"][
            self.results_guide["t3co_output_parameter"] == "discounted_tco_dol"
        ]
        legend_cols = list(disc_tco_label) + list(self.cost_col_names)
        x_groups = (
            self.t3co_results[x_group_col].unique() if x_group_col != "None" else [0]
        )
        y_groups = (
            self.t3co_results[y_group_col].unique() if y_group_col != "None" else [0]
        )
        fontsize = 25

        if (x_group_col == "None" and y_group_col == "None") or (
            len(x_groups) == 1 and len(y_groups) == 1
        ):
            fig, ax = plt.subplots(
                1,
                1,
                figsize=(
                    min(len(self.t3co_results) * fig_x_size + 4, 50),
                    min(4 + fig_y_size, 50),
                ),
                sharex=True,
            )
            # bottom = np.zeros(len(groups))
            # width = 0.15
            x_values = range(
                len(self.t3co_results)
            )  # X-values based on the index of the DataFrame
            y_values = self.t3co_results["discounted_tco_dol"]

            ax.scatter(
                x_values,
                y_values,
                color="red",
                label=disc_tco_label,
                zorder=3,
                marker="D",
                s=100,
            )
            self.t3co_results.plot.bar(
                y=self.cost_cols.keys(),
                stacked=True,
                figsize=(min(len(self.t3co_results) * fig_x_size, 50), 6 + fig_y_size),
                width=bar_width,
                ax=ax,
                legend=False,
                color=self.cost_cols,
                edgecolor=(edgecolor if edgecolor in self.edgecolors else "none"),
                alpha=0.8,
            )

            xlabels = [
                "\n".join(wrap(x, 25)) for x in self.t3co_results["scenario_name"]
            ]

            # bars = ax.patches
            # hatches = [p for p in patterns for i in range(len(self.t3co_results[self.cost_cols.keys()]))]
            # for bar, hatch in zip(bars, hatches):
            #     bar.set_hatch(hatch)
            # self.t3co_results.plot.line(x = ['scenario_name'], y= ['discounted_tco_dol'], ax= ax)
            ax.set_xlabel("Scenarios", fontsize=fontsize, labelpad=10)
            ax.get_yaxis().set_major_formatter(
                FuncFormatter(lambda x, p: "$" + format(int(x), ","))
            )
            ax.set_xticklabels(self.t3co_results["scenario_name"])
            ax.set_ylabel("Cost [$\$$]", fontsize=fontsize, labelpad=10)
            ax.minorticks_on()
            ax.set_xlim(-0.5, len(self.t3co_results) - 0.5)

            ax.set_xlim(-0.5, len(x_values) - 0.5)

            # plt.tight_layout()
            ax.set_xticks(range(len(self.t3co_results)), xlabels)
            ax.tick_params(labelsize=fontsize)
            handles, labels = [], []
            for h, l in zip(*ax.get_legend_handles_labels()):
                handles.append(h)
                labels.append(l)

            fig.legend(
                handles,
                legend_cols,
                loc="center right",
                bbox_to_anchor=(1 + legend_pos, 0.5),
                fontsize=fontsize,
            )

            fig.suptitle(
                "Total Cost Of Ownership Breakdown",
                fontsize=fontsize * 1.5,
                fontweight="bold",
            )
            fig = ax.get_figure()
        # %%
        elif len(x_groups) > 1 and len(y_groups) == 1:
            fig, ax = plt.subplots(
                1,
                len(x_groups),
                sharey=True,
                sharex=True,
                figsize=(min(len(x_groups) * fig_x_size + 8, 50), min(4 + fig_y_size)),
            )
            # print(self.t3co_results.loc[ self.t3co_results[x_group_col] == x_groups[0]])

            max_x = 1
            # print(f'maxn = {maxn}')
            for i in range(len(x_groups)):
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

                self.t3co_results.loc[
                    self.t3co_results[x_group_col] == x_groups[i]
                ].plot.bar(
                    x=subplot_group_col,
                    y=self.cost_cols.keys(),
                    stacked=True,
                    ax=ax[i],
                    figsize=(
                        min(len(self.t3co_results) * fig_x_size, 50),
                        min(len(y_groups) * fig_y_size + 4, 50),
                    ),
                    legend=False,
                    width=bar_width,
                    color=self.cost_cols,
                    edgecolor=edgecolor,
                    alpha=0.7,
                )
                ax[i].minorticks_on()

                # ax[i].set_ylabel("Cost [$\$$]", fontsize = fontsize)

                max_x = max(len(x_values), max_x)

                ax[i].set_xticks(
                    x_values,
                    self.t3co_results.loc[
                        self.t3co_results[x_group_col] == x_groups[i], subplot_group_col
                    ],
                )

                ax[i].set_xlabel(f"{x_groups[i]}", fontsize=fontsize, labelpad=10)
                ax[i].tick_params(axis="x", labelsize=fontsize, labelrotation=90)
                ax[i].tick_params(axis="y", labelsize=fontsize, labelrotation=0)

                ax[i].get_yaxis().set_major_formatter(
                    FuncFormatter(lambda x, p: "$" + format(int(x), ","))
                )

            for i in range(len(x_groups)):
                ax[i].set_xlim(-0.5, max_x - 0.5)

            fig.supylabel("Cost [$\$$]", fontsize=fontsize)

            fig.suptitle(
                "Total Cost Of Ownership Breakdown",
                fontsize=fontsize * 1.5,
                fontweight="bold",
            )

            handles, labels = [], []
            for h, l in zip(*ax[-1].get_legend_handles_labels()):
                handles.append(h)
                labels.append(l)

            fig.legend(
                handles,
                legend_cols,
                loc="center right",
                bbox_to_anchor=(1 + legend_pos, 0.5),
                fontsize=fontsize,
            )

            fig.supxlabel(
                self.full_form_dict[x_group_col],
                fontsize=fontsize,
            )
            plt.subplots_adjust(bottom=0.21)

        # %%
        elif len(y_groups) > 1 and len(x_groups) == 1:
            fontsize = 25
            max_x = 1
            fig, ax = plt.subplots(
                len(y_groups),
                sharex=True,
                sharey=True,
                figsize=(
                    min(10 + fig_x_size, 50),
                    min(len(y_groups) * fig_y_size + 4, 50),
                ),
            )

            for i in range(len(y_groups)):
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

                self.t3co_results.loc[
                    self.t3co_results[y_group_col] == y_groups[i]
                ].plot.bar(
                    x=subplot_group_col,
                    y=self.cost_cols.keys(),
                    stacked=True,
                    figsize=(
                        min(len(self.t3co_results) * fig_x_size, 50),
                        min(len(y_groups) * fig_y_size, 50),
                    ),
                    ax=ax[i],
                    legend=False,
                    width=bar_width,
                    color=self.cost_cols,
                    edgecolor=edgecolor,
                    alpha=0.7,
                )

                ax[i].get_yaxis().set_major_formatter(
                    FuncFormatter(lambda x, p: "$" + format(int(x), ","))
                )

                ax[i].minorticks_on()

                ax2 = ax[i].twinx()
                ax2.set_ylabel(y_groups[i], fontsize=fontsize, labelpad=10)
                ax2.set_yticks([])
                max_x = max(len(x_values), max_x)

                ax[i].tick_params(axis="x", labelsize=fontsize, labelrotation=90)
                ax[i].tick_params(axis="y", labelsize=fontsize, labelrotation=0)

            for i in range(len(y_groups)):
                ax[i].set_xlim(-0.5, max_x - 0.5)
                ax[i].set_xlabel("")

                # if i==max_x:
                #     ax[i].set_xticks(x_values, self.t3co_results.loc[
                #         self.t3co_results[y_group_col] == y_groups[i], subplot_group_col
                #     ])

            handles, labels = [], []
            for h, l in zip(*ax[-1].get_legend_handles_labels()):
                handles.append(h)
                labels.append(l)

            fig.legend(
                handles,
                legend_cols,
                loc="center right",
                bbox_to_anchor=(1 + legend_pos, 0.5),
                fontsize=fontsize,
            )

            fig.supylabel("Cost [$\$$]", fontsize=fontsize)
            fig.supxlabel(
                self.full_form_dict[subplot_group_col],
                fontsize=fontsize,
            )
            fig.suptitle(
                "Total Cost Of Ownership Breakdown",
                fontsize=fontsize * 1.5,
                fontweight="bold",
            )

        # %%
        else:
            fontsize = 25
            max_x = 1
            fig, ax = plt.subplots(
                len(y_groups),
                len(x_groups),
                sharey=True,
                sharex=True,
                figsize=(
                    min(len(y_groups) * fig_x_size + 3, 50),
                    min(len(x_groups) * fig_y_size + 7, 50),
                ),
            )

            for i in range(len(y_groups)):
                for j in range(len(x_groups)):
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

                    ax[i][j].set_xlabel(
                        f"{x_groups[j]}", fontsize=fontsize, labelpad=10
                    )
                    ax2 = ax[i][j].twinx()
                    ax2.set_ylabel(f"{y_groups[i]}", fontsize=fontsize, labelpad=10)
                    ax2.set_yticks([])

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
                        y=self.cost_cols.keys(),
                        stacked=True,
                        ax=ax[i][j],
                        legend=False,
                        width=bar_width,
                        color=self.cost_cols,
                    )

                    max_x = max(len(x_values), max_x)

            for i in range(len(y_groups)):
                for j in range(len(x_groups)):
                    ax[i][j].set_xlim(-0.5, max_x - 0.5)

            handles, labels = [], []
            for h, l in zip(*ax[-1][-1].get_legend_handles_labels()):
                handles.append(h)
                labels.append(l)

            fig.legend(
                handles,
                legend_cols,
                loc="center right",
                bbox_to_anchor=(1 + legend_pos, 0.5),
                fontsize=fontsize,
            )

            fig.supylabel("Cost [$\$$]", fontsize=fontsize)
            fig.supxlabel(
                self.full_form_dict[subplot_group_col],
                fontsize=fontsize,
            )
            fig.suptitle(
                "Total Cost Of Ownership Breakdown",
                fontsize=fontsize * 1.25,
                fontweight="bold",
            )

        return fig

    def generate_violin_plot(self, x_group_col, y_group_col="discounted_tco_dol"):
        print("Running Violin plots")
        fig, ax = plt.subplots(1, 1)
        if "dol" in y_group_col:
            ax.get_yaxis().set_major_formatter(
                FuncFormatter(lambda x, p: "$" + format(int(x), ","))
            )
        sns.violinplot(
            x=x_group_col,
            y=y_group_col,
            data=self.t3co_results,
            ax=ax,
            palette="colorblind",
            cut=0,
            density_norm="count",
            inner="quart",
            hue=x_group_col,
            legend=False,
        )
        ax.set_ylabel(self.full_form_dict[y_group_col])
        ax.set_xlabel(self.full_form_dict[x_group_col])
        return fig

    def generate_histogram(self, hist_col, n_bins, show_pct: bool = False):
        print("Running Histogram")
        fig, ax = plt.subplots()
        if len(self.t3co_results[hist_col]) > 0:
            if show_pct:
                hist, bins = np.histogram(np.array(self.t3co_results[hist_col]), bins = n_bins)
                ax.bar(
                    bins[:-1],
                    hist.astype(np.float32) / hist.sum()*100,
                    width=(bins[1] - bins[0]),
                )
                ax.set_ylabel("Percentage of Scenarios [%]")
            else:
                ax.hist(x=self.t3co_results[hist_col], bins=n_bins)
                ax.set_ylabel("Number of Scenarios")
            ax.set_xlabel(self.full_form_dict[hist_col])
        return fig
