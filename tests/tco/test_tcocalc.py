import pandas as pd
import pytest
from t3co.input_data.toggles import Toggles
from t3co.tco.tcocalc import TCOCalc
from t3co.cost_models.capital_costs import CapitalCosts
from t3co.cost_models.operating_costs import OperatingCosts
from t3co.cost_models.opportunity_costs import OpportunityCosts
from t3co.energy_models.energy import Energy
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle


@pytest.fixture
def vehicle():
    vehicle = Vehicle(
        veh_pt_type="BEV",
        fc_max_kw=100.0,
        fs_kwh=50.0,
        mc_max_kw=200.0,
        ess_max_kwh=75.0,
        chg_eff=0.9,
        veh_override_kg=70000.0,
    )
    vehicle.set_veh_kg()
    return vehicle

@pytest.fixture
def toggles():
    return Toggles(
        msrp=True,
        purchase_tax=True,
        purchasing_downpayment=True,
        mark_up=True,
        residual_cost=True,
        fuel_cost=True,
        maintenance_oper_cost=True,
        insurance_cost=True,
        purchasing_cost=True,
        fueling_dwell_labor=True,
        payload_oppy_cost=True,
        fueling_dwell_oppy_cost=True,
        mr_downtime_oppy_cost=True,
        run_fastsim=False,
    )

@pytest.fixture
def scenario(toggles):
    scenario = Scenario(
        # drive_cycle="path/to/drive_cycle.csv",
        vehicle_glider_cost_dol=10000.0,
        fc_fuelcell_cost_dol_per_kw=200.0,
        fc_ice_cost_dol_per_kw=150.0,
        fc_cng_ice_cost_dol_per_kw=180.0,
        fc_ice_base_cost_dol=5000.0,
        fs_h2_cost_dol_per_kwh=10.0,
        fs_cng_cost_dol_per_kwh=8.0,
        fs_cost_dol_per_kwh=6.0,
        pe_mc_base_cost_dol=3000.0,
        pe_mc_cost_dol_per_kw=50.0,
        plug_base_cost_dol=1000.0,
        ess_base_cost_dol=5000.0,
        ess_cost_dol_per_kwh=200.0,
        markup_pct=0.1,
        tax_rate_pct=0.08,
        constant_trip_distance_mi=100.0,
        vmt=[10000] * 10,
        model_year=2020,
        region="US",
        fuel_type="electricity",
        activate_tco_payload_cap_cost_multiplier=True,
        plf_ref_veh_empty_mass_kg=8000.0,
        activate_tco_fueling_dwell_time_cost=True,
        activate_mr_downtime_cost=True,
        fdt_dwpt_fraction_power_pct=0.1,
        fdt_frac_full_charge_bounds="[0.2, 0.8]",
        fdt_avg_overhead_hr_per_dwell_hr=0.5,
        downtime_oppy_cost_dol_per_hr=50.0,
        shifts_per_year=[250] * 10,
        fdt_num_free_dwell_trips=0,
        fdt_available_freetime_hr=0,
        mr_planned_downtime_hr_per_yr=10.0,
        mr_unplanned_downtime_hr_per_mi=[0.01] * 10,
        mr_avg_tire_life_mi=50000.0,
        mr_tire_replace_downtime_hr_per_event=2.0,
        vehicle_life_yr=10,
        ess_max_charging_power_kw=100.0,
        discount_rate_pct_per_yr=0.05,
        avg_speed_mph=50.0,
        vehicle_class="class8",
        depreciation_rates_pct_per_yr=[0.09] * 10,
        insurance_rates_pct_per_yr=[0.01] * 10,
        maint_oper_cost_dol_per_mi=[0.05] * 10,
        fuel_prices_df=pd.DataFrame(
            {
                "Fuel": ["dolPerKwh"],
                "Region": ["US"],
                "2020": [0.1],
                "2021": [0.1],
                "2022": [0.1],
                "2023": [0.1],
                "2024": [0.1],
                "2025": [0.1],
                "2026": [0.1],
                "2027": [0.1],
                "2028": [0.1],
                "2029": [0.1],
            }
        ),
        cost_toggles=toggles
    )
    scenario.fuel_prices_df.set_index("Fuel", inplace=True)
    return scenario


@pytest.fixture
def energy():
    return Energy(mpgge=3.0, primary_fuel_range_mi=300.0)


@pytest.fixture
def cap_costs(vehicle, scenario):
    return CapitalCosts(vehicle=vehicle, scenario=scenario)


@pytest.fixture
def oper_costs(vehicle, scenario, energy, cap_costs):
    return OperatingCosts(
        year_number=1,
        cap_costs=cap_costs,
        vehicle=vehicle,
        scenario=scenario,
        energy=energy,
        oppy_costs=None,
    )


@pytest.fixture
def oppy_costs(vehicle, scenario, energy):
    return OpportunityCosts(
        year_number=1, vehicle=vehicle, scenario=scenario, energy=energy
    )


def test_tcocalc_initialization(
    vehicle, scenario, energy, cap_costs, oper_costs, oppy_costs
):
    tcocalc = TCOCalc(
        year_index=0,
        vehicle=vehicle,
        scenario=scenario,
        energy=energy,
        cap_costs=cap_costs,
    )

    assert tcocalc.year_number == 1
    assert tcocalc.cap_costs_dol == cap_costs
    assert tcocalc.oper_costs_dol.net_oper_cost_dol_per_yr == pytest.approx(
        12207.33, 0.01
    )
    assert tcocalc.oppy_costs_dol.net_downtime_oppy_cost_dol_per_yr == pytest.approx(
        7282.5, 0.01
    )
    assert tcocalc.total_cost_dol_per_yr == pytest.approx(71771.83, 0.01)
    assert tcocalc.disc_total_cost_dol_per_yr == pytest.approx(70843.26, 0.01)


def test_calculate_capital_costs(vehicle, scenario):
    tcocalc = TCOCalc.__new__(
        TCOCalc, year_index=0, vehicle=vehicle, scenario=scenario, energy=None
    )
    tcocalc.year_number = 0 + 1
    tcocalc.calculate_capital_costs(vehicle=vehicle, scenario=scenario)
    assert tcocalc.cap_costs_dol.glider_cost_dol == pytest.approx(11000.0, 0.01)


def test_calculate_opportunity_costs(vehicle, scenario, energy):
    tcocalc = TCOCalc.__new__(
        TCOCalc, year_index=0, vehicle=vehicle, scenario=scenario, energy=energy
    )
    tcocalc.year_number = 0 + 1
    tcocalc.calculate_opportunity_costs(
        vehicle=vehicle, scenario=scenario, energy=energy
    )
    assert tcocalc.oppy_costs_dol.net_downtime_oppy_cost_dol_per_yr == pytest.approx(
        7282.5, 0.01
    )


def test_calculate_operating_costs(vehicle, scenario, energy, cap_costs):
    tcocalc = TCOCalc.__new__(
        TCOCalc,
        year_index=0,
        vehicle=vehicle,
        scenario=scenario,
        energy=energy,
        cap_costs=cap_costs,
    )
    tcocalc.cap_costs_dol = cap_costs
    tcocalc.year_number = 0 + 1
    tcocalc.calculate_operating_costs(vehicle=vehicle, scenario=scenario, energy=energy)
    assert tcocalc.oper_costs_dol.net_oper_cost_dol_per_yr == pytest.approx(
        12207.33, 0.01
    )


def test_set_total_cost(vehicle, scenario, energy, cap_costs, oper_costs, oppy_costs):
    tcocalc = TCOCalc(
        year_index=0,
        vehicle=vehicle,
        scenario=scenario,
        energy=energy,
        cap_costs=cap_costs,
    )
    tcocalc.oper_costs_dol = oper_costs
    tcocalc.oppy_costs_dol = oppy_costs
    tcocalc.set_total_cost(scenario=scenario)
    assert tcocalc.total_cost_dol_per_yr == pytest.approx(71771.83, 0.01)


def test_set_disc_total_cost(
    vehicle, scenario, energy, cap_costs, oper_costs, oppy_costs
):
    tcocalc = TCOCalc(
        year_index=0,
        vehicle=vehicle,
        scenario=scenario,
        energy=energy,
        cap_costs=cap_costs,
    )
    tcocalc.oper_costs_dol = oper_costs
    tcocalc.oppy_costs_dol = oppy_costs
    tcocalc.set_disc_total_cost(vehicle=vehicle, scenario=scenario)
    assert tcocalc.disc_total_cost_dol_per_yr == pytest.approx(70843.26, 0.01)
