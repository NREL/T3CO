"""Tests for the T3CO visualization module (t3co.visualize.charts.T3COCharts)."""

import pandas as pd
import pytest

from t3co.visualize.charts import T3COCharts

# Bare Ledger cost fields that survive 2.0 flattening unchanged.
COST_COLS = list(T3COCharts.COST_COLS.keys())


def _make_results() -> pd.DataFrame:
    """Builds a small results frame using 2.0 *flattened* (prefixed) column names."""
    n = 6
    rows = []
    fuels = ["diesel", "BEV", "HEV"]
    for i in range(n):
        row = {
            "selection": i + 1,
            # legacy-format scenario_name also exercises the tech_progress parse
            "scenario_name": f"Class 8 Truck {i} ({fuels[i % 3]}, 2020, no program)",
            # nested-object columns as emitted by Ledger.to_dict(include_prefix=True)
            "scenario_fuel_type": fuels[i % 3],
            "scenario_vocation": "Long haul" if i % 2 else "Regional",
            "scenario_gvwr_kg": 36287.0 if i % 2 else 8000.0,
            "scenario_veh_year": 2020,
            "vehicle_veh_pt_type": fuels[i % 3],
            "discounted_tco_dol": 100000.0 + i * 5000,
            "mpgge": 4.0 + i * 0.1,
        }
        for k, col in enumerate(COST_COLS):
            row[col] = 1000.0 * (k + 1) + i * 100
        rows.append(row)
    return pd.DataFrame(rows)


@pytest.fixture
def results_df():
    return _make_results()


def test_normalizes_prefixed_columns(results_df):
    tc = T3COCharts(results_df=results_df, backend="plotly")
    df = tc.to_df()
    # prefixed source columns are mapped onto canonical grouping names
    assert "vehicle_fuel_type" in df.columns
    assert "vehicle_type" in df.columns
    assert "veh_pt_type" in df.columns
    assert "vehicle_weight_class" in df.columns
    assert list(df["vehicle_fuel_type"]) == list(results_df["scenario_fuel_type"])
    # weight class derived from GVWR (36287 -> Class 8, 8000 -> Class 5)
    assert set(df["vehicle_weight_class"]) == {"Class 8", "Class 5"}
    # tech_progress parsed from the legacy scenario_name format
    assert "tech_progress" in df.columns
    assert set(df["tech_progress"]) == {"no program"}
    # only present, valid group columns are exposed
    assert tc.group_columns[0] == "None"
    assert "vehicle_fuel_type" in tc.group_columns


def test_bad_backend_raises(results_df):
    with pytest.raises(ValueError):
        T3COCharts(results_df=results_df, backend="ggplot")


def test_requires_a_data_source():
    with pytest.raises(ValueError):
        T3COCharts()


def test_missing_tco_column_raises():
    df = _make_results().drop(columns=["discounted_tco_dol"])
    tc = T3COCharts(results_df=df, backend="plotly")
    with pytest.raises(KeyError):
        tc.generate_tco_plots()


# --------------------------- plotly backend --------------------------- #
def test_plotly_figures(results_df):
    go = pytest.importorskip("plotly.graph_objects")
    tc = T3COCharts(results_df=results_df, backend="plotly")

    tco = tc.generate_tco_plots(x_group_col="vehicle_fuel_type", subplot_group_col="vehicle_type")
    violin = tc.generate_violin_plot(x_group_col="vehicle_fuel_type", y_group_col="mpgge")
    hist = tc.generate_histogram(hist_col="discounted_tco_dol", n_bins=4, show_pct=True)

    assert isinstance(tco, go.Figure)
    assert isinstance(violin, go.Figure)
    assert isinstance(hist, go.Figure)
    # the TCO figure stacks one bar trace per cost component plus the TCO markers
    assert any(t.type == "bar" for t in tco.data)
    assert any(t.type == "scatter" for t in tco.data)


def test_plotly_ungrouped_tco(results_df):
    pytest.importorskip("plotly.graph_objects")
    tc = T3COCharts(results_df=results_df, backend="plotly")
    fig = tc.generate_tco_plots()  # no grouping
    assert fig is not None


def test_interactive_plot_has_xy_dropdowns(results_df):
    pytest.importorskip("plotly.graph_objects")
    tc = T3COCharts(results_df=results_df, backend="plotly")
    fig = tc.generate_interactive_plot(default_x="vehicle_fuel_type", default_y="discounted_tco_dol")

    # two dropdown menus: one for X, one for Y
    menus = fig.layout.updatemenus
    assert len(menus) == 2
    # each dropdown offers a button per candidate column, and switching swaps axis data
    for menu in menus:
        assert len(menu.buttons) >= 2
        assert menu.buttons[0].method == "update"
    # the initial axes reflect the requested defaults
    assert fig.layout.xaxis.title.text == tc._label("vehicle_fuel_type")
    assert fig.layout.yaxis.title.text == tc._label("discounted_tco_dol")


def test_save_default_plots_cli_hook(tmp_path, results_df):
    """The sweep --plot hook should write ONE combined HTML report next to the CSV."""
    pytest.importorskip("plotly.graph_objects")
    from t3co.cli.sweep import save_default_plots

    csv = tmp_path / "results.csv"
    results_df.to_csv(csv, index=False)
    saved = save_default_plots(csv, backend="plotly")

    # explorer + breakdown + histogram + violin, combined into a single HTML file
    assert len(saved) == 1
    report = saved[0]
    assert report.exists()
    assert report.suffix == ".html"
    assert report.parent == tmp_path
    # the report holds four plots in one page (incl. the interactive explorer)
    assert report.read_text().count('class="plotly-graph-div"') == 4


def test_write_html_report_combines_plots(tmp_path, results_df):
    pytest.importorskip("plotly.graph_objects")
    tc = T3COCharts(results_df=results_df, backend="plotly")
    figs = [
        tc.generate_tco_plots(x_group_col="vehicle_fuel_type"),
        tc.generate_histogram(hist_col="discounted_tco_dol", n_bins=4),
    ]
    out = T3COCharts.write_html_report(figs, tmp_path / "report.html")
    html = out.read_text()
    # both plots present in one page
    assert html.count('class="plotly-graph-div"') == 2
    # self-contained: the library is embedded inline, not loaded from a CDN <script src>
    assert 'src="https://cdn.plot.ly/plotly' not in html
    assert len(html) > 1_000_000


# ------------------------- matplotlib backend ------------------------- #
def test_matplotlib_figures(results_df):
    # matplotlib ships transitively with pymoo (a core dep), so the cost-breakdown
    # and histogram plots work without the viz extra; only the violin needs seaborn.
    mpl = pytest.importorskip("matplotlib")
    mpl.use("Agg")  # headless backend for CI
    from matplotlib.figure import Figure

    tc = T3COCharts(results_df=results_df, backend="matplotlib")

    tco = tc.generate_tco_plots(x_group_col="vehicle_fuel_type", subplot_group_col="vehicle_type")
    hist = tc.generate_histogram(hist_col="discounted_tco_dol", n_bins=4)

    assert isinstance(tco, Figure)
    assert isinstance(hist, Figure)


def test_matplotlib_violin_requires_seaborn(results_df):
    pytest.importorskip("seaborn")  # seaborn is only needed for the violin plot
    mpl = pytest.importorskip("matplotlib")
    mpl.use("Agg")
    from matplotlib.figure import Figure

    tc = T3COCharts(results_df=results_df, backend="matplotlib")
    violin = tc.generate_violin_plot(x_group_col="vehicle_fuel_type", y_group_col="mpgge")
    assert isinstance(violin, Figure)


def test_seaborn_alias_maps_to_matplotlib(results_df):
    tc = T3COCharts(results_df=results_df, backend="seaborn")
    assert tc.backend == "matplotlib"
