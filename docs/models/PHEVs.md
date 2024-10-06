# Plug-in Hybrid Electric Vehicle Considerations

Given that PHEVs follow along the same TCO and optimizaton path as other powertrains, but with some wrinkles attributable only to PHEVs, we've listed those considerations here separately to ensure PHEVs are documented clearly and distinctly where needed. 

## Contents

- [Plug-in Hybrid Electric Vehicle Considerations](#plug-in-hybrid-electric-vehicle-considerations)
	- [Contents](#contents)
	- [PHEV Fuel Economy CD/CS ](#phev-fuel-econ)
	- [PHEV Fuel Costs and Utility Factor ](#phev-fuel-costs)
	- [PHEV Acceleration \& Grade Tests ](#phev-accel-grade)
	- [PHEV Optimization ](#phev-optimization)
	- [PHEV Special Inputs ](#phev-special-inputs)
	- [PHEVs Not Doing What You Want?](#phev-issues)

## PHEV Fuel Economy CD/CS <a name="phev-fuel-econ"></a>

Plug in hybrid electric vehicles are presumed to operate in two distinct modes. The first – charge depleting (CD) - is a predominantly electrically powered regime, which is desirable to predominate the overall operational model of a vehicle due to its lower emissions per mile of operation. It is also presumed that due to a lower cost of charging electricity it would be an economically preferred mode of operation for a fleet operator or a light duty vehicle owner. As daily driving varies between vehicles, this mode of operation may be designed to cover majority of a fleet or personal driving. For longer operating routes or extensive driving, those vehicles are capable to operate safely after their initial “charge depleting” mode of operation is depleted. Once a state of battery charge reaches its “minimum” operating window for charge depleting mode, the vehicle’s controls would shift the vehicle power generation to predominantly come from the engine – which would switch the vehicle into a charge sustaining mode of operation (CS).  

One of T3CO’s objectives is that the model is flexible and generalized to allow wide variety of powertrain and drive cycle simulations. In some instances, drive cycles may experience highly dynamic  operation early in their simulated cycle followed by steadier operation in a different part of the cycle. Due to the cycle’s non-homogeneous operation, it desirable to assess the typical vehicle performance throughout a cycle while the vehicle is in either a CS or CD mode. In assessing an entire cycle in both CS and CD modes, the model thus assures that typical operation of a vehicle would be represented in designing the vehicle powertrain even when the design cycle is completely disparate in kinetic intensity between its start and end. Any cycle characteristics which may benefit or deter CS mode of operation early in the drive cycle would be simulated. Also, CD operation would be assessed with operation of the vehicle late in the simulated drive cycle. Below is a description of how to enable T3CO to produce a full evaluation of a drive cycle in both its CD and CS modes and provide optimizer (MOO) and model output parameters to allow powertrain and energy storage sizing for range.


## PHEV Fuel Costs and Utility Factor <a name="phev-fuel-costs"></a>

Fuel costs for PHEVs depend on a concept called the **Utility Factor**. The utility in question is when the PHEV operates in a Charge Depleting (CD) fashion, and the factor is the fraction of operational time in which the vehicle can do this. The ideal would be that the PHEV operates in CD at all times, as this maximizes miles running on electricity, and thus maximizes energy efficiency and minimizes fuel costs. This would correspond to a utility factor of 1.

The user can prescribe the utility factor as a constant value, using the **T3CO** input `phev_utility_factor_override`, otherwise, the UF will be computed for the user.

The **Utility Factor** is computed here: https://github.com/NREL/T3CO/blob/661d2cb308f66041df693ad27fab050f512d6298/t3co/run_scenario.py#L238
using the concept of shift range [miles], as: 
      
        shift_range_mi = vehicle miles travelled in year one / shifts_per_year
        phev_utility_factor_computed = round(min(shift_range_mi, cd_range_mi) / shift_range_mi, 3)  
        uf = scenario.phev_utility_factor_computed

`cd_range_mi` is computed here: https://github.com/NREL/T3CO/blob/661d2cb308f66041df693ad27fab050f512d6298/t3co/objectives/fueleconomy.py#L41

as described in the docs in **fuel_efficiency_and_range.md**

The Utility Factor essentially weights the three fuel economy metrics that go into TCO, computed for PHEVs: 
|code variable||
|--|--|
|cs_fuel_mpgge| Charge Sustaining miles per gallon of gasoline equivalent from ICE fuel stores only|
|cd_fuel_mpgge| Charge Depleting miles per gallon of gasoline equivalent from ICE fuel stores only|
|cd_grid_electric_mpgge| Charge Depleting grid adjusted (charger efficiency) miles per gallon of gasoline equivalent from PHEV battery pack only |

The code fills out fuel usage in GGE based on the utility factor adjusted mpgges for the CD and CS modes and computes a resulting fuel cost for each vehicle operational year:

        data = [
            [vehicle_segment, fuels[0], vocation, uf ],     # cd_electricity
            [vehicle_segment, fuels[1], vocation, uf ],     # cd_diesel
            [vehicle_segment, fuels[2], vocation, 1 - uf ]  # cs_diesel
        ]
	
![image](https://github.nrel.gov/storage/user/1225/files/c931067f-5c19-4ac4-b88c-a8dbec15ddd4)

![image](https://github.nrel.gov/storage/user/1225/files/58007fca-6cc6-4fcb-b1a7-111030beac85)


## PHEV Acceleration & Grade Tests <a name="phev-accel-grade"></a>

**PHEVs** have a special input for determining intial SOC during the acceleration test: `soc_norm_init_for_accel_pct`.
Similarly, **PHEVs** have a special input for determining intial SOC during the grade test: `soc_norm_init_for_grade_pct`. This is used to determine the normalized percentage of available SOC within the vehicle's minimum and maximum SOC range. The formula is:
	
	ess_init_soc_for_test = vehicle.min_soc + (scenario.soc_norm_init_for_test * (vehicle.max_soc - vehicle.min_soc) )

There are other inputs from the **T3CO** scenario file that can override initial SOC behavior. `ess_init_soc_grade` and `ess_init_soc_accel`. As of now, it is treated as an error for a user to provide these along with values for `soc_norm_init_for_grade_pct` and `soc_norm_init_for_accel_pct` as it is ambiguous as to which initial SOC is supposed to be used. These general initial SOC overrides should be supplied only for HEVs and BEVs. The *default* behavior, what the code does for inital SOC for tests in the absense of any input for `ess_init_soc_grade/accel`, or `ess_init_soc_for_grade/accel`, is a mix of **FASTSim's** default behaviors and some overrides that **T3CO** configures. This is described in **acceleration_and_grade_tests.md**

applied at: https://github.com/NREL/T3CO/blob/47d92dadef3451f403275159888811e01057416d/t3co/run_scenario.py#L539

**Note**
It is worth noting that initial SOC inputs for grade and acceleration of PHEVs do not seem to matter much *unless* the battery is small enough in size (kWh) as to make it possible that the vehicle can naturally deplete its usable SOC range before the test is over.

	ess kwh size 4.0
	max motor kw 163.0
	max fc kw 100.0
	init soc:  0.05 max speed at 6% grade achvd 36.333
	init soc:  0.15 max speed at 6% grade achvd 36.349
	init soc:  0.25 max speed at 6% grade achvd 36.49
	init soc:  0.35 max speed at 6% grade achvd 36.724
	init soc:  0.45 max speed at 6% grade achvd 37.102
	init soc:  0.55 max speed at 6% grade achvd 37.704
	init soc:  0.65 max speed at 6% grade achvd 38.652
	init soc:  0.75 max speed at 6% grade achvd 40.123
	init soc:  0.85 max speed at 6% grade achvd 42.363
	init soc:  0.95 max speed at 6% grade achvd 45.69

	ess kwh size 150.0
	max motor kw 163.0
	max fc kw 100.0
	init soc:  0.05 max speed at 6% grade achvd 34.849
	init soc:  0.15 max speed at 6% grade achvd 67.793
	init soc:  0.25 max speed at 6% grade achvd 67.793
	init soc:  0.35 max speed at 6% grade achvd 67.793
	init soc:  0.45 max speed at 6% grade achvd 67.793
	init soc:  0.55 max speed at 6% grade achvd 67.793
	init soc:  0.65 max speed at 6% grade achvd 67.793
	init soc:  0.75 max speed at 6% grade achvd 67.793
	init soc:  0.85 max speed at 6% grade achvd 67.793
	init soc:  0.95 max speed at 6% grade achvd 67.793

## PHEV Optimization <a name="phev-optimization"></a>

PHEV optimization uses an optional, special input called `motor_power_override_kw_fc_demand_on_pct`. This is the percentage of motor power value set to the vehicle field `kw_fc_demand_on` to allow `kw_fc_demand_on` to increase or decrease proportionally with changes in `mc_max_kw` from the optimizer. This is described in more detail in the opimization docs.

## PHEV Special Inputs <a name="phev-special-inputs"></a>

|**PHEV** scenario file inputs| description | required/optional | default | range |
|--|--|--|--|--|
|phev_utility_factor_override| prescribed utility factor, code will no longer compute it |optional | if not supplied, will be -1 and UF will be computed by T3CO | [0,1] |
|shifts_per_year| Get the PHEV utility factor derived from the computed range of the vehicle and the operational day range computed from shifts per year and the first vmt year |required | *Suggested value*: 250 (weekdays/yr, assuming 1 shift/day) | [1,inf] |
|soc_norm_init_for_grade_pct| **Strictly PHEV only, will throw error for other types** For grade test, determines the normalized percentage of available SOC within the vehicle's minimum and maximum SOC range |optional | if not supplied, will be -1, FASTSim sets PHEV init SOC as max_soc | [0,1] |
|soc_norm_init_for_accel_pct| **Strictly PHEV only, will throw error for other types** For accel test, determines the normalized percentage of available SOC within the vehicle's minimum and maximum SOC range |optional | if not supplied, will be -1, FASTSim sets PHEV init SOC as max_soc | [0,1] |
|motor_power_override_kw_fc_demand_on_pct| The percentage of motor power value set to the vehicle field `kw_fc_demand_on` to allow `kw_fc_demand_on` to increase or decrease proportionally with changes in `mc_max_kw` from the optimizer. |optional | *suggested value*: .85. If not supplied, will be -1 and `vehicle.kw_fc_demand_on defaults` to vehicle file input | (0,1] |


## PHEVs Not Doing What You Want? <a name="phev-issues"></a>

PHEVs can be difficult to work with and configure in order to get the desired results. Sometimes you want to manipulate the vehicle into operating paradigms for research purposes, such as using motor more favorably than engine, or vice versa. There are a few hybrid powertrain controls in **FASTSim Vehicle** models that users should be aware of:
- **kw_demand_fc_on** the kw demand on the transmission from the drive cycle, a threshold at which the fuel converter (engine) must be turned on the contribute to meeting powertrain demand 
- **mc_sec_to_peak_pwr** seconds to motor reaching peak power, should be tied to a physically realistic value
- **min_fc_time_on** minimum time in seconds the engine must be on if the engine is turned on to meet demand
- **new powertrain input/variable** 

Other considerations: Currently, if the engine is turned on at all, **FASTSim** tries to use the engine close to or at its max power (kw) level in order to approach the theoretical max efficiency of the engine. This is done without regard to how much engine power on top of motor power is actually needed in order to meet drive cycle demand.
	
	



