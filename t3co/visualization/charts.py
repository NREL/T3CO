from pathlib import Path
from textwrap import wrap
from typing import List

import matplotlib
import matplotlib.figure
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter, FormatStrFormatter


class T3COCharts:
    """
    This class takes T3CO output CSV file as input and generates different plots to gain insights from T3CO Results

    """

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
    ) -> None:
        """
        This constructor initializes the T3COCharts object either from a dataframe or a CSV file path.

        Args:
            filename (str, optional): Filepath to T3CO Results CSV File. Defaults to None.
            results_df (pd.DataFrame, optional): Input pandas dataframe containing T3CO Results. Defaults to None.
            results_guide (str | Path, optional): File path to t3co_outputs_guide.csv file that contains useful parameter descriptions and axis labels. Defaults to Path(__file__).parents[1]/"resources"/"visualization"/"t3co_outputs_guide.csv".
        """
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
            self.t3co_results[costcol] = self.t3co_results[costcol].astype(float).round(2)
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
    ) -> None:
        """
        This method reads a T3CO Results CSV file into a dataframe

        Args:
            filename (str | Path, optional): Path to T3CO Results CSV File. Defaults to None.
        """
        self.t3co_results = pd.read_csv(filename)

    def from_df(self, results_df: pd.DataFrame) -> None:
        """
        This method reads t3co_results from a dataframe

        Args:
            results_df (pd.DataFrame): Input T3CO Results dataframe
        """
        self.t3co_results = results_df

    def to_df(self) -> pd.DataFrame:
        """
        This returns the self.t3co_results member

        Returns:
            pd.DataFrame: T3CO Results dataframe
        """
        return self.t3co_results

    def parse_scenario_name(self) -> None:
        """
        This method parses 'scenario_name' into 'vehicle_type', 'tech_progress', and 'vehicle_fuel_type' and uses 'scenario_gvwr_kg' to create 'vehicle_weight_class'
        """
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
        x_group_col: str,
        y_group_col: str,
        subplot_group_col: str = "vehicle_fuel_type",
        fig_x_size: int = 8,
        fig_y_size: int = 8,
        bar_width: float = 0.8,
        legend_pos: float = 0.25,
        edgecolor: str = "none",
    ) -> matplotlib.figure.Figure:
        """
        This method generates a TCO Breakdown plot based on input arguments.
        If x_group_col and/or y_group_col are provided, then a matrix/grid of subplots are generated within the same figure based on row- and column-wise groupings

        Args:
            x_group_col (str): T3CO Results parameter name to group on x-axis, i.e., grouping criteria for columns in subplots grid
            y_group_col (str): T3CO Results parameter name to group on y-axis, i.e., grouping criteria for rows in subplots grid
            subplot_group_col (str, optional): T3CO Results parameter to display within each subplots cell. Defaults to "vehicle_fuel_type".
            fig_x_size (int, optional): Figure width relative to each bar on x-axis within subplot. Defaults to 8.
            fig_y_size (int, optional): Figure height relative to each subplot cell. Defaults to 8.
            bar_width (float, optional): Relative width of bars based on available width. Takes values between 0.0 and 1.0. Defaults to 0.8.
            legend_pos (float, optional): Relative position of legend on the right side of plots. Takes values between 0.0 and 1.0. Defaults to 0.25.
            edgecolor (str, optional): Edge color to distinguish cost elements in the stacked bars. Defaults to "none".

        Returns:
            matplotlib.figure.Figure: TCO Breakdown Figure object
        """
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
            ax.set_ylabel(r"Cost [$]", fontsize=fontsize, labelpad=10)
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

        elif len(x_groups) > 1 and len(y_groups) == 1:
            fig, ax = plt.subplots(
                1,
                len(x_groups),
                sharey=True,
                sharex=True,
                figsize=(min(len(x_groups) * fig_x_size + 8, 50), min(4 + fig_y_size,50)),
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

            fig.supylabel(r"Cost [$]", fontsize=fontsize)

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

            fig.supylabel(r"Cost [$]", fontsize=fontsize)
            fig.supxlabel(
                self.full_form_dict[subplot_group_col],
                fontsize=fontsize,
            )
            fig.suptitle(
                "Total Cost Of Ownership Breakdown",
                fontsize=fontsize * 1.5,
                fontweight="bold",
            )

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

            fig.supylabel(r"Cost [$]", fontsize=fontsize)
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

    def generate_violin_plot(
        self, x_group_col: str, y_group_col: str = "discounted_tco_dol", fig_width:float =8, fig_height:float = 5,
    ) -> matplotlib.figure.Figure:
        """
        This method generates a violin plot based on x-axis group column and y-axis column name.

        Args:
            x_group_col (str): T3CO Results parameter to group by on x-axis inside violinplot
            y_group_col (str, optional): T3CO Results parameter to plot on y-axis. Defaults to "discounted_tco_dol".

        Returns:
            matplotlib.figure.Figure: Violin Plot Figure object
        """
        print("Running Violin plots")
        fontsize = 10
        fig, ax = plt.subplots(1,1,figsize = (fig_width,fig_height))
        self.t3co_results[y_group_col] = self.t3co_results[y_group_col].astype(float).round(5)
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
        if "dol" in y_group_col:
            ax.get_yaxis().set_major_formatter(
                FuncFormatter(lambda x, p: "$" + format(int(x), ","))
            )
        
        ax.set_title("Violin Plot",fontsize=fontsize * 1.5,
                fontweight="bold",)
        ax.set_ylabel(self.full_form_dict[y_group_col])
        ax.set_xlabel(self.full_form_dict[x_group_col])
        return fig

    def generate_histogram(
        self, hist_col: str, n_bins: int, fig_width:float =8, fig_height:float = 5, show_pct: bool = False
    ) -> matplotlib.figure.Figure:
        """
        This method generates a histogram plot based on inputs hist_col and n_bins

        Args:
            hist_col (str): T3CO column name to plot histogram
            n_bins (int): Number of bins in histogram
            fig_width (float): Figure total width
            fig_height (float):  Figure total height
            show_pct (bool, optional): If True, plots percentage on y-axis instead of number of items. Defaults to False.

        Returns:
            matplotlib.figure.Figure: Histogram figure object
        """
        print("Running Histogram")
        fig, ax = plt.subplots(1,1,figsize = (fig_width,fig_height))
        fontsize = 10
        self.t3co_results[hist_col] = self.t3co_results[hist_col].astype(float).round(4)
        if len(self.t3co_results[hist_col]) > 0:
            if show_pct:
                hist, bins = np.histogram(
                    np.array(self.t3co_results[hist_col]), bins=n_bins
                )
                ax.bar(
                    bins[:-1],
                    hist.astype(np.float32) / hist.sum() * 100,
                    width=(bins[1] - bins[0]),
                )
                ax.set_ylabel("Percentage of Scenarios [%]")
            else:
                ax.hist(x=self.t3co_results[hist_col], bins=n_bins)
                ax.set_ylabel("Number of Scenarios")
            ax.set_title("Histogram Plot", fontsize=fontsize * 1.25,
                fontweight="bold",)
            ax.set_xlabel(self.full_form_dict[hist_col])
        return fig
