# Table of Contents

* [t3co/tco/opportunity\_cost](#t3co/tco/opportunity_cost)
  * [OpportunityCost](#t3co/tco/opportunity_cost.OpportunityCost)
    * [\_\_init\_\_](#t3co/tco/opportunity_cost.OpportunityCost.__init__)
    * [set\_kdes](#t3co/tco/opportunity_cost.OpportunityCost.set_kdes)
    * [set\_payload\_loss\_factor](#t3co/tco/opportunity_cost.OpportunityCost.set_payload_loss_factor)
    * [set\_fueling\_dwell\_time\_cost](#t3co/tco/opportunity_cost.OpportunityCost.set_fueling_dwell_time_cost)
    * [set\_M\_R\_downtime\_cost](#t3co/tco/opportunity_cost.OpportunityCost.set_M_R_downtime_cost)
  * [main](#t3co/tco/opportunity_cost.main)

<a id="t3co/tco/opportunity_cost"></a>

# t3co/tco/opportunity\_cost

<a id="t3co/tco/opportunity_cost.OpportunityCost"></a>

## OpportunityCost Objects

```python
class OpportunityCost()
```

This class is used to calculate the different opportunity costs for a scenario and vehicle
- Payload Capacity Cost Multiplier
- Fueling Downtime Cost
- Maintenance and Repair Downtime Cost

<a id="t3co/tco/opportunity_cost.OpportunityCost.__init__"></a>

#### \_\_init\_\_

```python
def __init__(scenario: run_scenario.Scenario,
             range_dict: dict = None,
             **kwargs) -> None
```

Initializes OpportunityCost object using Scenario object, range_dict (from fueleconomy module), and other arguments

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object
- `range_dict` _dict, optional_ - dictionary containing primary_fuel_range_mi from fueleconomy.get_range_mi function. Defaults to None.

<a id="t3co/tco/opportunity_cost.OpportunityCost.set_kdes"></a>

#### set\_kdes

```python
def set_kdes(scenario: run_scenario.Scenario,
             bw_method: float = 0.15,
             verbose: bool = False) -> None
```

This method sets tje kde kernel. This is time-consuming, only call this once, if possible.

**Arguments**:

- `scenario` _run_scenario.Scenario_ - Scenario object
- `bw_method` _float, optional_ - kernel bandwidth method used by guassian_kde. Defaults to .15.
- `verbose` _bool, optional_ - if True, prints process sets. Defaults to False.

<a id="t3co/tco/opportunity_cost.OpportunityCost.set_payload_loss_factor"></a>

#### set\_payload\_loss\_factor

```python
def set_payload_loss_factor(a_vehicle: fastsim.vehicle.Vehicle,
                            scenario: run_scenario.Scenario,
                            plots: bool = False,
                            plots_dir: str = None) -> None
```

This method runs teh kernel density estimation function set_kdes and calculates the payload capacity loss factor (payload_cap_cost_multiplier)             of the new vehicle compared to a conventional vehicle's reference empty weight.

**Arguments**:

- `a_vehicle` _fastsim.vehicle_ - FASTSim vehicle object of the analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object of current selection
- `plots` _bool, optional_ - if True, creates histogram of KDE weight bins. Defaults to False.
- `plots_dir` _str, optional_ - output diretory for saving plot figure. Defaults to None.

<a id="t3co/tco/opportunity_cost.OpportunityCost.set_fueling_dwell_time_cost"></a>

#### set\_fueling\_dwell\_time\_cost

```python
def set_fueling_dwell_time_cost(a_vehicle: fastsim.vehicle.Vehicle,
                                scenario: run_scenario.Scenario) -> None
```

This function calculates the fueling dwell time cost for a vehicle based on fuel fill rate/charging power and shifts_per_year

**Arguments**:

- `a_vehicle` _fastsim.vehicle_ - FASTSim vehicle object of analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object for current selection

<a id="t3co/tco/opportunity_cost.OpportunityCost.set_M_R_downtime_cost"></a>

#### set\_M\_R\_downtime\_cost

```python
def set_M_R_downtime_cost(a_vehicle: fastsim.vehicle.Vehicle,
                          scenario: run_scenario.Scenario) -> None
```

This function calculates the Maintenance and Repair (M&R) downtime cost based on planned, unplanned, and tire replacement downtime inputs

**Arguments**:

- `a_vehicle` _fastsim.vehicle_ - FASTSim object of the analysis vehicle
- `scenario` _run_scenario.Scenario_ - Scenario object for the current selection

<a id="t3co/tco/opportunity_cost.main"></a>

#### main

```python
def main()
```

Runs the opportunity cost module as a standalone code based on input vehicles and scenarios

