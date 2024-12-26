# Table of Contents

* [t3co/visualization/charts](#t3co/visualization/charts)
  * [T3COCharts](#t3co/visualization/charts.T3COCharts)
    * [\_\_init\_\_](#t3co/visualization/charts.T3COCharts.__init__)
    * [from\_file](#t3co/visualization/charts.T3COCharts.from_file)
    * [from\_df](#t3co/visualization/charts.T3COCharts.from_df)
    * [to\_df](#t3co/visualization/charts.T3COCharts.to_df)
    * [parse\_scenario\_name](#t3co/visualization/charts.T3COCharts.parse_scenario_name)
    * [generate\_tco\_plots](#t3co/visualization/charts.T3COCharts.generate_tco_plots)
    * [generate\_violin\_plot](#t3co/visualization/charts.T3COCharts.generate_violin_plot)
    * [generate\_histogram](#t3co/visualization/charts.T3COCharts.generate_histogram)

<a id="t3co/visualization/charts"></a>

# t3co/visualization/charts

<a id="t3co/visualization/charts.T3COCharts"></a>

## T3COCharts Objects

```python
class T3COCharts()
```

This class takes T3CO output CSV file as input and generates different plots to gain insights from T3CO Results

<a id="t3co/visualization/charts.T3COCharts.__init__"></a>

#### \_\_init\_\_

```python
def __init__(
    filename: str = None,
    results_df: pd.DataFrame = None,
    results_guide: str | Path = Path(__file__).parents[1] / "resources" /
    "visualization" / "t3co_outputs_guide.csv"
) -> None
```

This constructor initializes the T3COCharts object either from a dataframe or a CSV file path.

**Arguments**:

- `filename` _str, optional_ - Filepath to T3CO Results CSV File. Defaults to None.
- `results_df` _pd.DataFrame, optional_ - Input pandas dataframe containing T3CO Results. Defaults to None.
- `results_guide` _str | Path, optional_ - File path to t3co_outputs_guide.csv file that contains useful parameter descriptions and axis labels. Defaults to Path(__file__).parents[1]/"resources"/"visualization"/"t3co_outputs_guide.csv".

<a id="t3co/visualization/charts.T3COCharts.from_file"></a>

#### from\_file

```python
def from_file(filename: str | Path = None) -> None
```

This method reads a T3CO Results CSV file into a dataframe

**Arguments**:

- `filename` _str | Path, optional_ - Path to T3CO Results CSV File. Defaults to None.

<a id="t3co/visualization/charts.T3COCharts.from_df"></a>

#### from\_df

```python
def from_df(results_df: pd.DataFrame) -> None
```

This method reads t3co_results from a dataframe

**Arguments**:

- `results_df` _pd.DataFrame_ - Input T3CO Results dataframe

<a id="t3co/visualization/charts.T3COCharts.to_df"></a>

#### to\_df

```python
def to_df() -> pd.DataFrame
```

This returns the self.t3co_results member

**Returns**:

- `pd.DataFrame` - T3CO Results dataframe

<a id="t3co/visualization/charts.T3COCharts.parse_scenario_name"></a>

#### parse\_scenario\_name

```python
def parse_scenario_name() -> None
```

This method parses 'scenario_name' into 'vehicle_type', 'tech_progress', and 'vehicle_fuel_type' and uses 'scenario_gvwr_kg' to create 'vehicle_weight_class'

<a id="t3co/visualization/charts.T3COCharts.generate_tco_plots"></a>

#### generate\_tco\_plots

```python
def generate_tco_plots(x_group_col: str,
                       y_group_col: str,
                       subplot_group_col: str = "vehicle_fuel_type",
                       fig_x_size: int = 8,
                       fig_y_size: int = 8,
                       bar_width: float = 0.8,
                       legend_pos: float = 0.25,
                       edgecolor: str = "none") -> matplotlib.figure.Figure
```

This method generates a TCO Breakdown plot based on input arguments.
If x_group_col and/or y_group_col are provided, then a matrix/grid of subplots are generated within the same figure based on row- and column-wise groupings

**Arguments**:

- `x_group_col` _str_ - T3CO Results parameter name to group on x-axis, i.e., grouping criteria for columns in subplots grid
- `y_group_col` _str_ - T3CO Results parameter name to group on y-axis, i.e., grouping criteria for rows in subplots grid
- `subplot_group_col` _str, optional_ - T3CO Results parameter to display within each subplots cell. Defaults to "vehicle_fuel_type".
- `fig_x_size` _int, optional_ - Figure width relative to each bar on x-axis within subplot. Defaults to 8.
- `fig_y_size` _int, optional_ - Figure height relative to each subplot cell. Defaults to 8.
- `bar_width` _float, optional_ - Relative width of bars based on available width. Takes values between 0.0 and 1.0. Defaults to 0.8.
- `legend_pos` _float, optional_ - Relative position of legend on the right side of plots. Takes values between 0.0 and 1.0. Defaults to 0.25.
- `edgecolor` _str, optional_ - Edge color to distinguish cost elements in the stacked bars. Defaults to "none".
  

**Returns**:

- `matplotlib.figure.Figure` - TCO Breakdown Figure object

<a id="t3co/visualization/charts.T3COCharts.generate_violin_plot"></a>

#### generate\_violin\_plot

```python
def generate_violin_plot(
        x_group_col: str,
        y_group_col: str = "discounted_tco_dol") -> matplotlib.figure.Figure
```

This method generates a violin plot based on x-axis group column and y-axis column name.

**Arguments**:

- `x_group_col` _str_ - T3CO Results parameter to group by on x-axis inside violinplot
- `y_group_col` _str, optional_ - T3CO Results parameter to plot on y-axis. Defaults to "discounted_tco_dol".
  

**Returns**:

- `matplotlib.figure.Figure` - Violin Plot Figure object

<a id="t3co/visualization/charts.T3COCharts.generate_histogram"></a>

#### generate\_histogram

```python
def generate_histogram(hist_col: str,
                       n_bins: int,
                       show_pct: bool = False) -> matplotlib.figure.Figure
```

This method generates a histogram plot based on inputs hist_col and n_bins

**Arguments**:

- `hist_col` _str_ - T3CO column name to plot histogram
- `n_bins` _int_ - Number of bins in histogram
- `show_pct` _bool, optional_ - If True, plots percentage on y-axis instead of number of items. Defaults to False.
  

**Returns**:

- `matplotlib.figure.Figure` - Histogram figure object

