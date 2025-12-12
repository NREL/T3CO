import pytest
from unittest.mock import MagicMock, patch, ANY
import numpy as np
from t3co.optimize.optimization import VehicleDesignOpt, run_optimization
import t3co.constants.Global as gl


@pytest.fixture
def mock_vehicle():
    vehicle = MagicMock()
    vehicle.veh_pt_type = gl.BEV
    vehicle.selection = 1
    return vehicle


@pytest.fixture
def mock_scenario():
    scenario = MagicMock()
    scenario.knob_min_ess_kwh = 10
    scenario.knob_max_ess_kwh = 100
    scenario.knob_min_motor_kw = 50
    scenario.knob_max_motor_kw = 200
    scenario.knob_min_fc_kw = 20
    scenario.knob_max_fc_kw = 150
    scenario.knob_min_fs_kwh = 30
    scenario.knob_max_fs_kwh = 300
    scenario.constraint_accel = False
    scenario.constraint_grade = False
    scenario.constraint_range = False
    return scenario


@pytest.fixture
def mock_config():
    config = MagicMock()
    return config


class TestVehicleDesignOpt:
    def test_init_bev(self, mock_vehicle, mock_scenario, mock_config):
        mock_vehicle.veh_pt_type = gl.BEV

        problem = VehicleDesignOpt(mock_vehicle, mock_scenario, mock_config)

        assert problem.n_var == 2
        assert np.array_equal(problem.xl, np.array([10, 50]))
        assert np.array_equal(problem.xu, np.array([100, 200]))

    def test_init_conv(self, mock_vehicle, mock_scenario, mock_config):
        mock_vehicle.veh_pt_type = gl.CONV

        problem = VehicleDesignOpt(mock_vehicle, mock_scenario, mock_config)

        assert problem.n_var == 2
        assert np.array_equal(problem.xl, np.array([20, 30]))
        assert np.array_equal(problem.xu, np.array([150, 300]))

    def test_evaluate_bev(self, mock_vehicle, mock_scenario, mock_config):
        mock_vehicle.veh_pt_type = gl.BEV
        problem = VehicleDesignOpt(mock_vehicle, mock_scenario, mock_config)

        x = np.array([50, 100])  # ess_kwh, motor_kw
        out = {}

        with (
            patch("t3co.optimize.optimization.Energy") as MockEnergy,
            patch("t3co.optimize.optimization.Ledger") as MockLedger,
        ):
            mock_energy_instance = MockEnergy.return_value
            mock_ledger_instance = MockLedger.return_value
            mock_ledger_instance.discounted_tco_dol = 50000

            problem._evaluate(x, out)

            assert mock_vehicle.ess_max_kwh == 50
            assert mock_vehicle.mc_max_kw == 100

            mock_energy_instance.run_fastsim_model.assert_called_once()
            MockLedger.assert_called_once()

            assert out["F"] == [50000]

    def test_evaluate_constraints(self, mock_vehicle, mock_scenario, mock_config):
        mock_vehicle.veh_pt_type = gl.BEV
        mock_scenario.constraint_accel = True
        mock_scenario.max_time_0_to_60mph_at_gvwr_s = 10
        mock_scenario.max_time_0_to_30mph_at_gvwr_s = 5

        problem = VehicleDesignOpt(mock_vehicle, mock_scenario, mock_config)

        x = np.array([50, 100])
        out = {}

        with (
            patch("t3co.optimize.optimization.Energy") as MockEnergy,
            patch("t3co.optimize.optimization.Ledger") as MockLedger,
        ):
            mock_energy_instance = MockEnergy.return_value
            mock_energy_instance.zero_to_sixty_loaded = 12  # Violation
            mock_energy_instance.zero_to_thirty_loaded = 4  # Pass

            mock_ledger_instance = MockLedger.return_value
            mock_ledger_instance.discounted_tco_dol = 50000

            problem._evaluate(x, out)

            assert "G" in out
            # G[0] = 12 - 10 = 2 > 0 (violation)
            # G[1] = 4 - 5 = -1 <= 0 (pass)
            assert out["G"][0] == 2
            assert out["G"][1] == -1


def test_run_optimization():
    with (
        patch("t3co.optimize.optimization.Config") as MockConfig,
        patch("t3co.optimize.optimization.Vehicle") as MockVehicle,
        patch("t3co.optimize.optimization.Scenario") as MockScenario,
        patch("t3co.optimize.optimization.Pool") as MockPool,
        patch("t3co.optimize.optimization.minimize") as mock_minimize,
        patch("t3co.optimize.optimization.VehicleDesignOpt") as MockProblem,
    ):
        mock_res = MagicMock()
        mock_res.X = [10, 20]
        mock_res.F = [1000]
        mock_minimize.return_value = mock_res

        mock_vehicle_instance = MockVehicle.return_value
        mock_vehicle_instance.from_config.return_value = mock_vehicle_instance
        mock_vehicle_instance.veh_pt_type = gl.BEV

        run_optimization(selection=1, parallel=True, n_processes=2)

        MockConfig.assert_called()
        MockVehicle.assert_called()
        MockScenario.assert_called()
        MockPool.assert_called_with(2)
        mock_minimize.assert_called()
