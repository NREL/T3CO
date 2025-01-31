# Table of Contents

* [t3co/cost\_models/capital\_costs](#t3co/cost_models/capital_costs)
  * [CapitalCosts](#t3co/cost_models/capital_costs.CapitalCosts)
    * [\_\_new\_\_](#t3co/cost_models/capital_costs.CapitalCosts.__new__)
    * [\_\_init\_\_](#t3co/cost_models/capital_costs.CapitalCosts.__init__)
    * [set\_glider\_cost](#t3co/cost_models/capital_costs.CapitalCosts.set_glider_cost)
    * [set\_fuel\_converter\_cost\_dol](#t3co/cost_models/capital_costs.CapitalCosts.set_fuel_converter_cost_dol)
    * [set\_fuel\_storage\_cost](#t3co/cost_models/capital_costs.CapitalCosts.set_fuel_storage_cost)
    * [set\_motor\_control\_power\_elecs\_cost](#t3co/cost_models/capital_costs.CapitalCosts.set_motor_control_power_elecs_cost)
    * [set\_plug\_cost](#t3co/cost_models/capital_costs.CapitalCosts.set_plug_cost)
    * [set\_battery\_cost](#t3co/cost_models/capital_costs.CapitalCosts.set_battery_cost)
    * [set\_msrp](#t3co/cost_models/capital_costs.CapitalCosts.set_msrp)
    * [set\_purchase\_tax](#t3co/cost_models/capital_costs.CapitalCosts.set_purchase_tax)
    * [set\_downpayment](#t3co/cost_models/capital_costs.CapitalCosts.set_downpayment)
    * [set\_residual\_cost](#t3co/cost_models/capital_costs.CapitalCosts.set_residual_cost)
    * [set\_net\_capital\_cost](#t3co/cost_models/capital_costs.CapitalCosts.set_net_capital_cost)
    * [set\_disc\_residual\_cost](#t3co/cost_models/capital_costs.CapitalCosts.set_disc_residual_cost)
    * [get\_marked\_up\_value](#t3co/cost_models/capital_costs.CapitalCosts.get_marked_up_value)

<a id="t3co/cost_models/capital_costs"></a>

# t3co/cost\_models/capital\_costs

<a id="t3co/cost_models/capital_costs.CapitalCosts"></a>

## CapitalCosts Objects

```python
class CapitalCosts()
```

<a id="t3co/cost_models/capital_costs.CapitalCosts.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the CapitalCosts class.

<a id="t3co/cost_models/capital_costs.CapitalCosts.__init__"></a>

#### \_\_init\_\_

```python
def __init__(vehicle: Vehicle,
             scenario: Scenario,
             msrp_total_dol: float = None)
```

Initializes the CapitalCosts instance.

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.
- `msrp_total_dol` _float, optional_ - MSRP in dollars as input

<a id="t3co/cost_models/capital_costs.CapitalCosts.set_glider_cost"></a>

#### set\_glider\_cost

```python
def set_glider_cost(scenario: Scenario) -> None
```

Sets the glider cost for the vehicle.

This method calculates the marked up glider cost based on the vehicle class and the base cost.

Inputs from scenario:
- vehicle_glider_cost_dol

Estimated class variables:
- glider_cost_dol

**Arguments**:

- `scenario` _Scenario_ - The scenario instance containing configuration data, including the base cost for the glider.

<a id="t3co/cost_models/capital_costs.CapitalCosts.set_fuel_converter_cost_dol"></a>

#### set\_fuel\_converter\_cost\_dol

```python
def set_fuel_converter_cost_dol(vehicle: Vehicle, scenario: Scenario) -> None
```

Sets the fuel converter cost for the vehicle.

This method calculates the marked up fuel converter cost based on the vehicle powertrain type and the cost per kW.

Inputs from vehicle:
- fc_max_kw

Inputs from scenario:
- fc_fuelcell_cost_dol_per_kw
- fc_ice_cost_dol_per_kw
- fc_cng_ice_cost_dol_per_kw
- fc_ice_base_cost_dol

Estimated class variables:
- fuel_converter_cost_dol

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data, including the cost per kW for the fuel converter.

<a id="t3co/cost_models/capital_costs.CapitalCosts.set_fuel_storage_cost"></a>

#### set\_fuel\_storage\_cost

```python
def set_fuel_storage_cost(vehicle: Vehicle, scenario: Scenario) -> None
```

Sets the fuel storage cost for the vehicle.

This method calculates the marked up fuel storage cost based on the vehicle powertrain type and the cost per kWh.

Inputs from vehicle:
- fs_kwh

Inputs from scenario:
- fs_h2_cost_dol_per_kwh
- fs_cng_cost_dol_per_kwh
- fs_cost_dol_per_kwh

Estimated class variables:
- fuel_storage_cost_dol

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data, including the cost per kWh for the fuel storage.

<a id="t3co/cost_models/capital_costs.CapitalCosts.set_motor_control_power_elecs_cost"></a>

#### set\_motor\_control\_power\_elecs\_cost

```python
def set_motor_control_power_elecs_cost(vehicle: Vehicle,
                                       scenario: Scenario) -> None
```

Sets the motor control and power electronics cost for the vehicle.

This method calculates the marked up motor control and power electronics cost based on the vehicle powertrain type and the cost per kW.

Inputs from vehicle:
- mc_max_kw

Inputs from scenario:
- pe_mc_base_cost_dol
- pe_mc_cost_dol_per_kw

Estimated class variables:
- motor_control_power_elecs_cost_dol

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data, including the cost per kW for the motor control and power electronics.

<a id="t3co/cost_models/capital_costs.CapitalCosts.set_plug_cost"></a>

#### set\_plug\_cost

```python
def set_plug_cost(vehicle: Vehicle, scenario: Scenario) -> None
```

Sets the plug cost for the vehicle.

This method calculates the marked up plug cost based on the base cost.

Inputs from scenario:
- plug_base_cost_dol

Estimated class variables:
- plug_cost_dol

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data, including the base cost for the plug.

<a id="t3co/cost_models/capital_costs.CapitalCosts.set_battery_cost"></a>

#### set\_battery\_cost

```python
def set_battery_cost(vehicle: Vehicle, scenario: Scenario) -> None
```

Sets the battery cost for the vehicle.

This method calculates the marked up battery cost based on the energy storage system (ESS) capacity and the cost per kWh.

Inputs from vehicle:
- ess_max_kwh

Inputs from scenario:
- ess_base_cost_dol
- ess_cost_dol_per_kwh

Estimated class variables:
- battery_cost_dol

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data, including the cost per kWh for the battery.

<a id="t3co/cost_models/capital_costs.CapitalCosts.set_msrp"></a>

#### set\_msrp

```python
def set_msrp() -> None
```

Calculates the total MSRP (Manufacturer's Suggested Retail Price) for the vehicle.

This method calculates the total MSRP by summing the costs of various components of the vehicle.
The calculation uses the following CapitalCosts elements:
- glider_cost_dol
- fuel_storage_cost_dol
- fuel_converter_cost_dol
- motor_control_power_elecs_cost_dol
- battery_cost_dol
- plug_cost_dol

Estimated class variables:
- msrp_total_dol

<a id="t3co/cost_models/capital_costs.CapitalCosts.set_purchase_tax"></a>

#### set\_purchase\_tax

```python
def set_purchase_tax(scenario: Scenario) -> None
```

Sets the purchase tax for the vehicle.

This method calculates the purchase tax based on the total MSRP (Manufacturer's Suggested Retail Price) of the vehicle components.
The calculations use the following CapitalCosts elements:
- msrp_total_dol

Inputs from scenario:
- tax_rate_pct

Estimated class variables:
- purchase_tax_dol

**Arguments**:

- `scenario` _Scenario_ - The scenario instance containing configuration data, including the tax rate.

<a id="t3co/cost_models/capital_costs.CapitalCosts.set_downpayment"></a>

#### set\_downpayment

```python
def set_downpayment(scenario: Scenario) -> None
```

Sets the downpayment and initial principal for the vehicle purchase.

This method calculates the downpayment and initial principal based on the purchasing method specified in the scenario.
The calculations use the following CapitalCosts elements:
- msrp_total_dol
- purchase_tax_dol

Inputs from scenario:
- purchasing_method
- purchasing_down_payment_pct
- purchasing_interest_apr_pct_per_yr

Estimated class variables:
- purchasing_downpayment_dol
- purchasing_initial_principal_dol

**Arguments**:

- `scenario` _Scenario_ - The scenario instance containing configuration data, including the purchasing method, down payment percentage, and interest rate.

<a id="t3co/cost_models/capital_costs.CapitalCosts.set_residual_cost"></a>

#### set\_residual\_cost

```python
def set_residual_cost(scenario: Scenario) -> None
```

Sets the residual cost for the vehicle.

This method calculates the residual cost based on the total MSRP (Manufacturer's Suggested Retail Price) of the vehicle components,
the depreciation rates per year, and the vehicle's life span. The residual cost is the remaining value of the vehicle after depreciation.
The calculation uses the following CapitalCosts elements:
- msrp_total_dol

Inputs from scenario:
- depreciation_rates_pct_per_yr
- vehicle_life_yr

Estimated scenario variables:
- residual_rate_pct

Estimated class variables:
- residual_cost_dol

**Arguments**:

- `scenario` _Scenario_ - The scenario instance containing configuration data, including depreciation rates and vehicle life span.

<a id="t3co/cost_models/capital_costs.CapitalCosts.set_net_capital_cost"></a>

#### set\_net\_capital\_cost

```python
def set_net_capital_cost() -> None
```

Sets the total capital cost for the vehicle.

This method calculates the total capital cost by summing the costs of various components and applying the purchase tax.
The calculation uses the following CapitalCosts elements:
- purchasing_downpayment_dol

Inputs from scenario:
- tax_rate_pct

Estimated class variables:
- net_capital_cost_dol

<a id="t3co/cost_models/capital_costs.CapitalCosts.set_disc_residual_cost"></a>

#### set\_disc\_residual\_cost

```python
def set_disc_residual_cost(scenario: Scenario) -> None
```

Sets the discounted residual cost for the vehicle.

**Arguments**:

- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co/cost_models/capital_costs.CapitalCosts.get_marked_up_value"></a>

#### get\_marked\_up\_value

```python
def get_marked_up_value(value: float, scenario: Scenario) -> float
```

Returns the marked up value.

**Arguments**:

- `value` _float_ - The value to mark up.
- `scenario` _Scenario_ - The scenario instance containing configuration data.
  

**Returns**:

- `float` - The marked up value.

