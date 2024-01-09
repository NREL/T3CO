## How to install Oxidized FASTSim for Oxidized T3CO in server environment (or local desktop)

As of now, running from source code in **UNIX-like** server environments is the only way to use Oxidzed T3CO until a tarball or wheel dist for **UNIX-like** is completed 

- `cd /srv/data/users/$USER/` # i.e. the path for where you should have your programs on the fleetdna server
- `conda create --name t3co-env`
- `conda activate t3co-env`

# Install rust (if needed)
- conda update rust
or
- export RUSTUP_HOME=/srv/data/users/ayip/.rustup
- export CARGO_HOME=/srv/data/users/ayip/.cargo
- curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install FASTSim 2.0.7 from the Github repo
- If FASTSim is already installed n your current environment, uninstall it: `pip uninstall fastsim`
- clone fastsim repo with git, `git clone https://github.com/NREL/fastsim.git`
- `cd fastsim`
- `git checkout rust-port` # switch to rust-port branch - may or may not be redundant with next step
- `git checkout 2.0.7` # switch to tagged version/commit 2.0.7
- (citing instructions to compile and test Rust under [DEVELOPERS](https://github.nrel.gov/MBAP/fastsim/blob/rust-port/fastsim/docs/README.md#developers))
  - do `pip install maturin`
  - `cd rust`
  - do `cargo test --release`
  - `cd fastsim-py`
  - do `maturin develop --release`
  - `cd ..` back up to root folder in `/fastsim`
  -  install the FASTSim 2.0.7 code base into your activated conda environment for T3CO with `pip install -e .` # you might have to do this a few times repeatedly, if you get the error message "resource temporarily unavailable" - maybe VPN/SSH related but it's unavoidable because we're on the server


# Test run Oxidized T3CO
- `cd run_scripts`
- `python sweep.py -dst_dir /srv/data/nfs/T3CO/users/$USER/t3co-test-delete-bevs -look_for "BEV" -skopt -skiv`
