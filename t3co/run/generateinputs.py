import pandas as pd
import numpy as np
import ast
from pathlib import Path
from t3co.run import Global as gl


def generate(vocation, dst=gl.OPTIMIZATION_AND_TCO_RCRS):
    """
    This function aggregates specifications from users for powertrains, desired ranges, component costs etc. into two
    csv files - FASTSimInputs and OtherInputs

    Args:
        vocation (str): Vocation type description
        dst (str, optional): results directory file path. Defaults to gl.OPTIMIZATION_AND_TCO_RCRS.
    """

    print("generating inputs")

    vehiclesdir = "vehicles"
    srcdir = "resources"

    BaselineVehicle_path = (
        Path(__file__).parent
        / srcdir
        / vehiclesdir
        / vocation
        / "specifications/BaselineVehicle.csv"
    )
    OptimizerInitializationValues_path = (
        Path(__file__).parent
        / srcdir
        / vehiclesdir
        / vocation
        / "specifications/OptimizerInitializationValues.csv"
    )
    PowertrainTechTargets_path = (
        Path(__file__).parent
        / srcdir
        / vehiclesdir
        / vocation
        / "specifications/PowertrainTechTargets.csv"
    )
    VocationRequirements_path = (
        Path(__file__).parent
        / srcdir
        / vehiclesdir
        / vocation
        / "specifications/VocationRequirements.csv"
    )
    FastsimHeader_path = Path(__file__).parent / "resources" / "aux" / "FASTSimInputsHeader.csv"
    Other_Inputs_Header_path = (
        Path(__file__).parent / "resources" / "aux" / "OtherInputsHeader.csv"
    )

    BaselineVehicleSpec = pd.read_csv(BaselineVehicle_path)
    OptimizerInitializationValues = pd.read_csv(OptimizerInitializationValues_path)
    PowertrainTechTargets = pd.read_csv(PowertrainTechTargets_path)
    VocationRequirements = pd.read_csv(VocationRequirements_path)

    TechYears = BaselineVehicleSpec.loc[:, "Year"].values
    Nyears = len(TechYears)

    Ranges = np.array(ast.literal_eval(VocationRequirements.at[1, "MinRangeMiles"]))
    Nranges = len(Ranges)
    Npowertrains = max(PowertrainTechTargets["PowertrainNumber"].values)

    FASTSimInputsDf = pd.read_csv(FastsimHeader_path)
    OtherInputsDf = pd.read_csv(Other_Inputs_Header_path)

    OtherInputsDf["VMT"] = OtherInputsDf.VMT.astype(str)

    v = 0
    for pt in range(0, Npowertrains):
        for y in range(0, Nyears):
            for r in range(0, Nranges):
                # FASTSimInputsDf.at[v, "scenario_name"] = f"{v/3} {v}"
                FASTSimInputsDf.at[v, "selection"] = v + 1
                FASTSimInputsDf.at[v, "scenario_name"] = (
                    f"{PowertrainTechTargets[PowertrainTechTargets.PowertrainNumber > pt].iloc[0]['PowertrainName']} "
                    f"{BaselineVehicleSpec.at[y, 'Year']} tech, "
                    f" {Ranges[r]} mi range"
                )
                FASTSimInputsDf.at[v, "veh_pt_type"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "veh_pt_type",
                ].values[0]
                FASTSimInputsDf.at[v, "drag_coef"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "drag_coef",
                ]
                FASTSimInputsDf.at[v, "frontalAreaM2"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "frontalAreaM2",
                ]
                FASTSimInputsDf.at[v, "glider_kg"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "glider_kg",
                ]
                FASTSimInputsDf.at[v, "vehCgM"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "vehCgM",
                ]
                FASTSimInputsDf.at[v, "driveAxleWeightFrac"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "driveAxleWeightFrac",
                ]
                FASTSimInputsDf.at[v, "wheelBaseM"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "wheelBaseM",
                ]
                FASTSimInputsDf.at[v, "cargo_kg"] = VocationRequirements.loc[
                    y, "cargo_kg"
                ]
                FASTSimInputsDf.at[v, "vehOverrideKg"] = 0
                FASTSimInputsDf.at[v, "fs_max_kw"] = OptimizerInitializationValues.loc[
                    (OptimizerInitializationValues["PowertrainNumber"] == (pt + 1))
                    & (
                        OptimizerInitializationValues["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fs_max_kw",
                ].values[0]
                FASTSimInputsDf.at[
                    v, "fuelStorSecsToPeakPwr"
                ] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fuelStorSecsToPeakPwr",
                ].values[0]
                FASTSimInputsDf.at[v, "fs_kwh"] = OptimizerInitializationValues.loc[
                    (OptimizerInitializationValues["PowertrainNumber"] == (pt + 1))
                    & (
                        OptimizerInitializationValues["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fs_kwh",
                ].values[0]
                FASTSimInputsDf.at[v, "fs_kwhPerKg"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fs_kwhPerKg",
                ].values[0]
                FASTSimInputsDf.at[v, "fc_max_kw"] = OptimizerInitializationValues.loc[
                    (OptimizerInitializationValues["PowertrainNumber"] == (pt + 1))
                    & (
                        OptimizerInitializationValues["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fc_max_kw",
                ].values[0]
                FASTSimInputsDf.at[v, "fc_eff_type"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fc_eff_type",
                ].values[0]
                FASTSimInputsDf.at[v, "fcAbsEffImpr"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fcAbsEffImpr",
                ].values[0]
                FASTSimInputsDf.at[
                    v, "fuelConvSecsToPeakPwr"
                ] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fuelConvSecsToPeakPwr",
                ].values[0]
                FASTSimInputsDf.at[v, "fuelConvBaseKg"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fuelConvBaseKg",
                ].values[0]
                FASTSimInputsDf.at[v, "fuelConvKwPerKg"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fuelConvKwPerKg",
                ].values[0]
                FASTSimInputsDf.at[v, "mc_max_kw"] = OptimizerInitializationValues.loc[
                    (OptimizerInitializationValues["PowertrainNumber"] == (pt + 1))
                    & (
                        OptimizerInitializationValues["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "mc_max_kw",
                ].values[0]
                # FASTSimInputsDf.at[v, "motorPeakEff"] =                 PowertrainTechTargets.loc[(PowertrainTechTargets['PowertrainNumber'] == (pt+1)) & (PowertrainTechTargets['Year'] == BaselineVehicleSpec.at[y, 'Year']), 'motorPeakEff'].values[0]
                FASTSimInputsDf.at[v, "motorSecsToPeakPwr"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "motorSecsToPeakPwr",
                ].values[0]
                FASTSimInputsDf.at[v, "mcPeKgPerKw"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "mcPeKgPerKw",
                ].values[0]
                FASTSimInputsDf.at[v, "mcPeBaseKg"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "mcPeBaseKg",
                ].values[0]
                FASTSimInputsDf.at[v, "ess_max_kw"] = OptimizerInitializationValues.loc[
                    (OptimizerInitializationValues["PowertrainNumber"] == (pt + 1))
                    & (
                        OptimizerInitializationValues["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "ess_max_kw",
                ].values[0]
                FASTSimInputsDf.at[
                    v, "ess_max_kwh"
                ] = OptimizerInitializationValues.loc[
                    (OptimizerInitializationValues["PowertrainNumber"] == (pt + 1))
                    & (
                        OptimizerInitializationValues["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "ess_max_kwh",
                ].values[0]
                FASTSimInputsDf.at[v, "essKgPerKwh"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essKgPerKwh",
                ].values[0]
                FASTSimInputsDf.at[v, "essBaseKg"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essBaseKg",
                ].values[0]
                FASTSimInputsDf.at[v, "essRoundTripEff"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essRoundTripEff",
                ].values[0]
                FASTSimInputsDf.at[v, "essLifeCoefA"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essLifeCoefA",
                ].values[0]
                FASTSimInputsDf.at[v, "essLifeCoefB"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essLifeCoefB",
                ].values[0]
                FASTSimInputsDf.at[v, "wheelInertiaKgM2"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "wheelInertiaKgM2",
                ]
                FASTSimInputsDf.at[v, "numWheels"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "numWheels",
                ]
                FASTSimInputsDf.at[v, "wheelRrCoef"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "wheelRrCoef",
                ]
                FASTSimInputsDf.at[v, "wheelRadiusM"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "wheelRadiusM",
                ]
                FASTSimInputsDf.at[v, "wheelCoefOfFric"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "wheelCoefOfFric",
                ]
                FASTSimInputsDf.at[v, "min_soc"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "min_soc",
                ].values[0]
                FASTSimInputsDf.at[v, "max_soc"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "max_soc",
                ].values[0]
                FASTSimInputsDf.at[
                    v, "essDischgToFcMaxEffPerc"
                ] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essDischgToFcMaxEffPerc",
                ].values[0]
                FASTSimInputsDf.at[
                    v, "essChgToFcMaxEffPerc"
                ] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essChgToFcMaxEffPerc",
                ].values[0]
                FASTSimInputsDf.at[v, "maxAccelBufferMph"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "maxAccelBufferMph",
                ].values[0]
                FASTSimInputsDf.at[
                    v, "maxAccelBufferPercOfUseableSoc"
                ] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "maxAccelBufferPercOfUseableSoc",
                ].values[0]
                FASTSimInputsDf.at[v, "percHighAccBuf"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "percHighAccBuf",
                ].values[0]
                FASTSimInputsDf.at[v, "mphFcOn"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "mphFcOn",
                ].values[0]
                FASTSimInputsDf.at[v, "kwDemandFcOn"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "kwDemandFcOn",
                ].values[0]
                FASTSimInputsDf.at[v, "altEff"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "altEff",
                ].values[0]
                FASTSimInputsDf.at[v, "chgEff"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "chgEff",
                ].values[0]
                FASTSimInputsDf.at[v, "auxKw"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "auxKw",
                ]
                FASTSimInputsDf.at[v, "forceAuxOnFC"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "forceAuxOnFC",
                ].values[0]
                FASTSimInputsDf.at[v, "transKg"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "transKg",
                ]
                FASTSimInputsDf.at[v, "transEff"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "transEff",
                ]
                FASTSimInputsDf.at[v, "comp_mass_multiplier"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "comp_mass_multiplier",
                ]
                FASTSimInputsDf.at[v, "essToFuelOkError"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essToFuelOkError",
                ].values[0]
                FASTSimInputsDf.at[v, "maxRegen"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "maxRegen",
                ].values[0]
                FASTSimInputsDf.at[v, "minFcTimeOn"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "minFcTimeOn",
                ].values[0]
                FASTSimInputsDf.at[v, "idleFcKw"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "idleFcKw",
                ].values[0]
                FASTSimInputsDf.at[v, "fc_eff_map"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "engineMap",
                ].values[0]
                FASTSimInputsDf.at[v, "mcPwrOutPerc"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "mcPwrOutPerc",
                ].values[0]
                FASTSimInputsDf.at[v, "largeBaselineEff"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "largeBaselineEff",
                ].values[0]  # I'm not sure what this is
                FASTSimInputsDf.at[v, "smallBaselineEff"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "smallBaselineEff",
                ].values[0]  # I'm not sure what this is
                FASTSimInputsDf.at[v, "modernMax"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "modernMax",
                ].values[0]  # I'm not sure what this is
                FASTSimInputsDf.at[v, "stopStart"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "stopStart",
                ].values[0]  # I'm not sure what this is

                FASTSimInputsDf.at[v, "valUddsMpgge"] = 0
                FASTSimInputsDf.at[v, "valHwyMpgge"] = 0
                FASTSimInputsDf.at[v, "valCombMpgge"] = 0
                FASTSimInputsDf.at[v, "valUddsKwhPerMile"] = 0
                FASTSimInputsDf.at[v, "valHwyKwhPerMile"] = 0
                FASTSimInputsDf.at[v, "valCombKwhPerMile"] = 0
                FASTSimInputsDf.at[v, "valCdRangeMi"] = 0
                FASTSimInputsDf.at[v, "valConst65MphKwhPerMile"] = 0
                FASTSimInputsDf.at[v, "valConst60MphKwhPerMile"] = 0
                FASTSimInputsDf.at[v, "valConst55MphKwhPerMile"] = 0
                FASTSimInputsDf.at[v, "valConst45MphKwhPerMile"] = 0
                FASTSimInputsDf.at[v, "valUnadjUddsKwhPerMile"] = 0
                FASTSimInputsDf.at[v, "valUnadjHwyKwhPerMile"] = 0
                FASTSimInputsDf.at[v, "val0To60Mph"] = 0
                FASTSimInputsDf.at[v, "valEssLifeMiles"] = 0
                FASTSimInputsDf.at[v, "valRangeMiles"] = 0
                FASTSimInputsDf.at[v, "valVehBaseCost"] = 0
                FASTSimInputsDf.at[v, "valMsrp"] = 0

                # Values to send to OtherInputs file

                OtherInputsDf.at[v, "selection"] = v + 1
                OtherInputsDf.at[v, "VMT"] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "VMT",
                ].values[0]
                OtherInputsDf.at[v, "driveCycle"] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "rangeDriveCycleFilePath",
                ].values[0]
                OtherInputsDf.at[v, "segmentName"] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "segmentName",
                ].values[0]
                OtherInputsDf.at[v, "GVWRkg"] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "GVWRkg",
                ].values[0]
                OtherInputsDf.at[v, "GVWRCredit_kg"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "GVWRCredit_kg",
                ].values[0]
                OtherInputsDf.at[v, "fuel"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fuel",
                ].values[0]
                OtherInputsDf.at[v, "maintDolPerMi"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "maintDolPerMi",
                ].values[0]
                OtherInputsDf.at[v, "constTripDistMiles"] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "constTripDistMiles",
                ].values[0]
                OtherInputsDf.at[v, "vehLifeYears"] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "vehLifeYears",
                ].values[0]
                OtherInputsDf.at[
                    v, "desiredEssReplacements"
                ] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "desiredEssReplacements",
                ].values[0]
                OtherInputsDf.at[v, "discRate"] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "discRate",
                ]
                OtherInputsDf.at[v, "essDolPerKw"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essDolPerKw",
                ].values[0]
                OtherInputsDf.at[v, "essDolPerKwh"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essDolPerKwh",
                ].values[0]
                OtherInputsDf.at[v, "essPackageCost"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essPackageCost",
                ].values[0]
                OtherInputsDf.at[v, "essCostRedPerYear"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essCostRedPerYear",
                ].values[0]
                OtherInputsDf.at[v, "essSalvageVal"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "essSalvageVal",
                ].values[0]
                OtherInputsDf.at[v, "peAndMcDolPerKw"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "peAndMcDolPerKw",
                ].values[0]
                OtherInputsDf.at[v, "peAndMcBaseCost"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "peAndMcBaseCost",
                ].values[0]
                OtherInputsDf.at[v, "iceDolPerKw"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "iceDolPerKw",
                ].values[0]
                OtherInputsDf.at[v, "iceBaseCost"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "iceBaseCost",
                ].values[0]
                OtherInputsDf.at[v, "fuelCellDolPerKw"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fuelCellDolPerKw",
                ].values[0]
                OtherInputsDf.at[v, "fuelStorDolPerKwh"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fuelStorDolPerKwh",
                ].values[0]
                OtherInputsDf.at[v, "fuelStorH2DolPerKwh"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fuelStorH2DolPerKwh",
                ].values[0]
                OtherInputsDf.at[v, "plugCost"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "plugCost",
                ].values[0]
                OtherInputsDf.at[v, "markup"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "markup",
                ]
                OtherInputsDf.at[v, "cngIceDolPerKw"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "cngIceDolPerKw",
                ].values[0]
                OtherInputsDf.at[v, "fuelStorCngDolPerKwh"] = PowertrainTechTargets.loc[
                    (PowertrainTechTargets["PowertrainNumber"] == (pt + 1))
                    & (
                        PowertrainTechTargets["Year"]
                        == BaselineVehicleSpec.at[y, "Year"]
                    ),
                    "fuelStorCngDolPerKwh",
                ].values[0]
                OtherInputsDf.at[v, "vehGliderPrice"] = BaselineVehicleSpec.loc[
                    PowertrainTechTargets["Year"] == BaselineVehicleSpec.at[y, "Year"],
                    "vehGliderPrice",
                ]
                OtherInputsDf.at[v, "tax"] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "tax",
                ]
                OtherInputsDf.at[v, "vocation"] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "vocation",
                ].values[0]
                OtherInputsDf.at[v, "modelYear"] = BaselineVehicleSpec.at[y, "Year"]
                OtherInputsDf.at[v, "region"] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "region",
                ].values[0]
                OtherInputsDf.at[v, "TargetRangeMi"] = Ranges[r]
                OtherInputsDf.at[
                    v, "minSpeed6PercentGradeIn5min"
                ] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "minSpeed6PercentGradeIn5min",
                ].values[0]
                OtherInputsDf.at[
                    v, "minSpeed1point25PercentGradeIn5min"
                ] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "minSpeed1point25PercentGradeIn5min",
                ].values[0]
                OtherInputsDf.at[v, "max0to60secAtGVWR"] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "max0to60secAtGVWR",
                ].values[0]
                OtherInputsDf.at[v, "max0to30secAtGVWR"] = VocationRequirements.loc[
                    VocationRequirements["Year"] == VocationRequirements.at[y, "Year"],
                    "max0to30secAtGVWR",
                ].values[0]
                # OtherInputsDf.at[v, "Powertrain"] =                  PowertrainTechTargets.loc[(PowertrainTechTargets['PowertrainNumber'] == (pt+1)) & (PowertrainTechTargets['Year'] == BaselineVehicleSpec.at[y, 'Year']), 'PowertrainName'].values[0]

                v += 1

    FASTSimInputsDf.set_index(
        pd.Series(range(1, len(FASTSimInputsDf) + 1)), inplace=True
    )
    FASTSimInputsDf.to_csv(
        dst / gl.FASTSIM_INPUTS_FILE, index=False
    )  # ####Make this into a results folder

    OtherInputsDf.set_index(pd.Series(range(1, len(OtherInputsDf) + 1)), inplace=True)
    OtherInputsDf.to_csv(
        dst / gl.OTHER_INPUTS_FILE, index=False
    )  # ####Make this into a results folder
