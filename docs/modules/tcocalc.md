# Table of Contents

* [t3co/tco/tcocalc](#t3co/tco/tcocalc)
  * [TCOCalc](#t3co/tco/tcocalc.TCOCalc)
    * [\_\_new\_\_](#t3co/tco/tcocalc.TCOCalc.__new__)
    * [\_\_init\_\_](#t3co/tco/tcocalc.TCOCalc.__init__)
    * [calculate\_capital\_costs](#t3co/tco/tcocalc.TCOCalc.calculate_capital_costs)
    * [calculate\_opportunity\_costs](#t3co/tco/tcocalc.TCOCalc.calculate_opportunity_costs)
    * [calculate\_operating\_costs](#t3co/tco/tcocalc.TCOCalc.calculate_operating_costs)
    * [set\_total\_cost](#t3co/tco/tcocalc.TCOCalc.set_total_cost)
    * [set\_disc\_total\_cost](#t3co/tco/tcocalc.TCOCalc.set_disc_total_cost)
    * [\_\_str\_\_](#t3co/tco/tcocalc.TCOCalc.__str__)

<a id="t3co/tco/tcocalc"></a>

# t3co/tco/tcocalc

<a id="t3co/tco/tcocalc.TCOCalc"></a>

## TCOCalc Objects

```python
class TCOCalc()
```

<a id="t3co/tco/tcocalc.TCOCalc.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the TCOCalc class.

<a id="t3co/tco/tcocalc.TCOCalc.__init__"></a>

#### \_\_init\_\_

```python
def __init__(year_index: int,
             vehicle: Vehicle,
             scenario: Scenario,
             energy: Energy,
             payload_cap_cost_multiplier: float = None,
             cap_costs: CapitalCosts = None)
```

Initializes the TCOCalc instance.

**Arguments**:

- `year_index` _int_ - The year index.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance.
- `energy` _Energy_ - The energy instance.
- `payload_cap_cost_multiplier` _float, optional_ - Payload capacity cost multiplier. Defaults to None.
- `cap_costs` _CapitalCosts, optional_ - Capital costs instance. Defaults to None.

<a id="t3co/tco/tcocalc.TCOCalc.calculate_capital_costs"></a>

#### calculate\_capital\_costs

```python
def calculate_capital_costs(vehicle: Vehicle, scenario: Scenario) -> None
```

Calculates the capital costs.

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance.

<a id="t3co/tco/tcocalc.TCOCalc.calculate_opportunity_costs"></a>

#### calculate\_opportunity\_costs

```python
def calculate_opportunity_costs(vehicle: Vehicle, scenario: Scenario,
                                energy: Energy) -> None
```

Calculates the opportunity costs.

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance.
- `energy` _Energy_ - The energy instance.

<a id="t3co/tco/tcocalc.TCOCalc.calculate_operating_costs"></a>

#### calculate\_operating\_costs

```python
def calculate_operating_costs(vehicle: Vehicle, scenario: Scenario,
                              energy: Energy) -> None
```

Calculates the operating costs.

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance.
- `energy` _Energy_ - The energy instance.

<a id="t3co/tco/tcocalc.TCOCalc.set_total_cost"></a>

#### set\_total\_cost

```python
def set_total_cost(scenario: Scenario) -> None
```

Sets the total cost for the year.

**Arguments**:

- `scenario` _Scenario_ - The scenario instance.

<a id="t3co/tco/tcocalc.TCOCalc.set_disc_total_cost"></a>

#### set\_disc\_total\_cost

```python
def set_disc_total_cost(vehicle: Vehicle,
                        scenario: Scenario,
                        payload_cap_cost_multiplier: float = None,
                        TCO_switch="DIRECT") -> None
```

Sets the discounted total cost for the year.

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance.
- `payload_cap_cost_multiplier` _float, optional_ - Payload capacity cost multiplier. Defaults to None.
- `TCO_switch` _str, optional_ - TCO calculation method. Defaults to "DIRECT".

<a id="t3co/tco/tcocalc.TCOCalc.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns a string representation of the TCOCalc instance.

**Returns**:

- `str` - String representation of the TCOCalc instance.

