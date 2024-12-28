# Installation
## Setting Up a Python Environment <a name="setting-up-env"></a>
This package depends on [Python](https://www.python.org/downloads/)>=3.8 and <=3.10. To create an environment containing the appropriate Python version and a built-in `pip`, there are two preferred ways:

1. First option is to use [**conda**](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html):

    ```bash
    conda create -n nrel_package python=3.10
    conda activate nrel_package
    ```

2. The other option is using [venv](https://docs.python.org/3/library/venv.html)

    ```bash
    python3.10 -m venv nrel_package
    ```

    On macOS/Linux, activate the environment:

    ```bash
    source nrel_package/bin/activate
    ```

    On Windows Powershell:
    
    ```bash
    nrel_package\Scripts\activate
    ```

## Installing nrel_package Python Package
nrel_package is available on PyPI and as a public access GitHub repository. This gives the user two ways of installing the nrel_package Python Package.
### 1. Installing From [PyPI](https://pypi.org/project/nrel_package/) <a name=install-from-pypi></a>
nrel_package can be easily installed from PyPI. This is the preferred method when using nrel_package to run analysis using input files. To install the latest release:
```bash
pip install nrel_package
```

To install a specific version (for example nrel_package v1.0.8):
```bash
pip install nrel_package==1.0.8
```

### 2. From [GitHub](https://github.com/NREL/nrel_package)
nrel_package can also be installed directly from the GitHub repository for accessing demo input files and running nrel_package using the Command Line Interface.

First, [clone](https://git-scm.com/docs/git-clone) the repository from [GitHub](https://github.com/NREL/nrel_package):
```bash
git clone https://github.nrel.gov/AVCI/nrel-python-package-template.git nrel_package
```

From within the [Python environment](#setting-up-env) Navigate to the parent directory containing the nrel_package repository e.g. `cd GitHub/nrel_package/` and run:
```bash
pip install -e .
```
This installs the local version of the nrel_package clone along with all its [dependencies](https://github.nrel.gov/AVCI/nrel-python-package-template/blob/3ab424fec5c24ca0bcf7e0983aa72b781ab60a23/requirements.txt).


Check that the right version of nrel_package is installed in your environment:
```bash
pip show nrel_package
```

If there are updates or new releases to nrel_package that don't show in the local version, use a `git pull` command the latest version from the `main` branch on the repo:
```bash
git pull origin main
```


## Copying nrel_package Demo Input Files <a name=copy-demo-inputs></a>
The `nrel_package.resources` folder contains all the necessary input files needed for running nrel_package. However, it sometimes is difficult to navigate to these files when installing. To help with this, run this command on the Command Line Interface.

```bash
install_nrel_package_demo_inputs
```

The user will receive these questions on the command line:

`Do you want to copy the nrel_package demo input files? (y/n):` 

`Enter the path where you want to copy demo input files:`

Choose `y` and provide the desired destination path (relative or absolute) to get a `demo_inputs` folder containing the `nrel_package.resources` files copied to your local directory. To copy to the current directory, provide `.` as the path. 

## Running your first analysis
To learn about the tool and run your first nrel_package analysis, proceed to the [Quick Start Guide](./quick_start.md)
