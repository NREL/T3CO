# Overview

## T3CO Introduction <a name="t3co-introduction"></a>

[NREL's Transportation Technology Total Cost of Ownership](https://www.nrel.gov/transportation/t3co.html) (T3CO) tool enables levelized assessments of the full life cycle costs of current and advanced technology commercial vehicles.

## Code Flow <a name="code-flow"></a>

Generally speaking, T3CO can be used in two ways:

- The first option generates total cost of ownership (TCO) and performance metrics for a pre-defined vehicle.

- The second option optimizes a vehicle's component specifications to achieve the lowest total cost of ownership possible while meeting performance objectives. Since optimization requires gathering TCO and performance metrics during each step of optimization, it essentially is an expansion of the first option for using T3CO.

## Generating TCO and performance <a name="generating-tco-and-performance"></a>

There are a few main components of a vehicle's total cost of ownership: MSRP (the cost of the vehicle at time of purchase), fuel costs (based on $ per gallon of gasoline equivalent for every operational year's fuel used, other operating costs maintenance [\$/mile\]), fueling dwell time labor [\$/hr], opportunity cost for payload loss and downtime, and resale value at end of ownership.

Fuel costs are computed after determining the vehicle energy efficiency (e.g. miles per gallon of fuel) and factoring in the annual miles driven and the fuel price for each year and region where the vehicle operates.
The performance metrics estimated for the vehicle are: miles of range, acceleration time, and gradeability.

More details on performance metrics are included below under [optimization flow](#optimization-flow). If the analysis does not include optimization, these metrics are simply reported in the results.


## T3CO Input Files <a name="t3co-input-files)"></a>

There are three main files that form the basis of T3CO TCO calculations and T3CO optimizations. The first is the **Vehicle File** which provides [vehicle model inputs](vehicle_inputs_descriptions.md) for FASTSim simulation. The second type of file is the T3CO input file, or **Scenario File**, which specifies the [cost assumption parameters](scenario_inputs_descriptions.md) for the TCO calculation. These include technology cost assumptions (e.g. $ per kilowatt for engine or motor size), operating conditions, (e.g. annual VMT and geographic region), financial inputs (e.g. operating years and discount rate), analysis option controls (e.g. whether to optimize the vehicle or not), and performance requirements if optimizing (e.g. range, grade and acceleration targets). The third file is the **Config File**, which provides an [easier way to manage analyses](config_inputs_descriptions.md) with minimal command line inputs, containing overrides for major scenario input parameters.

T3CO provides some example Vehicle and Scenario models to assist the user in getting started. There are demo versions of the [Vehicle file](https://github.com/NREL/T3CO/blob/main/t3co/resources/inputs/demo/Demo_FY22_vehicle_model_assumptions.csv) and [Scenario file](https://github.com/NREL/T3CO/blob/main/t3co/resources/inputs/demo/Demo_FY22_scenario_assumptions.csv) available in the `/t3co/resources/inputs/demo/` folder. The [Config file](https://github.com/NREL/T3CO/blob/main/t3co/resources/T3COConfig.csv) is available in the `/t3co/resources/` folder. They are also available in the demo_inputs folder if the [`install_t3co_demo_inputs`](installation.md#copying-t3co-demo-input-files) command is used to copy the required input files to your local directory.


## Optimization Flow <a name="optimization-flow"></a>

The TCO & [Performance metric targets](#performance-constraints) described below are the core of the optimization loop. T3CO has the capability to take vehicle specifications, such as engine size, motor size, battery size, coefficient of aerodynamic drag, vehicle weight, etc. and modify them in order to find the set of specifications that yields the lowest TCO while still meeting minimum performance requirements in acceleration, grade and range. Adjusting these vehicle specifications impacts the vehicle’s MSRP and also, by changing its energy consumption per mile, its operating costs. If including engine efficiency, aerodynamic drag, and light-weighting in the optimization, [additional input files](https://github.com/NREL/T3CO/tree/main/t3co/resources/auxiliary) are required to specify the cost of improving these features.

Optimization is handled in the [optimization module](moo.md), inheriting from the [PyMOO](https://pymoo.org/index.html) module.

## Performance Constraints <a name="performance-constraints"></a>

The user must specify targets for the following performance metrics to constrain the optimization

- **Gradeability** is the measure of the vehicle's max speed achieved at 1.25 and 6 percent grades, while the vehicle is operating at max allowable GVWR (including EV weight credit kilograms)

- **Acceleration** is the measure of the time in seconds the vehicle takes to reach 30 miles per hour and 60 miles per hour. This constraint can be specified at max allowable GVWR or calculated vehicle weight using input payload.

- **Range** is the computation of the vehicle's range in miles based on the computed fuel efficiency (MPGGE - miles per gallon gasoline equivalent) and vehicle fuel or energy storage; MPGGE is attained using a design cycle (cycle or cycles determined to be representative of vehicle operation). The design cycle can be a single drive cycle or a weighted composite of multiple drive cycles.