
![t3co_logo](https://github.com/user-attachments/assets/60623b62-57de-4475-b839-d7eb39405185)

[![homepage](https://img.shields.io/badge/homepage-t3co-blue)](https://www.nrel.gov/transportation/t3co.html) [![github](https://img.shields.io/badge/github-t3co-blue.svg)](https://github.com/NREL/T3CO) [![documentation](https://img.shields.io/badge/documentation-t3co-blue.svg)](https://nrel.github.io/T3CO/) [![PyPI - Version](https://img.shields.io/pypi/v/t3co)](https://pypi.org/project/t3co/) ![GitHub License](https://img.shields.io/github/license/NREL/T3CO) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/t3co) 


# **T3CO** : Transportation Technology Total Cost of Ownership Tool
## Description

This repo houses T3CO (Transportation Technology Total Cost of Ownership), software for modeling total cost of ownership for commercial vehicles with advanced powertrains.

To get started, read the [Quick Start Guide](https://github.com/NREL/T3CO/blob/1eefffc251fcbd2b0c0515512f51d1b27bb978fd/docs/quick_start.md)

For information on the T3CO models, go to the [Overview](https://github.com/NREL/T3CO/blob/264a730de942671eb2345a5afca7e1afd6d67666/docs/T3CO_Overview.md)

## Usage

**T3CO** is a general framework allowing a user to determine the total cost of ownership (TCO) of a FASTSim vehicle (paired with a FASTSim DriveCycle(s) for determining fuel efficiency). The user can also determine performance of gradability, acceleration, and range. In addition to straight TCO computation there is also the option to optimize a vehicle powertrain such that it meets performance optional targets while also optionally minimizing TCO.

## Installation
### Installing From [PyPI](https://pypi.org/project/t3co/)
T3CO can be easily installed from PyPI. This is the preferred method when using T3CO as a dependency for a project. To install the latest release:
```bash
pip install t3co
```

To install a specific version (for example T3CO v1.0.8):
```bash
pip install t3co==1.0.8
```

### From GitHub
T3CO can also be installed directly from the GitHub repository for accessing demo input files and running T3CO using the Command Line Interface.

First, clone the repository from [GitHub](https://github.com/NREL/T3CO):
```bash
git clone https://github.com/NREL/T3CO.git T3CO
```

From within the [Python environment](#setting-up-env) Navigate to the parent directory containing the T3CO repository e.g. `cd github/T3CO/` and run:
```bash
pip install -e .
```
This installs the local version of the T3CO clone along with all its [dependencies](https://github.com/NREL/T3CO/blob/29b0e848360b3b2de84b555bf52c52bf6e76134e/requirements.txt).


## Demo
**Using the [T3CO Config](https://github.com/NREL/T3CO/blob/c3df6421033cef7d35b7d7cd575ab94e85fcd9a9/t3co/resources/T3COConfig.csv) file**

Create a new `analysis_id` on `./t3co/resources/T3COConfig.csv` or update the existing rows and use them to run T3CO.

```bash
cd t3co
python sweep.py --analysis-id=0
```

**Using Command Line Arguments**

```bash
cd t3co
python sweep.py --skip_all_opt --selections  [1,2,3,4,5] --dst_dir .t3co_results/demodata
```


**using optimiztion in sweep module** [see](https://github.com/NREL/T3CO/blob/master/docs/optimization.md#optimization-from-sweep-module-)


## Acknowledgements
This tool was developed with funding support from the US Department of Energy's Office of Energy Efficiency and Renewable Energy (EERE)'s Vehicle Technology Office.

DOE NREL Software Record: [SWR-21-54](https://doi.org/10.11578/dc.20240806.4)

## To cite T3CO

*Lustbader, Jason, Panneer Selvam, Harish, Bennion, Kevin, Payne, Grant, Hunter, Chad, Penev, Michael, Brooker, Aaron, Baker, Chad, Birky, Alicia, Zhang, Chen, and Carow, Kyle. "T3CO (Transportation Technology Total Cost of Ownership) Open Source [SWR-21-54]." Computer software. September 16, 2024. https://github.com/NREL/T3CO. https://doi.org/10.11578/dc.20240806.4.*

