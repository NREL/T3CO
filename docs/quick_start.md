# Quick Start Guide to T3CO

This guide will help you get started with T3CO quickly, from understanding inputs to running your first analysis and visualizing results.

## Overview

T3CO (Transportation Technology Total Cost of Ownership) calculates the total cost of owning and operating different vehicle technologies. A successful analysis requires:

1. Input files that define your vehicles and scenarios
2. Running the T3CO analysis
3. Reviewing and visualizing the results

## Step 1: Get the Demo Input Files

T3CO comes with over 500 pre-configured demo scenarios to help you get started. These serve as templates that you can modify for your own analyses.

To get a local copy of these demo files:

```bash
install_t3co_demo_inputs
```

When prompted:

- Answer `y` to copy the files
- Enter a path where you want the files, or `.` (period) for the current directory

This creates a `demo_inputs` folder with all the necessary files to run T3CO.

## Step 2: Understand the Input Files

T3CO requires three main input files:

### 1. Vehicle File

The [***Vehicle***](vehicle_inputs_descriptions.md) file defines the technical specifications of different vehicles. It includes:

- Vehicle type (car, truck, bus, etc.)
- Powertrain characteristics (engine power, battery capacity, etc.)
- Physical properties (weight, aerodynamics, etc.)

Each vehicle is identified by a unique `vehicle.selection` value.

### 2. Scenario File

The [***Scenario***](scenario_inputs_descriptions.md) file defines the cost and operational parameters:

- Fuel prices and electricity costs
- Annual mileage and lifetime
- Financing terms and interest rates
- Infrastructure requirements

Each scenario is identified by a `scenario.selection` value that matches its corresponding vehicle.

### 3. Config File

The [***Config***](config_inputs_descriptions.md) file controls which analyses to run and where to find all input files:

- Which vehicle-scenario pairs to analyze (`config.selections`)
- Paths to input and output files
- Global parameter overrides
- Optimization settings

Each analysis configuration is identified by a `config.analysis_id`.

### Auxiliary Input Files

Additional files in the `auxiliary` folder provide supporting data like:

- Fuel price projections
- Residual value assumptions
- Cost curves for technology improvements

## Step 3: Run Your First Analysis

Now let's run a simple analysis using the demo files:

### If You Installed T3CO from PyPI

Navigate to the directory where you copied the demo files and run:

```bash
python -m t3co.sweep --analysis-id=0 --config=demo_inputs/T3COConfig.csv
```

### If You Cloned the GitHub Repository

Navigate to the T3CO repository directory and run:

```bash
python -m t3co.sweep --analysis-id=0
```

This runs the analysis defined in row 0 of the Config file, which analyzes several vehicle types.

## Step 4: Understand the Results

After running the analysis, T3CO creates a results CSV file in the output directory (default is `./results`). This file contains:

- **Cost outputs**: Total costs broken down by category (vehicle, fuel, maintenance, etc.)
- **Vehicle parameters**: All the input vehicle specifications
- **Scenario parameters**: All the input scenario parameters
- **Optimization results**: If optimization was enabled, the optimized parameters

## Step 5: Visualize Your Results

T3CO includes tools to visualize your results:

```bash
python -m t3co.demos.visualization_demo
```

This generates three types of visualizations:

1. **TCO Breakdown Chart**: Shows cost components for each vehicle

<img src="https://raw.githubusercontent.com/NREL/T3CO/refs/heads/main/docs/tco_breakdown_sample.png" alt="tcobreakdown" width="650"/>

2. **Histogram Plot**: Compares a specific metric across vehicle types

<img src="https://raw.githubusercontent.com/NREL/T3CO/refs/heads/main/docs/histogram_sample.png" alt="histogram" width="400"/>

3. **Violin Plot**: Shows the distribution of values for a specific metric

<img src="https://raw.githubusercontent.com/NREL/T3CO/refs/heads/main/docs/violinplot_sample.png" alt="violinplot" width="400"/>
## Advanced Features

### Running Multiple Analyses in Parallel

To speed up processing, use the multiprocessing option:

```bash
python -m t3co.sweep --analysis-id=0 --run-multi --n-processors=4
```

Adjust the number of processors based on your computer's capabilities (usually use 1-2 less than your total cores).

### Running Batch Analyses with Multiple Drive Cycles

For analyses involving multiple drive cycles:

```bash
python -m t3co.sweep --analysis-id=3
```

This special analysis mode automatically creates scenarios for each drive cycle in a specified folder.

### Customizing Your Analysis

You can modify existing analyses or create new ones:

1. Open the Config file (`T3COConfig.csv`) in a spreadsheet program
2. Duplicate an existing row
3. Update the `analysis_id` to a new value
4. Modify the parameters as needed
5. Save the file
6. Run T3CO with your new analysis ID

## Getting Help

For a full list of command-line options:

```bash
python -m t3co.sweep --help
```

## Next Steps

- Explore the [T3CO Overview](./T3CO_Overview.md) for more details on the underlying models
- Review the [Vehicle Input Descriptions](./vehicle_inputs_descriptions.md) and [Scenario Input Descriptions](./scenario_inputs_descriptions.md) to customize your analyses
- Learn about [T3CO Modules](./t3co_modules.md) to understand the calculation methodology
