# Installation
## Setting Up a Python Environment <a name="setting-up-env"></a>
T3CO depends on [Python](https://www.python.org/downloads/)>=3.8 and <=3.10. To create an environment containing the appropriate Python version and a built-in `pip`, there are two preferred ways:

1. First option is to use [**conda**](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html):

    ```bash
    conda create -n t3co python=3.10
    conda activate t3co
    ```

2. The other option is using [venv](https://docs.python.org/3/library/venv.html)

    ```bash
    python3.10 -m venv t3co
    ```

    On macOS/Linux, activate the environment:

    ```bash
    source t3co/bin/activate
    ```

    On Windows Powershell:
    
    ```bash
    t3co\Scripts\activate
    ```

## Installing T3CO Python Package
T3CO is available on PyPI and as a public access GitHub repository. This gives the user two ways of installing the T3CO Python Package.
### 1. Installing From [PyPI](https://pypi.org/project/t3co/) <a name=install-from-pypi></a>
T3CO can be easily installed from PyPI. This is the preferred method for using T3CO to run analysis with input files. To install the latest release:
```bash
pip install t3co
```

To install a specific version (for example T3CO v1.0.8):
```bash
pip install t3co==1.0.8
```

### 2. From [GitHub](https://github.com/NREL/T3CO)
T3CO can also be installed directly from the GitHub repository for accessing demo input files and running T3CO using the Command Line Interface.

First, [clone](https://git-scm.com/docs/git-clone) the repository from [GitHub](https://github.com/NREL/T3CO):
```bash
git clone https://github.com/NREL/T3CO.git T3CO
```

From within the [Python environment](#setting-up-env) Navigate to the parent directory containing the T3CO repository e.g. `cd GitHub/T3CO/` and run:
```bash
pip install -e .
```
This installs the local version of the T3CO clone along with all its [dependencies](https://github.com/NREL/T3CO/blob/29b0e848360b3b2de84b555bf52c52bf6e76134e/requirements.txt).

FASTSim is installed along with other library dependancies. In case of `ModuleNotFoundError: No module named 'fastsim'` error:
```bash
pip install fastsim==2.1.1
```

Check that the right version of T3CO is installed in your environment:
```bash
pip show t3co
```

If there are updates or new releases to T3CO that don't show in the local version, use a `git pull` command the latest version from the `main` branch on the repo:
```bash
git pull origin main
```


## Copying T3CO Demo Input Files <a name=copy-demo-inputs></a>
The `t3co.resources` folder contains all the necessary input files needed for running T3CO. However, it sometimes is difficult to navigate to these files when installing. To help with this, run this command on the Command Line Interface.

```bash
install_t3co_demo_inputs
```

The user will receive these questions on the command line:

`Do you want to copy the T3CO demo input files? (y/n):`

`Enter the path where you want to copy demo input files:`

Choose `y` and provide the desired destination path to get a `demo_inputs` folder containing the `t3co.resources` files copied to your local directory. To copy the folder to the current directory you are on, answer the second question with ".".

## Running your first analysis
To learn about the tool and run your first T3CO analysis, proceed to the [Quick Start Guide](./quick_start.md)