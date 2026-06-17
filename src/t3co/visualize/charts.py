"""
T3CO visualization module.

This module ports the charting functionality from T3CO 1.0.x into the 2.0 results
schema. It exposes a single :class:`T3COCharts` class that reads a T3CO results CSV
(or DataFrame) and generates three plots - a TCO cost-breakdown chart, a violin
plot, and a histogram.

Each plot can be rendered with one of two interchangeable backends:

* ``"matplotlib"`` (alias ``"seaborn"``) - static figures suitable for PNG/PDF export.
* ``"plotly"`` - interactive figures suitable for self-contained HTML export.

The plotting dependencies are optional. Install them alongside T3CO with::

    pip install t3co_go[viz]
"""

from pathlib import Path
from textwrap import wrap
from typing import List, Union

import numpy as np
import pandas as pd

# Pip extra that provides the optional plotting backends.
_VIZ_EXTRA_HINT = (
    "This requires the optional plotting dependencies. "
    "Install them with: pip install t3co_go[viz]"
)

DEFAULT_RESULTS_GUIDE = (
    Path(__file__).parents[1] / "resources" / "visualization" / "t3co_outputs_guide.csv"
)


class T3COCharts:
    """
    Generates plots from T3CO results to gain insights from the Total Cost of
    Ownership outputs.

    The class accepts a T3CO results CSV file or DataFrame (as produced by
    ``Ledger.to_csv``/``Ledger.to_df`` or the ``t3co.cli.sweep`` runner) and
    normalizes the 2.0 flattened column names into the canonical names used by
    the plots and the ``t3co_outputs_guide.csv`` labels guide.
    """

    t3co_results: pd.DataFrame
    results_guide: pd.DataFrame
    value_cols: List[str]
    backend: str

    # Cost components shown (stacked) in the TCO breakdown plot, with their colors.
    # These are bare Ledger fields and survive the 2.0 flattening unchanged.
    COST_COLS = {
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

    # Weight-class boundaries (kg, upper-inclusive) used to derive vehicle_weight_class.
    _WEIGHT_CLASS_BINS = [0, 2722, 3856, 4536, 6350, 7257, 8845, 11793, 14969, 50000]
    _WEIGHT_CLASS_LABELS = [
        "Class 1",
        "Class 2a",
        "Class 2b",
        "Class 3",
        "Class 4",
        "Class 5",
        "Class 6",
        "Class 7",
        "Class 8",
    ]

    # Maps a canonical grouping column to the 2.0 flattened source columns it may
    # come from (first match wins). Lets the same code consume both a freshly
    # flattened sweep CSV (prefixed names) and a pre-normalized one (bare names).
    _GROUP_COL_SOURCES = {
        "vehicle_fuel_type": ["vehicle_fuel_type", "scenario_fuel_type", "fuel_type"],
        "veh_year": ["veh_year", "scenario_veh_year"],
        "vehicle_type": ["vehicle_type", "scenario_vocation", "vocation"],
        "veh_pt_type": ["veh_pt_type", "vehicle_veh_pt_type"],
    }

    def __init__(
        self,
        filename: Union[str, Path] = None,
        results_df: pd.DataFrame = None,
        backend: str = "matplotlib",
        results_guide: Union[str, Path] = DEFAULT_RESULTS_GUIDE,
    ) -> None:
        """
        Initializes the T3COCharts object from a DataFrame or a CSV file path.

        Args:
            filename (str | Path, optional): Filepath to a T3CO results CSV file. Defaults to None.
            results_df (pd.DataFrame, optional): T3CO results DataFrame. Defaults to None.
            backend (str, optional): Rendering backend. One of "matplotlib" (alias "seaborn")
                for static figures or "plotly" for interactive HTML figures. Defaults to "matplotlib".
            results_guide (str | Path, optional): Path to t3co_outputs_guide.csv containing parameter
                descriptions and axis labels. Defaults to the bundled resource file.

        Raises:
            ValueError: If neither filename nor results_df is provided, or backend is unknown.
        """
        self.backend = self._normalize_backend(backend)

        if filename is not None:
            self.from_file(filename)
        elif results_df is not None:
            self.from_df(results_df)
        else:
            raise ValueError("Provide either 'filename' or 'results_df'.")

        self.results_guide = pd.read_csv(results_guide)
        self.full_form_dict = dict(
            zip(
                self.results_guide["t3co_output_parameter"],
                self.results_guide["full_form"],
            )
        )
        self.value_cols = list(
            self.results_guide.loc[
                self.results_guide["data_type"] == "float", "t3co_output_parameter"
            ].values
        )

        self._normalize_columns()

        # Cast plotted numeric columns to float (results CSVs may load as object/str).
        for col in list(self.present_cost_cols().keys()) + ["discounted_tco_dol"]:
            if col in self.t3co_results.columns:
                self.t3co_results[col] = (
                    pd.to_numeric(self.t3co_results[col], errors="coerce").astype(float).round(2)
                )

        # Group-by options exposed for the TCO plot, limited to columns actually present.
        candidate_groups = [
            "vehicle_weight_class",
            "veh_year",
            "vehicle_type",
            "tech_progress",
            "vehicle_fuel_type",
            "veh_pt_type",
        ]
        self.group_columns = ["None"] + [
            c for c in candidate_groups if c in self.t3co_results.columns
        ]
        self.edgecolors = ["none", "black", "gray", "white"]

    # ------------------------------------------------------------------ #
    # Data loading / access
    # ------------------------------------------------------------------ #
    def from_file(self, filename: Union[str, Path]) -> None:
        """Reads a T3CO results CSV file into ``self.t3co_results``."""
        self.t3co_results = pd.read_csv(filename)

    def from_df(self, results_df: pd.DataFrame) -> None:
        """Loads ``self.t3co_results`` from an existing DataFrame (a copy is taken)."""
        self.t3co_results = results_df.copy().reset_index(drop=True)

    def to_df(self) -> pd.DataFrame:
        """Returns the (normalized) results DataFrame."""
        return self.t3co_results

    def present_cost_cols(self) -> dict:
        """Returns the subset of cost columns (with colors) present in the results."""
        return {
            k: v for k, v in self.COST_COLS.items() if k in self.t3co_results.columns
        }

    # ------------------------------------------------------------------ #
    # Schema normalization
    # ------------------------------------------------------------------ #
    def _normalize_columns(self) -> None:
        """
        Creates canonical grouping columns expected by the plots from the 2.0
        flattened results schema.

        The 2.0 results come from ``Ledger.to_dict(include_prefix=True)`` which
        prefixes nested objects (e.g. ``scenario_fuel_type``). This maps those to
        the bare names the plots and the labels guide use, and derives
        ``vehicle_weight_class`` from GVWR. All steps are guarded so a CSV that
        already uses bare names is left untouched.
        """
        df = self.t3co_results

        # Map prefixed/source columns onto canonical names when not already present.
        for canonical, sources in self._GROUP_COL_SOURCES.items():
            if canonical in df.columns:
                continue
            for src in sources:
                if src in df.columns:
                    df[canonical] = df[src]
                    break

        # Derive vehicle_weight_class from GVWR if not already provided.
        if "vehicle_weight_class" not in df.columns:
            gvwr_col = next(
                (c for c in ["scenario_gvwr_kg", "gvwr_kg"] if c in df.columns), None
            )
            if gvwr_col is not None:
                df["vehicle_weight_class"] = pd.cut(
                    pd.to_numeric(df[gvwr_col], errors="coerce"),
                    bins=self._WEIGHT_CLASS_BINS,
                    labels=self._WEIGHT_CLASS_LABELS,
                    right=True,
                ).astype("object")

        # tech_progress is not a 2.0 field; best-effort parse from scenario_name
        # of the legacy "Vocation Type (FuelType, TechProgress)" format.
        if "tech_progress" not in df.columns and "scenario_name" in df.columns:
            try:
                parsed = (
                    df["scenario_name"]
                    .str.split("(")
                    .apply(lambda x: x[1].split(",")[-1].split(")")[0].strip())
                )
                if parsed.notna().all() and (parsed.str.len() > 0).all():
                    df["tech_progress"] = parsed
            except (IndexError, AttributeError):
                pass  # scenario_name not in the legacy format; skip tech_progress.

        self.t3co_results = df

    # ------------------------------------------------------------------ #
    # Backend helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _normalize_backend(backend: str) -> str:
        """Validates and canonicalizes the backend name."""
        backend = (backend or "").lower()
        if backend in ("matplotlib", "seaborn", "mpl"):
            return "matplotlib"
        if backend in ("plotly", "html"):
            return "plotly"
        raise ValueError(
            f"Unknown backend {backend!r}. Use 'matplotlib' (static) or 'plotly' (interactive)."
        )

    def _require_matplotlib(self):
        """Lazily imports matplotlib with a helpful error.

        matplotlib is a transitive dependency of pymoo (a core T3CO requirement),
        so the cost-breakdown and histogram plots work on a base install. Only the
        violin plot additionally needs seaborn (see ``_require_seaborn``).
        """
        try:
            import matplotlib
            import matplotlib.pyplot as plt
            from matplotlib.ticker import FuncFormatter

            return matplotlib, plt, FuncFormatter
        except ImportError as e:  # pragma: no cover - exercised via error path
            raise ImportError(
                f"Static (matplotlib) plotting is unavailable. {_VIZ_EXTRA_HINT}"
            ) from e

    def _require_seaborn(self):
        """Lazily imports seaborn (used only for violin plots) with a helpful error."""
        try:
            import seaborn as sns

            return sns
        except ImportError as e:  # pragma: no cover - exercised via error path
            raise ImportError(
                f"Violin plots require seaborn. {_VIZ_EXTRA_HINT}"
            ) from e

    def _require_plotly(self):
        """Lazily imports the plotly stack with a helpful error."""
        try:
            import plotly.express as px
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots

            return go, px, make_subplots
        except ImportError as e:  # pragma: no cover - exercised via error path
            raise ImportError(
                f"Interactive (plotly) plotting is unavailable. {_VIZ_EXTRA_HINT}"
            ) from e

    def _label(self, col: str) -> str:
        """Returns the human-readable label for a column, falling back to its name."""
        return self.full_form_dict.get(col, col)

    def _group_values(self, group_col: str) -> list:
        """Returns the distinct values to iterate over for a grouping column."""
        if group_col == "None":
            return [None]
        return list(self.t3co_results[group_col].unique())

    # ------------------------------------------------------------------ #
    # Public plotting API (backend-dispatching)
    # ------------------------------------------------------------------ #
    def generate_tco_plots(
        self,
        x_group_col: str = "None",
        y_group_col: str = "None",
        subplot_group_col: str = "vehicle_fuel_type",
        fig_x_size: int = 8,
        fig_y_size: int = 8,
        bar_width: float = 0.8,
        legend_pos: float = 0.25,
        edgecolor: str = "none",
    ):
        """
        Generates a TCO cost-breakdown plot, optionally as a grid of subplots
        grouped by ``x_group_col`` (columns) and ``y_group_col`` (rows).

        Within each cell, stacked bars show every cost component (colored per
        ``COST_COLS``) and red diamond markers overlay the discounted TCO.

        Args:
            x_group_col (str, optional): Column to group subplot columns. Use "None" for no grouping.
            y_group_col (str, optional): Column to group subplot rows. Use "None" for no grouping.
            subplot_group_col (str, optional): Column shown as bars within each cell when grouped.
                Defaults to "vehicle_fuel_type".
            fig_x_size (int, optional): Figure width factor per subplot column. Defaults to 8.
            fig_y_size (int, optional): Figure height factor per subplot row. Defaults to 8.
            bar_width (float, optional): Bar width fraction (0-1). Defaults to 0.8.
            legend_pos (float, optional): Legend horizontal offset (matplotlib only). Defaults to 0.25.
            edgecolor (str, optional): Bar edge color (matplotlib only). Defaults to "none".

        Returns:
            matplotlib.figure.Figure | plotly.graph_objects.Figure: The TCO breakdown figure.
        """
        if "discounted_tco_dol" not in self.t3co_results.columns:
            raise KeyError("Results are missing required column 'discounted_tco_dol'.")
        if self.backend == "plotly":
            return self._generate_tco_plots_plotly(
                x_group_col, y_group_col, subplot_group_col, fig_x_size, fig_y_size, bar_width
            )
        return self._generate_tco_plots_mpl(
            x_group_col,
            y_group_col,
            subplot_group_col,
            fig_x_size,
            fig_y_size,
            bar_width,
            legend_pos,
            edgecolor,
        )

    def generate_violin_plot(
        self,
        x_group_col: str,
        y_group_col: str = "discounted_tco_dol",
        fig_width: float = 8,
        fig_height: float = 5,
    ):
        """
        Generates a violin plot of ``y_group_col`` distribution across ``x_group_col`` categories.

        Args:
            x_group_col (str): Categorical column to group on the x-axis.
            y_group_col (str, optional): Numeric column on the y-axis. Defaults to "discounted_tco_dol".
            fig_width (float, optional): Figure width (inches for matplotlib). Defaults to 8.
            fig_height (float, optional): Figure height (inches for matplotlib). Defaults to 5.

        Returns:
            matplotlib.figure.Figure | plotly.graph_objects.Figure: The violin figure.
        """
        if self.backend == "plotly":
            return self._generate_violin_plotly(x_group_col, y_group_col, fig_width, fig_height)
        return self._generate_violin_mpl(x_group_col, y_group_col, fig_width, fig_height)

    def generate_histogram(
        self,
        hist_col: str,
        n_bins: int,
        fig_width: float = 8,
        fig_height: float = 5,
        show_pct: bool = False,
    ):
        """
        Generates a histogram of ``hist_col``.

        Args:
            hist_col (str): Column to plot.
            n_bins (int): Number of bins.
            fig_width (float, optional): Figure width (inches for matplotlib). Defaults to 8.
            fig_height (float, optional): Figure height (inches for matplotlib). Defaults to 5.
            show_pct (bool, optional): If True, the y-axis shows percentage of scenarios
                instead of a count. Defaults to False.

        Returns:
            matplotlib.figure.Figure | plotly.graph_objects.Figure: The histogram figure.
        """
        if self.backend == "plotly":
            return self._generate_histogram_plotly(hist_col, n_bins, fig_width, fig_height, show_pct)
        return self._generate_histogram_mpl(hist_col, n_bins, fig_width, fig_height, show_pct)

    # ------------------------------------------------------------------ #
    # matplotlib / seaborn implementations
    # ------------------------------------------------------------------ #
    def _generate_tco_plots_mpl(
        self,
        x_group_col,
        y_group_col,
        subplot_group_col,
        fig_x_size,
        fig_y_size,
        bar_width,
        legend_pos,
        edgecolor,
    ):
        _, plt, FuncFormatter = self._require_matplotlib()

        df = self.t3co_results
        cost_cols = self.present_cost_cols()
        ycols = list(cost_cols.keys())
        colors = list(cost_cols.values())
        disc_label = self._label("discounted_tco_dol")
        currency = FuncFormatter(lambda v, p: "$" + format(int(v), ","))
        fontsize = 14
        grouped = x_group_col != "None" or y_group_col != "None"

        x_groups = self._group_values(x_group_col)
        y_groups = self._group_values(y_group_col)
        nrows, ncols = len(y_groups), len(x_groups)

        fig, axes = plt.subplots(
            nrows,
            ncols,
            sharey=True,
            squeeze=False,
            figsize=(
                min(4 + ncols * fig_x_size, 50),
                min(4 + nrows * fig_y_size, 50),
            ),
        )

        for i, yv in enumerate(y_groups):
            for j, xv in enumerate(x_groups):
                ax = axes[i][j]
                sub = df
                if x_group_col != "None":
                    sub = sub[sub[x_group_col] == xv]
                if y_group_col != "None":
                    sub = sub[sub[y_group_col] == yv]
                if sub.empty:
                    ax.set_axis_off()
                    continue

                xpos = range(len(sub))
                ax.scatter(
                    list(xpos),
                    sub["discounted_tco_dol"],
                    color="red",
                    marker="D",
                    s=80,
                    zorder=3,
                    label=disc_label,
                )
                sub.plot.bar(
                    y=ycols,
                    stacked=True,
                    ax=ax,
                    width=bar_width,
                    color=colors,
                    legend=False,
                    edgecolor=edgecolor if edgecolor in self.edgecolors else "none",
                    alpha=0.85,
                )
                ax.get_yaxis().set_major_formatter(currency)
                ax.minorticks_on()

                if grouped and subplot_group_col in sub.columns:
                    ticklabels = [str(v) for v in sub[subplot_group_col]]
                else:
                    ticklabels = ["\n".join(wrap(str(s), 25)) for s in sub["scenario_name"]]
                ax.set_xticks(list(range(len(sub))))
                ax.set_xticklabels(ticklabels, rotation=90, fontsize=fontsize * 0.7)
                ax.set_xlim(-0.5, len(sub) - 0.5)

                if x_group_col != "None" and i == nrows - 1:
                    ax.set_xlabel(str(xv), fontsize=fontsize, labelpad=8)
                if y_group_col != "None" and j == ncols - 1:
                    ax2 = ax.twinx()
                    ax2.set_yticks([])
                    ax2.set_ylabel(str(yv), fontsize=fontsize, labelpad=8)

        legend_labels = [disc_label] + [self._label(c) for c in ycols]
        handles, _ = axes[0][0].get_legend_handles_labels()
        fig.legend(
            handles,
            legend_labels,
            loc="center right",
            bbox_to_anchor=(1 + legend_pos, 0.5),
            fontsize=fontsize,
        )
        fig.supylabel(r"Cost [$]", fontsize=fontsize)
        if x_group_col != "None":
            fig.supxlabel(self._label(x_group_col), fontsize=fontsize)
        fig.suptitle(
            "Total Cost of Ownership Breakdown",
            fontsize=fontsize * 1.4,
            fontweight="bold",
        )
        fig.tight_layout()
        return fig

    def _generate_violin_mpl(self, x_group_col, y_group_col, fig_width, fig_height):
        _, plt, FuncFormatter = self._require_matplotlib()
        sns = self._require_seaborn()

        df = self.t3co_results.copy()
        df[y_group_col] = pd.to_numeric(df[y_group_col], errors="coerce").round(5)
        fig, ax = plt.subplots(1, 1, figsize=(fig_width, fig_height))
        sns.violinplot(
            x=x_group_col,
            y=y_group_col,
            data=df,
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
                FuncFormatter(lambda v, p: "$" + format(int(v), ","))
            )
        ax.set_title("Violin Plot", fontsize=15, fontweight="bold")
        ax.set_xlabel(self._label(x_group_col))
        ax.set_ylabel(self._label(y_group_col))
        fig.tight_layout()
        return fig

    def _generate_histogram_mpl(self, hist_col, n_bins, fig_width, fig_height, show_pct):
        _, plt, _ = self._require_matplotlib()

        df = self.t3co_results
        values = pd.to_numeric(df[hist_col], errors="coerce").dropna().round(4)
        fig, ax = plt.subplots(1, 1, figsize=(fig_width, fig_height))
        if len(values) > 0:
            if show_pct:
                hist, bins = np.histogram(np.array(values), bins=n_bins)
                ax.bar(
                    bins[:-1],
                    hist.astype(np.float32) / hist.sum() * 100,
                    width=(bins[1] - bins[0]),
                    align="edge",
                )
                ax.set_ylabel("Percentage of Scenarios [%]")
            else:
                ax.hist(x=values, bins=n_bins)
                ax.set_ylabel("Number of Scenarios")
            ax.set_title("Histogram Plot", fontsize=14, fontweight="bold")
            ax.set_xlabel(self._label(hist_col))
        fig.tight_layout()
        return fig

    # ------------------------------------------------------------------ #
    # plotly implementations
    # ------------------------------------------------------------------ #
    def _generate_tco_plots_plotly(
        self, x_group_col, y_group_col, subplot_group_col, fig_x_size, fig_y_size, bar_width
    ):
        go, _, make_subplots = self._require_plotly()

        df = self.t3co_results
        cost_cols = self.present_cost_cols()
        grouped = x_group_col != "None" or y_group_col != "None"

        x_groups = self._group_values(x_group_col)
        y_groups = self._group_values(y_group_col)
        nrows, ncols = len(y_groups), len(x_groups)

        fig = make_subplots(
            rows=nrows,
            cols=ncols,
            shared_yaxes=True,
            column_titles=[str(x) for x in x_groups] if x_group_col != "None" else None,
            row_titles=[str(y) for y in y_groups] if y_group_col != "None" else None,
            horizontal_spacing=0.04,
            vertical_spacing=0.08,
        )

        shown = set()
        for i, yv in enumerate(y_groups):
            for j, xv in enumerate(x_groups):
                sub = df
                if x_group_col != "None":
                    sub = sub[sub[x_group_col] == xv]
                if y_group_col != "None":
                    sub = sub[sub[y_group_col] == yv]
                if sub.empty:
                    continue

                if grouped and subplot_group_col in sub.columns:
                    xvals = [str(v) for v in sub[subplot_group_col]]
                else:
                    xvals = [str(v) for v in sub["scenario_name"]]

                for col, color in cost_cols.items():
                    fig.add_trace(
                        go.Bar(
                            x=xvals,
                            y=sub[col],
                            name=self._label(col),
                            marker_color=color,
                            legendgroup=col,
                            showlegend=col not in shown,
                        ),
                        row=i + 1,
                        col=j + 1,
                    )
                    shown.add(col)

                fig.add_trace(
                    go.Scatter(
                        x=xvals,
                        y=sub["discounted_tco_dol"],
                        mode="markers",
                        name=self._label("discounted_tco_dol"),
                        marker=dict(color="red", symbol="diamond", size=9),
                        legendgroup="_disc_tco",
                        showlegend="_disc_tco" not in shown,
                    ),
                    row=i + 1,
                    col=j + 1,
                )
                shown.add("_disc_tco")

        fig.update_layout(
            barmode="stack",
            bargap=max(0.0, 1.0 - bar_width),
            title=dict(text="Total Cost of Ownership Breakdown", x=0.5, font=dict(size=20)),
            legend_title_text="Cost Components",
            width=min(400 + ncols * fig_x_size * 60, 2400),
            height=min(300 + nrows * fig_y_size * 55, 2000),
        )
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")
        fig.update_yaxes(title_text="Cost [$]", row=(nrows + 1) // 2, col=1)
        if x_group_col != "None":
            fig.update_xaxes(title_text=self._label(x_group_col), row=nrows, col=(ncols + 1) // 2)
        return fig

    def _generate_violin_plotly(self, x_group_col, y_group_col, fig_width, fig_height):
        _, px, _ = self._require_plotly()

        df = self.t3co_results.copy()
        df[y_group_col] = pd.to_numeric(df[y_group_col], errors="coerce")
        fig = px.violin(
            df,
            x=x_group_col,
            y=y_group_col,
            color=x_group_col,
            box=True,
            points="all",
        )
        if "dol" in y_group_col:
            fig.update_yaxes(tickprefix="$", tickformat=",.0f")
        fig.update_layout(
            title=dict(text="Violin Plot", x=0.5, font=dict(size=18)),
            xaxis_title=self._label(x_group_col),
            yaxis_title=self._label(y_group_col),
            width=int(fig_width * 96),
            height=int(fig_height * 96),
            showlegend=False,
        )
        return fig

    def _generate_histogram_plotly(self, hist_col, n_bins, fig_width, fig_height, show_pct):
        go, _, _ = self._require_plotly()

        df = self.t3co_results.copy()
        values = pd.to_numeric(df[hist_col], errors="coerce")
        fig = go.Figure(
            go.Histogram(
                x=values,
                nbinsx=n_bins,
                histnorm="percent" if show_pct else None,
            )
        )
        fig.update_layout(
            title=dict(text="Histogram Plot", x=0.5, font=dict(size=18)),
            xaxis_title=self._label(hist_col),
            yaxis_title="Percentage of Scenarios [%]" if show_pct else "Number of Scenarios",
            width=int(fig_width * 96),
            height=int(fig_height * 96),
            bargap=0.05,
        )
        return fig
