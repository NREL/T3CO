import pytest
from t3co.cost_models.opportunity_costs import OpportunityCosts
from t3co.energy_models.energy import Energy
from t3co.input_data.toggles import Toggles
from t3co.input_data.vehicle import Vehicle
from t3co.input_data.scenario import Scenario
import pandas as pd


@pytest.fixture
def vehicle():
    vehicle = Vehicle(
        veh_pt_type="BEV",
        fc_max_kw=100.0,
        fs_kwh=50.0,
        mc_max_kw=200.0,
        ess_max_kwh=75.0,
        chg_eff=0.9,
        veh_override_kg=10000.0,
        cargo_kg=5000.0,
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
    return Scenario(
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
        vehicle_class="class8",
        vehicle_life_yr=10,
        discount_rate_pct_per_yr=0.05,
        fuel_prices_file="fuel_prices.csv",
        insurance_rates_pct_per_yr="[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]",
        maint_oper_cost_dol_per_mi=[0.1] * 10,
        vmt=[10000] * 10,
        fuel_type="electricity",
        model_year=2020,
        region="US",
        fuel_prices_df=pd.DataFrame(
            {
                "Fuel": ["electricity"],
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
        plf_ref_veh_empty_mass_kg=8000.0,
        gvwr_kg=15000.0,
        gvwr_credit_kg=1000.0,
        activate_tco_payload_cap_cost_multiplier=True,
        activate_tco_fueling_dwell_time_cost=True,
        activate_mr_downtime_cost=True,
        fdt_dwpt_fraction_power_pct=0.1,
        fdt_frac_full_charge_bounds=[0.2, 0.8],
        fdt_avg_overhead_hr_per_dwell_hr=0.5,
        ess_max_charging_power_kw=100.0,
        downtime_oppy_cost_dol_per_hr=50.0,
        shifts_per_year=[250] * 10,
        constant_trip_distance_mi=100.0,
        fdt_num_free_dwell_trips=0,
        fdt_available_freetime_hr=0,
        mr_planned_downtime_hr_per_yr=10.0,
        mr_unplanned_downtime_hr_per_mi=[0.01] * 10,
        mr_avg_tire_life_mi=50000.0,
        mr_tire_replace_downtime_hr_per_event=2.0,
        cost_toggles=toggles
    )


@pytest.fixture
def energy():
    return Energy(mpgge=3.0, primary_fuel_range_mi=300.0)


def test_opportunity_costs_initialization(vehicle, scenario, energy):
    opportunity_costs = OpportunityCosts(
        year_number=1, vehicle=vehicle, scenario=scenario, energy=energy
    )
    assert opportunity_costs.payload_cap_cost_multiplier == pytest.approx(1.0, 0.01)
    assert opportunity_costs.fueling_dwell_time_hr_per_yr == pytest.approx(35.25, 0.01)
    assert opportunity_costs.mr_planned_downtime_hr == pytest.approx(10.0, 0.01)
    assert opportunity_costs.mr_unplanned_downtime_hr == pytest.approx(100.0, 0.01)
    assert opportunity_costs.mr_tire_replacement_downtime_hr == pytest.approx(0.4, 0.01)
    assert opportunity_costs.mr_downtime_hr_per_yr == pytest.approx(110.4, 0.01)
    assert opportunity_costs.net_downtime_hr_per_yr == pytest.approx(145.65, 0.01)
    assert opportunity_costs.fueling_downtime_oppy_cost_dol_per_yr == pytest.approx(
        1762.5, 0.01
    )
    assert opportunity_costs.mr_downtime_oppy_cost_dol_per_yr == pytest.approx(
        5520.0, 0.01
    )
    assert opportunity_costs.net_downtime_oppy_cost_dol_per_yr == pytest.approx(
        7282.5, 0.01
    )
    assert opportunity_costs.disc_downtime_oppy_cost_dol == pytest.approx(6935.71, 0.01)


def test_set_payload_cap_cost_multiplier(vehicle, scenario):
    opportunity_costs = OpportunityCosts.__new__(
        OpportunityCosts, year_number=1, vehicle=vehicle, scenario=scenario, energy=None
    )
    opportunity_costs.set_payload_cap_cost_multiplier(
        vehicle=vehicle, scenario=scenario
    )
    assert opportunity_costs.payload_cap_cost_multiplier == pytest.approx(1.0, 0.01)


def test_set_fueling_dwell_time_cost(vehicle, scenario, energy):
    opportunity_costs = OpportunityCosts.__new__(
        OpportunityCosts,
        year_number=1,
        vehicle=vehicle,
        scenario=scenario,
        energy=energy,
    )
    opportunity_costs.set_fueling_dwell_time_cost(
        year_number=1, vehicle=vehicle, scenario=scenario, energy=energy
    )
    assert opportunity_costs.fueling_dwell_time_hr_per_yr == pytest.approx(35.25, 0.01)
    assert opportunity_costs.fueling_downtime_oppy_cost_dol_per_yr == pytest.approx(
        1762.5, 0.01
    )


def test_set_mr_downtime_cost(vehicle, scenario):
    opportunity_costs = OpportunityCosts.__new__(
        OpportunityCosts, year_number=1, vehicle=vehicle, scenario=scenario, energy=None
    )
    opportunity_costs.set_mr_downtime_cost(
        year_number=1, vehicle=vehicle, scenario=scenario
    )
    assert opportunity_costs.mr_planned_downtime_hr == pytest.approx(10.0, 0.01)
    assert opportunity_costs.mr_unplanned_downtime_hr == pytest.approx(100.0, 0.01)
    assert opportunity_costs.mr_tire_replacement_downtime_hr == pytest.approx(0.4, 0.01)
    assert opportunity_costs.mr_downtime_hr_per_yr == pytest.approx(110.4, 0.01)
    assert opportunity_costs.mr_downtime_oppy_cost_dol_per_yr == pytest.approx(
        5520.0, 0.01
    )


def test_set_net_downtime_oppy_cost(vehicle, scenario, energy):
    opportunity_costs = OpportunityCosts(
        year_number=1, vehicle=vehicle, scenario=scenario, energy=energy
    )
    opportunity_costs.set_net_downtime_oppy_cost()
    assert opportunity_costs.net_downtime_oppy_cost_dol_per_yr == pytest.approx(
        7282.5, 0.01
    )
    assert opportunity_costs.net_downtime_hr_per_yr == pytest.approx(145.65, 0.01)


def test_set_disc_downtime_oppy_cost(vehicle, scenario, energy):
    opportunity_costs = OpportunityCosts(
        year_number=1, vehicle=vehicle, scenario=scenario, energy=energy
    )
    opportunity_costs.set_disc_downtime_oppy_cost(year_number=1, scenario=scenario)
    assert opportunity_costs.disc_downtime_oppy_cost_dol == pytest.approx(6935.71, 0.01)
