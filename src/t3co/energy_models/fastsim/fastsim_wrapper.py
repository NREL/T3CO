import ast
from pathlib import Path
import fastsim
from fastsim.simdrive import SimDrive
import numpy as np

from t3co.input_data.config import Config
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle
from t3co.constants import Global as gl

class RunFastsim():
    vehicle: fastsim.vehicle.Vehicle
    cycle: fastsim.cycle.Cycle
    simdrive: fastsim.simdrive.SimDrive

    def __init__(self, vehicle: Vehicle, scenario: Scenario) -> None:
        self.load_vehicle()
        cyc = self.load_design_cycle_from_scenario(scenario)

        if isinstance(self.cycle, list):
            scenario.constant_trip_distance_mi = sum(
                [
                    sum(cyc[i][0].mph * np.diff(np.array(cyc[i][0].time_s), append=0))
                    * cyc[i][1]
                    / 3600
                    for i in range(len(cyc))
                ]
            )
        else:
            scenario.constant_trip_distance_mi = (
                sum(cyc.mph * np.diff(np.array(cyc.time_s), append=0)) / 3600
            )

    def load_vehicle(self, veh_no: int, veh_input_path: str) -> fastsim.vehicle.Vehicle:
        """
        This function loads vehicle object from vehicle number and input csv filepath

        Args:
            veh_no (int): vehicle selection number
            veh_input_path (str): vehicle model assumptions input CSV file path

        Returns:
            veh (fastsim.vehicle.Vehicle): FASTSim vehicle object
        """

        scenario_sel = int(float(str(veh_no).split("_")[0]))
        self.vehicle = fastsim.vehicle.Vehicle.from_vehdb(scenario_sel, veh_input_path, to_rust=True)
        self.vehicle.set_derived()
        self.vehicle.set_veh_mass()

    def load_design_cycle_from_scenario(
        self,
        scenario: Scenario,
        config: Config = None,
        cyc_file_path: str = gl.OPTIMIZATION_DRIVE_CYCLES,
        do_input_validation: bool = False,
    ) -> fastsim.cycle.Cycle:
        """
        This helper method loads the design cycle used for mpgge and range determination.
        It can also be used standalone to get cycles not in standard gl.OPTIMIZATION_DRIVE_CYCLES location,
        but still needs cycle name from scenario object, carried in scenario.drive_cycle.
        If the drive cycles are a list of tuples, handle accordingly with eval.

        Args:
            scenario (Scenario): Scenario object for current selection
            cyc_file_path (str, optional): drivecycle input file path. Defaults to gl.OPTIMIZATION_DRIVE_CYCLES.

        Returns:
            range_cyc (fastsim.cycle.Cycle): FASTSim cycle object for current Scenario object
        """

        if config.dc_files != None and not do_input_validation:
            dc_id = int(float(str(scenario.selection).split("_")[1]))
            sdc = str(config.dc_files[dc_id])
        else:
            sdc = str(scenario.drive_cycle)
        print(f"Drivecycle: {sdc}")
        if "[" in sdc and "]" in sdc and "(" in sdc and ")" in sdc:
            scenario.drive_cycle = ast.literal_eval(sdc)
            range_cyc = []
            for dc_weight in scenario.drive_cycle:
                cycle_file_name = Path(dc_weight[0]).name
                self.load_design_cycle_from_path(
                    cyc_file_path=Path(cyc_file_path) / dc_weight[0]
                )
                self.cycle.name = cycle_file_name
                weight = dc_weight[1]
                range_cyc.append((self.cycle, weight))
            return range_cyc
        else:
            cycle_file_name = Path(sdc).name
            self.load_design_cycle_from_path(cyc_file_path=sdc)
            self.cycle.name = cycle_file_name
            return None

    def load_design_cycle_from_path(self, cyc_file_path: str):
        """
        This helper method loads the Cycle object from the drivecycle filepath

        Args:
            cyc_file_path (str): drivecycle input file path

        Returns:
            range_cyc (fastsim.cycle.Cycle): FASTSim cycle object for current Scenario object
        """
        if Path(cyc_file_path).exists() == False:
            print(
                f"Drive cycle not found in {cyc_file_path}, trying {gl.OPTIMIZATION_DRIVE_CYCLES}"
            )
            finalized_path = Path(gl.OPTIMIZATION_DRIVE_CYCLES) / cyc_file_path

        else:
            finalized_path = cyc_file_path

        self.cycle = fastsim.cycle.Cycle.from_file(finalized_path)
        self.cycle = self.cycle.to_rust()


