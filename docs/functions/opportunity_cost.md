# Table of Contents

* [tco.opportunity\_cost](#tco.opportunity_cost)
  * [OpportunityCost](#tco.opportunity_cost.OpportunityCost)
    * [\_\_init\_\_](#tco.opportunity_cost.OpportunityCost.__init__)
    * [set\_kdes](#tco.opportunity_cost.OpportunityCost.set_kdes)
    * [get\_payload\_loss\_factor](#tco.opportunity_cost.OpportunityCost.get_payload_loss_factor)
    * [get\_dwell\_time\_cost](#tco.opportunity_cost.OpportunityCost.get_dwell_time_cost)
    * [get\_M\_R\_downtime\_cost](#tco.opportunity_cost.OpportunityCost.get_M_R_downtime_cost)
  * [main](#tco.opportunity_cost.main)

<a id="tco.opportunity_cost"></a>

# tco.opportunity\_cost

<a id="tco.opportunity_cost.OpportunityCost"></a>

## OpportunityCost Objects

```python
class OpportunityCost()
```

This class is used to calculate the different opportunity costs for a scenario and vehicle
- Payload Capacity Cost Multiplier
- Fueling Downtime Cost
- Maintenance and Repair Downtime Cost

<a id="tco.opportunity_cost.OpportunityCost.__init__"></a>

#### \_\_init\_\_

```python
def __init__(scenario, range_dict=None, **kwargs)
```

Initializes OpportunityCost object using Scenario object, range_dict (from fueleconomy module), and other arguments

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object
- `range_dict` _dict, optional_ - dictionary containing primary_fuel_range_mi from fueleconomy.get_range_mi function. Defaults to None.

<a id="tco.opportunity_cost.OpportunityCost.set_kdes"></a>

#### set\_kdes

```python
def set_kdes(scenario, bw_method=0.15, verbose=False)
```

This method sets tje kde kernel. This is time-consuming, only call this once, if possible.

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object
- `bw_method` _float, optional_ - kernel bandwidth method used by guassian_kde. Defaults to .15.
- `verbose` _bool, optional_ - if True, prints process sets. Defaults to False.

<a id="tco.opportunity_cost.OpportunityCost.get_payload_loss_factor"></a>

#### get\_payload\_loss\_factor

```python
def get_payload_loss_factor(a_vehicle: fastsim.vehicle,
                            scenario,
                            plots=False,
                            plots_dir=None)
```

This method runs teh kernel density estimation function set_kdes and calculates the payload capacity loss factor (payload_cap_cost_multiplier)             of the new vehicle compared to a conventional vehicle's reference empty weight.

**Arguments**:

- `a_vehicle` _fastsim.vehicle_ - FASTSim vehicle object of the analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `plots` _bool, optional_ - if True, creates histogram of KDE weight bins. Defaults to False.
- `plots_dir` _str, optional_ - output diretory for saving plot figure. Defaults to None.

<a id="tco.opportunity_cost.OpportunityCost.get_dwell_time_cost"></a>

#### get\_dwell\_time\_cost

```python
def get_dwell_time_cost(a_vehicle: fastsim.vehicle, scenario)
```

This function calculates the fueling dwell time cost for a vehicle based on fuel fill rate/charging power and shifts_per_year

**Arguments**:

- `a_vehicle` _fastsim.vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object for current selection

<a id="tco.opportunity_cost.OpportunityCost.get_M_R_downtime_cost"></a>

#### get\_M\_R\_downtime\_cost

```python
def get_M_R_downtime_cost(a_vehicle: fastsim.vehicle, scenario)
```

This function calculates the Maintenance and Repair (M&R) downtime cost based on planned, unplanned, and tire replacement downtime inputs

**Arguments**:

- `a_vehicle` _fastsim.vehicle_ - FASTSim object of the analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object for the current selection

<a id="tco.opportunity_cost.main"></a>

#### main

```python
def main()
```

Runs the opportunity cost module as a standalone code based on input vehicles and scenarios

