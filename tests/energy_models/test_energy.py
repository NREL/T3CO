import pytest

from t3co.energy_models.energy import Energy


def test_energy_initialization():
    energy = Energy(mpgge=3.0, primary_fuel_range_mi=300.0)
    assert energy.mpgge == pytest.approx(3.0, 0.01)
    assert energy.primary_fuel_range_mi == pytest.approx(300.0, 0.01)


def test_energy_initialization_default():
    energy = Energy()
    assert energy.mpgge is None
    assert energy.primary_fuel_range_mi is None


def test_energy_initialization_partial():
    energy = Energy(mpgge=3.0)
    assert energy.mpgge is None
    assert energy.primary_fuel_range_mi is None

    energy = Energy(primary_fuel_range_mi=300.0)
    assert energy.mpgge is None
    assert energy.primary_fuel_range_mi is None

from unittest.mock import patch

def test_run_fastsim_model_missing_dependency():
    energy = Energy()
    scenario = "dummy_scenario"
    
    with patch("t3co.energy_models.energy.RunFASTSim", None):
        with pytest.raises(ImportError, match="FASTSim is not installed"):
            energy.run_fastsim_model(veh_no=1, scenario=scenario)
