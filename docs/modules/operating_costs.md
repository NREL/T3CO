# Table of Contents

* [t3co/cost\_models/operating\_costs](#t3co/cost_models/operating_costs)
  * [OperatingCosts](#t3co/cost_models/operating_costs.OperatingCosts)
    * [\_\_new\_\_](#t3co/cost_models/operating_costs.OperatingCosts.__new__)
    * [\_\_init\_\_](#t3co/cost_models/operating_costs.OperatingCosts.__init__)
    * [set\_fuel\_cost](#t3co/cost_models/operating_costs.OperatingCosts.set_fuel_cost)
    * [set\_maintenance\_oper\_cost](#t3co/cost_models/operating_costs.OperatingCosts.set_maintenance_oper_cost)
    * [set\_insurance\_cost](#t3co/cost_models/operating_costs.OperatingCosts.set_insurance_cost)
    * [set\_purchasing\_payment\_cost](#t3co/cost_models/operating_costs.OperatingCosts.set_purchasing_payment_cost)
    * [set\_fueling\_dwell\_labor\_cost](#t3co/cost_models/operating_costs.OperatingCosts.set_fueling_dwell_labor_cost)
    * [set\_net\_oper\_cost](#t3co/cost_models/operating_costs.OperatingCosts.set_net_oper_cost)
    * [set\_disc\_oper\_cost](#t3co/cost_models/operating_costs.OperatingCosts.set_disc_oper_cost)
    * [\_\_str\_\_](#t3co/cost_models/operating_costs.OperatingCosts.__str__)

<a id="t3co/cost_models/operating_costs"></a>

# t3co/cost\_models/operating\_costs

<a id="t3co/cost_models/operating_costs.OperatingCosts"></a>

## OperatingCosts Objects

```python
class OperatingCosts()
```

<a id="t3co/cost_models/operating_costs.OperatingCosts.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the OperatingCosts class.

<a id="t3co/cost_models/operating_costs.OperatingCosts.__init__"></a>

#### \_\_init\_\_

```python
def __init__(year_number: int,
             cap_costs: CapitalCosts,
             vehicle: Vehicle,
             scenario: Scenario,
             energy: Energy = None,
             oppy_costs: OpportunityCosts = None)
```

Initializes the OperatingCosts instance.

**Arguments**:

- `year_number` _int_ - The year number for which the operating costs are calculated.
- `cap_costs` _CapitalCosts_ - The capital costs associated with the vehicle.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.
- `energy` _Energy_ - The energy model instance.
- `oppy_costs` _OpportunityCosts_ - The opportunity costs associated with the vehicle.

<a id="t3co/cost_models/operating_costs.OperatingCosts.set_fuel_cost"></a>

#### set\_fuel\_cost

```python
def set_fuel_cost(year_number: int, vehicle: Vehicle,
                  scenario: Scenario) -> None
```

Sets the fuel cost for the given year.

This method calculates the fuel cost based on the fuel price and the amount of fuel used.
The calculation uses the following OperatingCosts elements:
- distance_traveled_mi_per_yr
- mpgge

Inputs from scenario:
- fuel_prices_df
- fuel_type
- model_year
- region

Estimated class variables:
- fuel_price_dol_per_gge
- fuel_used_gal_gge_per_yr
- fuel_used_gal_gde_per_yr
- energy_used_kwh_per_yr
- fuel_cost_dol_per_yr

**Arguments**:

- `year_number` _int_ - The year number for which the fuel cost is calculated.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co/cost_models/operating_costs.OperatingCosts.set_maintenance_oper_cost"></a>

#### set\_maintenance\_oper\_cost

```python
def set_maintenance_oper_cost(year_number: int, vehicle: Vehicle,
                              scenario: Scenario) -> None
```

Sets the maintenance operating cost for the given year.

This method calculates the maintenance cost based on the maintenance cost per mile and the distance traveled.

Inputs from scenario:
- maint_oper_cost_dol_per_mi
- vmt

Estimated class variables:
- maintenance_cost_dol_per_mi
- maintenance_cost_dol_per_yr

**Arguments**:

- `year_number` _int_ - The year number for which the maintenance cost is calculated.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co/cost_models/operating_costs.OperatingCosts.set_insurance_cost"></a>

#### set\_insurance\_cost

```python
def set_insurance_cost(year_number: int, cap_cost: CapitalCosts,
                       vehicle: Vehicle, scenario: Scenario) -> None
```

Sets the insurance cost for the given year.

This method calculates the insurance cost based on the insurance rate and the total value of the vehicle.

Inputs from scenario:
- insurance_rates_pct_per_yr

Inputs from cap_cost:
- msrp_total_dol

Estimated class variables:
- insurance_cost_dol_per_yr

**Arguments**:

- `year_number` _int_ - The year number for which the insurance cost is calculated.
- `cap_cost` _CapitalCosts_ - The capital costs associated with the vehicle.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co/cost_models/operating_costs.OperatingCosts.set_purchasing_payment_cost"></a>

#### set\_purchasing\_payment\_cost

```python
def set_purchasing_payment_cost(year_number: int, scenario: Scenario,
                                cap_costs: CapitalCosts)
```

Sets the purchasing payment cost for the given year.

This method calculates the purchasing payment cost based on the purchasing method specified in the scenario.

Inputs from scenario:
- purchasing_method
- purchasing_interest_apr_pct_per_yr
- purchasing_payment_frequency_months
- purchasing_term_yr
- tax_rate_pct
- leasing_money_factor

Inputs from cap_costs:
- purchasing_initial_principal_dol
- msrp_total_dol
- purchase_tax_dol
- purchasing_downpayment_dol
- residual_cost_dol

Estimated OperatingCosts variables:
- purchasing_payment_dol_per_yr
- purchasing_cost_dol_per_yr
- purchasing_remaining_principal_dol
- purchasing_tax_amount_dol_per_year

**Arguments**:

- `year_number` _int_ - The year number for which the purchasing payment cost is calculated.
- `scenario` _Scenario_ - The scenario instance containing configuration data, including the purchasing method, interest rate, and term.
- `cap_costs` _CapitalCosts_ - The capital costs associated with the vehicle.

<a id="t3co/cost_models/operating_costs.OperatingCosts.set_fueling_dwell_labor_cost"></a>

#### set\_fueling\_dwell\_labor\_cost

```python
def set_fueling_dwell_labor_cost(scenario: Scenario,
                                 oppy_costs: OpportunityCosts) -> None
```

Sets the fueling dwell labor cost for the given year.

This method calculates the fueling dwell labor cost based on the fueling dwell time and the labor rate.

Inputs from scenario:
- labor_rate_dol_per_hr

Inputs from oppy_costs:
- fueling_dwell_time_hr_per_yr

Estimated OperatingCosts variables:
- fueling_dwell_labor_cost_dol_per_yr

**Arguments**:

- `scenario` _Scenario_ - The scenario instance containing configuration data.
- `oppy_costs` _OpportunityCosts_ - The opportunity costs associated with the vehicle.

<a id="t3co/cost_models/operating_costs.OperatingCosts.set_net_oper_cost"></a>

#### set\_net\_oper\_cost

```python
def set_net_oper_cost() -> None
```

Sets the net operating cost for the given year.

This method calculates the net operating cost by summing the various operating cost components.
The calculation uses the following OperatingCosts elements:
- fuel_cost_dol_per_yr
- fueling_dwell_labor_cost_dol_per_yr
- maintenance_cost_dol_per_yr
- insurance_cost_dol_per_yr
- purchasing_payment_dol_per_yr

Estimated OperatingCosts variables:
- net_oper_cost_dol_per_yr

<a id="t3co/cost_models/operating_costs.OperatingCosts.set_disc_oper_cost"></a>

#### set\_disc\_oper\_cost

```python
def set_disc_oper_cost(year_number: int, scenario: Scenario) -> None
```

Sets the discounted operating cost for the given year.

This method calculates the discounted operating cost based on the net operating cost and the discount rate.
The calculation uses the following OperatingCosts elements:
- net_oper_cost_dol_per_yr

Inputs from scenario:
- discount_rate_pct_per_yr

Estimated OperatingCosts variables:
- disc_oper_cost_dol_per_yr

**Arguments**:

- `year_number` _int_ - The year number for which the discounted operating cost is calculated.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co/cost_models/operating_costs.OperatingCosts.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns a string representation of the OperatingCosts instance.

**Returns**:

- `str` - String representation of the OperatingCosts instance.

