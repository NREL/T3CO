import setuptools
from pathlib import Path
from typing import List
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_install_requires() -> List[str]:
    """Returns requirements.txt parsed to a list"""
    fname = Path(os.path.abspath(__file__)).parents[0] / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

setuptools.setup(
    name="t3co",
    version="1.0.0",
    author="NREL",
    author_email="t3co@nrel.gov",
    description="Tool for modeling and optimizing Total Cost of Ownership of commercial vehicles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NREL/T3CO",  

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",  # update if needed
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "t3co.resources": ["*"],
    },
    install_requires= get_install_requires(),
)
