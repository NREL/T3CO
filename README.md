![T3CO Logo](https://www.nrel.gov/transportation/assets/images/t3co-icon-web.jpg)

# **T3CO** : Transportation Technology Total Cost of Ownership Tool
## Description

This repo houses T3CO (Transportation Technology Total Cost of Ownership), software for modeling total cost of ownership for commercial vehicles with advanced powertrains.

To start, go to the [Overview](https://github.com/NREL/T3CO-private/blob/264a730de942671eb2345a5afca7e1afd6d67666/docs/T3CO_Overview.md)

## Usage

**T3CO** is a general framework allowing a user to determine the total cost of ownership (TCO) of a FASTSim vehicle (paired with a FASTSim DriveCycle(s) for determining fuel efficiency). The user can also determine performance of gradability, acceleration, and range. In addition to straight TCO computation there is also the option to optimize a vehicle powertrain such that it meets performance optional targets while also optionally minimizing TCO.

### Note

Current release does **not** have:

- cargo `payload opportunity cost` combined with `gvwr_credit_kg` validated  

## Installation

First, clone the repository from **NREL** GitHub:

    git clone https://github.com/NREL/T3CO-private.git T3CO

t3co depends on python 3.8. One way to satisfy this is to use conda:

    conda create -n t3co python=3.8
    conda activate t3co

After creating the environment, navigate to the parent directory containing the T3CO repository e.g. `cd github/T3CO/` and run:

    pip install -e .

from within the t3co python 3.8 environment you created.  

This will install t3co with minimal dependencies such that t3co files can be editable. Developers will find the `-e` option handy since t3co will be installed in place from the installation location, and any updates will be propagated each time t3co is freshly imported.  

to be compatible with the current code in T3CO.

## Demo
**Using the T3CO Config file**

```bash
cd t3co
python sweep.py --analysis-id 0
```

** or get some quick TCO results**

```bash
cd t3co
python sweep.py --skip_all_opt --selections  [1,2,3,4,5] --dst_dir .t3co_results/demodata
```


**using optimiztion in sweep module** [see](https://github.com/NREL/T3CO-private/blob/master/docs/optimization.md#optimization-from-sweep-module-)

## Generate MD Documentation from Docstrings (For Developers)
**On Windows**

```bash
pip install --user pipx
pipx ensurepath
```

**On Mac**
```bash
brew install pipx
pipx ensurepath
```

Then from T3CO root directory
```bash
pipx install pydoc-markdown
pydoc-markdown -I . -p . --render-toc > ../docs/content/CodeReference.md
```
for specific modules, specify the module name after `-m`:
`pydoc-markdown -I . -m sweep --render-toc > ../docs/content/sweep.md`

This generates CodeReference.md including a Table of Contents from all python docstrings in the T3CO package

## Generate MKDocs server for documentation website  (For Developers)
Use the `mkdocs.yml` file to configure the documentation website on localhost. `mkdocs` and `mkdocstrings` should get installed along with other dependencies when running `pip install -e .` from the root directory. In case it throws an error, these packages can be installed separately:
```bash
pip install mkdocs
pip install mkdocstrings-python
```
**On Mac**

List the processes using the 8000 port on localhost using the command:
```bash
lsof -i tcp:8000
```
if a PID number shows up in the list for a process called `Python`, clear the port by killing it by replacing <PID> in the following command: 
```bash
kill -9 <PID>
```
Once the port is cleared, run the following line from the T3CO root directory to generate an MKDocs interactive documentation website on your localhost
```bash
mkdocs serve
```
