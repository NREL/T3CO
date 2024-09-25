# Installation
## From [PyPI](https://pypi.org/project/t3co/)
```bash
pip install t3co
```

## From Github
First, clone the repository from [Github](https://github.com/NREL/T3CO) :

    git clone https://github.com/NREL/T3CO.git T3CO
    
t3co depends on python>=3.8 and <=3.10. One way to satisfy this is to use conda:

    conda create -n t3co python=3.8
    conda activate t3co


Navigate to the parent directory containing the T3CO repository e.g. `cd github/T3CO/` and run:

    pip install -e .

This installs the local version of T3CO along with all its dependencies. 

FASTSim is installed along with other library dependancies. In case of `ModuleNotFoundError: No module named 'fastsim'`:

    pip install fastsim


from within the t3co python 3.8 environment you created.  
    
This will install t3co with minimal dependencies such that t3co files can be editable. Developers will find the `-e` option handy since t3co will be installed in place from the installation location, and any updates will be propagated each time t3co is freshly imported.  


to be compatible with the current code in T3CO.

## Demo 
**get some quick TCO results**
```bash
cd run_scripts
python sweep.py -skip_all_opt -selections  [1,2,3,4,5] -dst_dir ./demodata
```

**using T3CO Config file**
```bash
cd run_scripts
pytho sweep.py -analysis_id 0
```

**using optimiztion in sweep module** [see](./models/optimization.md)

## Generate MD Documentation from Docstrings
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
pydoc-markdown -I . -p . --render-toc > CodeReference.md
```
for specific modules, specify the module name after `-m`:
`pydoc-markdown -I . -m run_scripts.sweep --render-toc > CodeReference.md`

This generates CodeReference.md including a Table of Contents from all python docstrings in the T3CO package