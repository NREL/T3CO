
![t3co_logo](https://github.com/user-attachments/assets/60623b62-57de-4475-b839-d7eb39405185)

[![homepage](https://img.shields.io/badge/homepage-t3co-blue)](https://www.nrel.gov/transportation/t3co.html) [![github](https://img.shields.io/badge/github-t3co-blue.svg)](https://github.com/NREL/T3CO) [![documentation](https://img.shields.io/badge/documentation-t3co-blue.svg)](https://nrel.github.io/T3CO/) [![PyPI - Version](https://img.shields.io/pypi/v/t3co)](https://pypi.org/project/t3co/) ![GitHub License](https://img.shields.io/github/license/NREL/T3CO) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/t3co) 


# **T3CO** : Transportation Technology Total Cost of Ownership Tool
## Description

This repo houses T3CO (Transportation Technology Total Cost of Ownership), software for modeling total cost of ownership for commercial vehicles with advanced powertrains.

To get started, read the [Quick Start Guide](https://github.com/NREL/T3CO/blob/main/docs/quick_start.md)

For information on the T3CO models, go to the [Overview](https://github.com/NREL/T3CO/blob/main/docs/T3CO_Overview.md)

## Usage

**T3CO** is a general framework allowing a user to determine the total cost of ownership (TCO) of a FASTSim vehicle (paired with a FASTSim DriveCycle(s) for determining fuel efficiency). The user can also determine performance of gradeability, acceleration, and range. In addition to straight TCO computation there is also the option to optimize a vehicle powertrain such that it meets performance optional targets while also optionally minimizing TCO.

## Installation
T3CO is available on PyPI and as a public access GitHub repository. This gives the user two ways of installing the T3CO Python Package.
### 1. Installing From [PyPI](https://pypi.org/project/t3co/)
```bash
pip install t3co
```

### 2. Cloning the [GitHub Repo](https://github.com/NREL/T3CO)
T3CO can also be installed directly from a clone of the GitHub repository which makes it easier to access input files and run the tool using a Command Line Interface.

First, [clone](https://git-scm.com/docs/git-clone) the repository from [GitHub](https://github.com/NREL/T3CO) from your desired directory:
```bash
git clone https://github.com/NREL/T3CO.git T3CO
```

From within the [Python environment](./docs/installation.md#setting-up-env), navigate to the parent directory containing the T3CO repository (e.g. `cd GitHub/T3CO/`) and run:
```bash
pip install -e .
```
This installs the local version of the T3CO clone along with all its [dependencies](https://github.com/NREL/T3CO/blob/main/requirements.txt).

### Copying the Demo Input Files
The [`t3co.resources`](https://github.com/NREL/T3CO/tree/main/t3co/resources) folder contains all the necessary input files needed for running T3CO. To get an offline copy of this folder in your preferred directory, run:
```bash
install_t3co_demo_inputs
```

More information on the demo input files can be found in the [Installation Guide](https://github.com/NREL/T3CO/blob/main/docs/installation.md#copy-demo-inputs)


## Running T3CO
T3CO needs three main input files (*Vehicles*, *Scenarios*, and *Config*) to run an analysis. The analysis settings, file paths to main and auxiliary input files, and other parameter overrides are saved as an entry on the *Config* file. The user is provided with 500+ *Vehicle-Scenario* pairs inputs and four *Config* sample analyses to choose from to modify parameters and/or run their first T3CO analysis. The main module for T3CO,`t3co.sweep`, can be run using:

```bash
python -m t3co.sweep --analysis-id=0 --config=<path/to/T3COConfig.csv>
```

Point the `--config` argument to the `T3COConfig.csv` file path (either the t3co/resource/T3COConfig.csv file in a repo clone or the demo_inputs/T3COConfig.csv file after copying the demo input files. This parameter defaults to the T3COConfig.csv file in the t3co.resources module) and `--analysis-id` to the desired `config.analysis_id` (either an existing row or a newly added "Analysis" row in the `T3COConfig.csv` file. Default = `0`).

Additional information on the inputs, the Batch Mode feature, other CLI arguments, and description of T3CO results are mentioned in the [Quick Start Guide](https://github.com/NREL/T3CO/blob/main/docs/quick_start.md)

## Acknowledgements
This tool was developed with funding support from the US Department of Energy's Office of Energy Efficiency and Renewable Energy (EERE)'s Vehicle Technology Office.

DOE NREL Software Record: [SWR-21-54](https://doi.org/10.11578/dc.20240806.4)

## To cite T3CO

*Lustbader, Jason, Panneer Selvam, Harish, Bennion, Kevin, Payne, Grant, Hunter, Chad, Penev, Michael, Brooker, Aaron, Baker, Chad, Birky, Alicia, Zhang, Chen, and Carow, Kyle. "T3CO (Transportation Technology Total Cost of Ownership) Open Source [SWR-21-54]." Computer software. September 16, 2024. https://github.com/NREL/T3CO. https://doi.org/10.11578/dc.20240806.4.*

