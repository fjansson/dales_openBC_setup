# dales_openBC_setup
This repository creates the boundary input for DALES simulations with open boundary conditions. Currently supports conversion from HARMONIE output only. COSMO and AUS2200 output conversions are work in progress

## scripts
Contains scripts to create input.

## simulations
Contains the different simulation setups.

# Installation

```
python -m venv openbc_env
. openbc_env/bin/activate
pip install cdsapi numpy xarray netcdf4 matplotlib numba "dask[complete]" progress  pyproj scipy f90nml
```