# Table of Contents

* [t3co/cost\_models/opportunity\_costs](#t3co/cost_models/opportunity_costs)
  * [OpportunityCosts](#t3co/cost_models/opportunity_costs.OpportunityCosts)
    * [\_\_new\_\_](#t3co/cost_models/opportunity_costs.OpportunityCosts.__new__)
    * [\_\_init\_\_](#t3co/cost_models/opportunity_costs.OpportunityCosts.__init__)
    * [set\_payload\_cap\_cost\_multiplier](#t3co/cost_models/opportunity_costs.OpportunityCosts.set_payload_cap_cost_multiplier)
    * [set\_fueling\_dwell\_time\_cost](#t3co/cost_models/opportunity_costs.OpportunityCosts.set_fueling_dwell_time_cost)
    * [set\_mr\_downtime\_cost](#t3co/cost_models/opportunity_costs.OpportunityCosts.set_mr_downtime_cost)
    * [set\_net\_downtime\_oppy\_cost](#t3co/cost_models/opportunity_costs.OpportunityCosts.set_net_downtime_oppy_cost)
    * [set\_disc\_downtime\_oppy\_cost](#t3co/cost_models/opportunity_costs.OpportunityCosts.set_disc_downtime_oppy_cost)
    * [\_\_str\_\_](#t3co/cost_models/opportunity_costs.OpportunityCosts.__str__)

<a id="t3co/cost_models/opportunity_costs"></a>

# t3co/cost\_models/opportunity\_costs

<a id="t3co/cost_models/opportunity_costs.OpportunityCosts"></a>

## OpportunityCosts Objects

```python
class OpportunityCosts()
```

<a id="t3co/cost_models/opportunity_costs.OpportunityCosts.__new__"></a>

#### \_\_new\_\_

```python
def __new__(cls, *args, **kwargs)
```

Creates a new instance of the OpportunityCosts class.

<a id="t3co/cost_models/opportunity_costs.OpportunityCosts.__init__"></a>

#### \_\_init\_\_

```python
def __init__(year_number: int, vehicle: Vehicle, scenario: Scenario,
             energy: Energy)
```

Initializes the OpportunityCosts instance.

**Arguments**:

- `year_number` _int_ - The year number for which the opportunity costs are calculated.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.
- `energy` _Energy_ - The energy model instance.

<a id="t3co/cost_models/opportunity_costs.OpportunityCosts.set_payload_cap_cost_multiplier"></a>

#### set\_payload\_cap\_cost\_multiplier

```python
def set_payload_cap_cost_multiplier(vehicle: Vehicle,
                                    scenario: Scenario) -> None
```

Sets the payload capacity cost multiplier for the vehicle.

This method calculates the payload capacity cost multiplier based on the vehicle's weight and the scenario's weight distribution.

Inputs from scenario:
- plf_weight_distribution_file
- plf_ref_veh_empty_mass_kg
- gvwr_kg
- gvwr_credit_kg

Inputs from vehicle:
- veh_kg
- cargo_kg

Estimated class variables:
- payload_cap_cost_multiplier

**Arguments**:

- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co/cost_models/opportunity_costs.OpportunityCosts.set_fueling_dwell_time_cost"></a>

#### set\_fueling\_dwell\_time\_cost

```python
def set_fueling_dwell_time_cost(year_number: int, vehicle: Vehicle,
                                scenario: Scenario, energy: Energy) -> None
```

Calculates the fueling dwell time cost for a vehicle based on fuel fill rate/charging power and shifts per year.

Inputs from scenario:
- fdt_frac_full_charge_bounds
- shifts_per_year
- constant_trip_distance_mi
- vmt
- fdt_dwpt_fraction_power_pct
- ess_max_charging_power_kw
- fs_fueling_rate_gasoline_gpm
- fs_fueling_rate_diesel_gpm
- fdt_num_free_dwell_trips
- fdt_avg_overhead_hr_per_dwell_hr
- fdt_available_freetime_hr
- downtime_oppy_cost_dol_per_hr

Inputs from vehicle:
- veh_pt_type
- ess_max_kwh
- fs_kwh

Inputs from energy:
- primary_fuel_range_mi

Estimated OpportunityCosts variables:
- fdt_frac_full_charge_bounds
- shifts_per_year
- fdt_full_dwell_hr
- trip_distance_mi
- fdt_num_of_dwells
- fueling_dwell_time_hr_per_yr
- fueling_downtime_oppy_cost_dol_per_yr

**Arguments**:

- `year_number` _int_ - The year number for which the fueling dwell time cost is calculated.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.
- `energy` _Energy_ - The energy model instance.

<a id="t3co/cost_models/opportunity_costs.OpportunityCosts.set_mr_downtime_cost"></a>

#### set\_mr\_downtime\_cost

```python
def set_mr_downtime_cost(year_number: int, vehicle: Vehicle,
                         scenario: Scenario) -> None
```

Calculates the Maintenance and Repair (M&R) downtime cost based on planned, unplanned, and tire replacement downtime inputs.

Inputs from scenario:
- mr_planned_downtime_hr_per_yr
- mr_unplanned_downtime_hr_per_mi
- vmt
- mr_avg_tire_life_mi
- mr_tire_replace_downtime_hr_per_event
- downtime_oppy_cost_dol_per_hr

Estimated OpportunityCosts variables:
- mr_planned_downtime_hr
- mr_unplanned_downtime_hr
- mr_tire_replacement_downtime_hr
- mr_downtime_hr_per_yr
- mr_downtime_oppy_cost_dol_per_yr

**Arguments**:

- `year_number` _int_ - The year number for which the M&R downtime cost is calculated.
- `vehicle` _Vehicle_ - The vehicle instance.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co/cost_models/opportunity_costs.OpportunityCosts.set_net_downtime_oppy_cost"></a>

#### set\_net\_downtime\_oppy\_cost

```python
def set_net_downtime_oppy_cost() -> None
```

Sets the net downtime opportunity cost for the vehicle.

This method calculates the net downtime opportunity cost by summing the fueling downtime and MR downtime opportunity costs.
The calculation uses the following OpportunityCosts elements:
- fueling_downtime_oppy_cost_dol_per_yr
- mr_downtime_oppy_cost_dol_per_yr
- fueling_dwell_time_hr_per_yr
- mr_downtime_hr_per_yr

Estimated OpportunityCosts variables:
- net_downtime_oppy_cost_dol_per_yr
- net_downtime_hr_per_yr

<a id="t3co/cost_models/opportunity_costs.OpportunityCosts.set_disc_downtime_oppy_cost"></a>

#### set\_disc\_downtime\_oppy\_cost

```python
def set_disc_downtime_oppy_cost(year_number: int, scenario: Scenario) -> None
```

Sets the discounted downtime opportunity cost for the given year.

Inputs from scenario:
- discount_rate_pct_per_yr

Estimated class variables:
- disc_downtime_oppy_cost_dol

**Arguments**:

- `year_number` _int_ - The year number for which the discounted downtime opportunity cost is calculated.
- `scenario` _Scenario_ - The scenario instance containing configuration data.

<a id="t3co/cost_models/opportunity_costs.OpportunityCosts.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Returns a string representation of the OpportunityCosts instance.

**Returns**:

- `str` - String representation of the OpportunityCosts instance.

