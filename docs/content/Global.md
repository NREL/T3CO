# Table of Contents

* [run.Global](#run.Global)
  * [DieselGalPerGasGal](#run.Global.DieselGalPerGasGal)
  * [kgH2\_per\_gge](#run.Global.kgH2_per_gge)
  * [mps\_to\_mph](#run.Global.mps_to_mph)
  * [m\_to\_mi](#run.Global.m_to_mi)
  * [get\_kwh\_per\_gge](#run.Global.get_kwh_per_gge)
  * [set\_tco\_intermediates](#run.Global.set_tco_intermediates)
  * [set\_tco\_results](#run.Global.set_tco_results)
  * [kg\_to\_lbs](#run.Global.kg_to_lbs)
  * [lbs\_to\_kgs](#run.Global.lbs_to_kgs)
  * [not\_falsy](#run.Global.not_falsy)

<a id="run.Global"></a>

# run.Global

Global constants
Stores paths to directories used for input files, as well as constants referenced throughout the code base

<a id="run.Global.DieselGalPerGasGal"></a>

#### DieselGalPerGasGal

energy equivalent gallons of diesel per 1 gallon gas

<a id="run.Global.kgH2_per_gge"></a>

#### kgH2\_per\_gge

https://epact.energy.gov/fuel-conversion-factors for Hydrogen

<a id="run.Global.mps_to_mph"></a>

#### mps\_to\_mph

1 mps = 2.23694 mph

<a id="run.Global.m_to_mi"></a>

#### m\_to\_mi

1 m = 0.000621371 mi

<a id="run.Global.get_kwh_per_gge"></a>

#### get\_kwh\_per\_gge

```python
def get_kwh_per_gge()
```

This is a getter for kwh_per_gge, sim and scenario dependant var that can change
important to get from one location each time so we can track when and how it's used

**Returns**:

- `kwh_per_gge` _float_ - kWh per Gasoline Gallon Equivalent

<a id="run.Global.set_tco_intermediates"></a>

#### set\_tco\_intermediates

```python
def set_tco_intermediates()
```

This function sets path for TCO_INTERMEDIATES to save tsv files

<a id="run.Global.set_tco_results"></a>

#### set\_tco\_results

```python
def set_tco_results()
```

This function sets path for TCO_RESULTS

<a id="run.Global.kg_to_lbs"></a>

#### kg\_to\_lbs

```python
def kg_to_lbs(kgs)
```

This function converts kg to lb

**Arguments**:

- `kgs` _float_ - mass in kg
  

**Returns**:

- `(float)` - mass in pounds

<a id="run.Global.lbs_to_kgs"></a>

#### lbs\_to\_kgs

```python
def lbs_to_kgs(lbs)
```

This function converts lb to kg

**Arguments**:

- `lbs` _float_ - mass in pounds
  

**Returns**:

- `(float)` - mass in kg

<a id="run.Global.not_falsy"></a>

#### not\_falsy

```python
def not_falsy(var)
```

This function returns True to verify that var is NOT falsy: not in [None, np.nan, 0, False]


**Arguments**:

- `var` _float_ - variable to check
  

**Returns**:

- `(bool)` - True if not in [None, 0, False]

