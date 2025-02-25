
![t3co_logo](https://github.com/user-attachments/assets/60623b62-57de-4475-b839-d7eb39405185)

[![homepage](https://img.shields.io/badge/homepage-t3co-blue)](https://www.nrel.gov/transportation/t3co.html) [![github](https://img.shields.io/badge/github-t3co-blue.svg)](https://github.com/NREL/T3CO) [![documentation](https://img.shields.io/badge/documentation-t3co-blue.svg)](https://nrel.github.io/T3CO/) [![PyPI - Version](https://img.shields.io/pypi/v/t3co)](https://pypi.org/project/t3co/) ![GitHub License](https://img.shields.io/github/license/NREL/T3CO) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/t3co) 


# **T3CO** : Transportation Technology Total Cost of Ownership Tool
## Description

This repo houses T3CO (Transportation Technology Total Cost of Ownership), software for modeling total cost of ownership for commercial vehicles with advanced powertrains.

To get started, read the [Quick Start Guide](./docs/quick_start.md)

For detailed installation instructions, read the [Installation Guide](./docs/installation.md)

For information on the T3CO models, go to the [Overview](./docs/T3CO_Overview.md)

## Usage

**T3CO** is a general framework allowing a user to determine the total cost of ownership (TCO) of a vehicle (sometimes a FASTSim vehicle model paired with drivecycle(s) for determining fuel efficiency). The user can also determine performance of gradeability, acceleration, and range. In addition to straight TCO computation there is also the option to optimize a vehicle powertrain such that it meets performance optional targets while also optionally minimizing TCO.

## Installation

T3CO is available on PyPI and as a public access GitHub repository. This gives the user **two sources** from where T3CO Python Package can be obtained and installed.

### Installation 'Extras'

The user can choose one of three installation options or 'extras' of T3CO based on their desired tool capabilities. 

- T3CO as a pure cost estimation tool with exogenous inputs (default version `t3co` - requires Python>=3.9, <=3.13)
- T3CO integrated with FASTSim for energy simulation (`t3co[fastsim]`, requires Python>=3.9,<=3.10)
- T3CO for developers and quality testers that includes all capabilities (`t3co[dev]` requires Python>=3.9,<=3.10)
The different 'extras' refers to different sets of dependencies that get installed along with T3CO.


### Installation Source #1: From [PyPI](https://pypi.org/project/t3co/)

After creating a version-appropriate [Python environment](./docs/installation.md#setting-up-env), the latest release of T3CO can be installed from PyPI using one of the following commands.

For the default option/extra:

```bash
pip install t3co
```

For the FASTSim-integrated 'extra':

```bash
pip install t3co[fastsim]
```

For the developer 'extra':

```bash
pip install t3co[dev]
```

### Installation Source #2: Cloning the [GitHub Repo](https://github.com/NREL/T3CO)

T3CO can also be installed from a clone of the GitHub repository.

First, [clone](https://git-scm.com/docs/git-clone) the repository from [GitHub](https://github.com/NREL/T3CO) from your desired directory (eg., /Users/Projects/):

```bash
git clone https://github.com/NREL/T3CO.git T3CO
```

This creates a git compliant folder 'T3CO' (i.e., a '/Users/Projects/T3CO' folder)

To access the `t3co-2.0` branch,

```bash
git checkout t3co-2.0
```

From within the [Python environment](./docs/installation.md#setting-up-env), navigate to the parent directory containing the T3CO repository (`cd T3CO`) and run one of these three installation options:


For the default option/extra:

```bash
pip install -e .
```

For the FASTSim-integrated 'extra':

```bash
pip install -e .[fastsim]
```

For the developer 'extra':

```bash
pip install -e .[dev]
```

### Copying the Demo Input Files
The [`t3co.resources`](./src/t3co/resources) module folder contains all the necessary input files needed for running T3CO. To get an offline copy of this folder in your preferred directory, run:
```bash
install_t3co_demo_inputs
```

More information on the demo input files can be found in the [Installation Guide](./docs/installation.md#copy-demo-inputs)


## Running T3CO
T3CO needs three main input files (*Vehicles*, *Scenarios*, and *Config*) to run an analysis. The analysis settings, file paths to main and auxiliary input files, and other parameter overrides are saved as an entry on the *Config* file. The user is provided with 500+ *Vehicle-Scenario* pairs inputs and four *Config* sample analyses to choose from to modify parameters and/or run their first T3CO analysis. The main module for T3CO,`t3co.cli.sweep`, can be run using:

```bash
python -m t3co.cli.sweep --analysis-id=0 --config=<path/to/T3COConfig.csv>
```

Point the `--config` argument to the `T3COConfig.csv` file path (either the src/t3co/resource/T3COConfig.csv file in a repo clone or the demo_inputs/T3COConfig.csv file after copying the demo input files. This parameter defaults to the T3COConfig.csv file in the t3co.resources module) and `--analysis-id` to the desired `config.analysis_id` (either an existing row or a newly added "Analysis" row in the `T3COConfig.csv` file. Default = `0`).

Additional information on the inputs, the Batch Mode feature, other CLI arguments, and description of T3CO results are mentioned in the [Quick Start Guide](./docs/quick_start.md)

## Acknowledgements

This tool was developed with funding support from the US Department of Energy's Office of Energy Efficiency and Renewable Energy (EERE)'s Vehicle Technology Office.

DOE NREL Software Record: [SWR-21-54](https://doi.org/10.11578/dc.20240806.4)

## To cite T3CO

*Lustbader, Jason, Panneer Selvam, Harish, Bennion, Kevin, Payne, Grant, Hunter, Chad, Penev, Michael, Brooker, Aaron, Baker, Chad, Birky, Alicia, Zhang, Chen, and Carow, Kyle. "T3CO (Transportation Technology Total Cost of Ownership) Open Source [SWR-21-54]." Computer software. September 16, 2024. https://github.com/NREL/T3CO. https://doi.org/10.11578/dc.20240806.4.*


## Contact Us
To reach out to the NREL developer team with feedback, feature requests, or to explore partnership opportunities, please email at [T3CO@nrel.gov](mailto:T3CO@nrel.gov)

This tool is developed and maintained by the Commercial Vehicle Technologies (CVT) team in NREL's Center for Integrated Mobility Sciences.