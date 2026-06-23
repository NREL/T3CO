# Visualization

The [`T3COCharts`](./api/charts.md) class (`t3co.visualize.charts`) turns a T3CO results CSV (or DataFrame) into three plots, each rendered with a selectable backend:

- `backend="matplotlib"` (default) — static figures for PNG/PDF export.
- `backend="plotly"` — interactive, self-contained HTML.

## Install

The plotting libraries are an optional extra:

```bash
pip install t3co[viz]
```

`matplotlib` is already a core T3CO dependency, so the TCO breakdown and histogram render without the extra. The violin plot additionally needs `seaborn`, and the interactive HTML backend needs `plotly`.

## Usage

```python
from t3co.visualize.charts import T3COCharts

tc = T3COCharts(filename="results.csv", backend="plotly")
fig = tc.generate_tco_plots(x_group_col="vehicle_fuel_type", subplot_group_col="vehicle_type")
fig.write_html("tco_breakdown.html")   # or fig.savefig(...) with the matplotlib backend

# Combine several Plotly figures into one self-contained HTML report:
T3COCharts.write_html_report(
    [
        tc.generate_tco_plots(x_group_col="vehicle_fuel_type"),
        tc.generate_histogram(hist_col="discounted_tco_dol", n_bins=10),
        tc.generate_violin_plot(x_group_col="vehicle_fuel_type", y_group_col="mpgge"),
    ],
    "charts.html",
)
```

`T3COCharts` reads the prefixed result columns directly and derives the grouping columns (`vehicle_fuel_type`, `vehicle_type`, `vehicle_weight_class`, `veh_pt_type`) automatically. Each `generate_*` method returns a figure object that you save or display yourself.

### TCO Breakdown

Stacked cost components per scenario, with a marker for the discounted TCO. Pass `x_group_col` and/or `y_group_col` to split the results into a subplot grid (e.g. by fuel type and weight class).

<img src="../images/tco_breakdown_sample.png" alt="TCO breakdown" width="650"/>

### Histogram

Distribution of any numeric output across selections. `show_pct=True` plots the percentage of scenarios instead of a count.

<img src="../images/histogram_sample.png" alt="Histogram" width="400"/>

### Violin

Distribution of a metric across categories (e.g. `mpgge` by fuel type).

<img src="../images/violinplot_sample.png" alt="Violin plot" width="400"/>

## Interactive explorer

`generate_interactive_plot()` returns a Plotly scatter with **dropdown menus to choose the x- and y-axis columns** directly on the page — pick any grouping column or numeric output for either axis and the chart updates client-side, no server needed. It always renders with Plotly (interactive only) and leads the combined HTML report.

```python
tc = T3COCharts(filename="results.csv", backend="plotly")
tc.generate_interactive_plot(default_x="vehicle_fuel_type", default_y="discounted_tco_dol")
```

## Charts from the CLI

Add `--plot` to a sweep run to generate the default charts next to the results CSV. The Plotly backend combines the interactive explorer plus the three standard charts into a **single self-contained HTML report** (`<results>_charts.html`); matplotlib writes one PNG per chart:

```bash
python -m t3co.cli.sweep --analysis-id=0 --plot             # one combined HTML (Plotly, default)
python -m t3co.cli.sweep --analysis-id=0 --plot matplotlib  # separate PNGs
```

The [`visualization_demo.py`](https://github.com/NatLabRockies/T3CO/tree/main/src/t3co/demos/visualization_demo.py) script shows the full programmatic workflow in both backends.
