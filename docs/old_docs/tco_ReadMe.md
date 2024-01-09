# ReadMe for Stock Model Framework

## Overview
- Please visit http://nrel.github.io/sera/ for detailed documentation on the SERA model (Stock Module will be of most interest to you)
- The SERA model was developed since the late 2000s, primarily funded for FCTO projects (most have GitHub repos that can be found here: https://github.nrel.gov/SERA)
- The model is primarily used for H2 infrastructure (LDV station placement over time, hydrogen supply chain optimization (production plant siting, trucks/pipeline placement and flows) across the US)
- The Stock Model is a general stock model framework analogous to the ANL VISION model but with the capability of much more spatial and temporal fidelity (and without the fudge factors)
- The SERA Stock Model algorithm is fairly general and the user has a lot of responsibility to create, validate, and use the correct, data-heavy input files (this allows the same algorithm to be very flexibly used - an attribute I spoke with Jason about)

## SERA Executable
- The actual SERA model is written in Haskell and is compiled into an executable file that one can run on Linux, Windows, and Mac machines
- Location of latest exe version is on Eagle at: /projects/sera/old-versions/sera-3.3.1.9
- Some aspects of the SERA model are currently being moved to the language Julia which has the potential to be much faster and more people understand the language

## SERA in Python
- I (Chad) have replicated some of the SERA stock model functionality in Python to improve computation speed (using the Pandas package)
- The Python version of the stock module has been validated to match the Haskell version
- There are a number of ways to make the code faster and even more robust which will be useful if it is going to be used for additional products

## Examples / This Folder
- I have included some example input files and the Python version of SERA's stock model in this folder
- We can discuss in more detail when I am back in the office, but feel free to browse the files to understand the structure and format

## More Documentation
- For more information, please see the FCTO Market Segmentation report on the y-drive [here](Y:\5400\ADV_VEH_INFRA\Infrastructure_Systems\1.0 H2_Analysis_DOE\6.3.5 MKT Segmentation FCEV Focus\Report materials)
- Additionally, much of the TCO analysis for that project was done in R. Most files are [here](https://github.nrel.gov/SERA/market-segmentation)