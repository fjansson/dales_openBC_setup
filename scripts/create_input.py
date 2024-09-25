#%% Load modules
import json
from GridDales import GridDales
from prep_harmonie import prep_harmonie
import prep_harmonie_WINS50
from initial_fields import initial_fields, initial_fields_fine
from boundary_fields import boundary_fields, boundary_fields_fine
from profiles import profiles
from surface_temperature import surface_temperature, surface_temperature_fine
from synthetic_turbulence import synthetic_turbulence
from gaussian_filter import gaussian_filter

#from lsm.create_dales_input import create_lsm_input    # older LSM input format
from lsm.spatial_transforms import proj4_rd, proj4_hm

# new LSM input compatible with DEPAC
from land_surface.create_dales_input import create_lsm_input_tno
#from land_surface.spatial_transforms import proj4_rd, proj4_hm  # identical to the one in lsm

from datetime import datetime
import sys
#%% Read input file
with open(sys.argv[1]) as f: input = json.load(f)
#%% Create input for outer simulation
if 'coarse' in input:
  input_coarse = input['coarse']
  input_coarse['author'] = input['author']
  #%% Create DALES grid
  grid = GridDales(input_coarse['grid'])
  #%% Transfor input data to rectilinear grid and to prognostic variables of DALES
  if(input_coarse['source'].lower() == 'harmonie'):
    data,transform = prep_harmonie(input_coarse,grid)
  elif(input_coarse['source'].lower() == 'harmonie_wins50'):
    data,transform = prep_harmonie_WINS50.prep_harmonie(input_coarse,grid)
  elif(input_coarse['source'].lower() == 'none'): # useful to test LSM alone
    pass
  else:
    print('unvalid source type')
    exit()
  #%% Apply spatial horizontal Gaussian filter to data
  if('filter' in input_coarse and input_coarse['source'].lower() != 'none'):
    data = gaussian_filter(data,input_coarse)

  if 'LSM' in input_coarse:
    x_sw, y_sw = proj4_hm(input_coarse['lon_sw'], input_coarse['lat_sw'], inverse=False)
    print(f'LSM {x_sw}, {y_sw}.')
    dx = input_coarse['grid']['xsize'] / input_coarse['grid']['itot']
    dy = input_coarse['grid']['ysize'] / input_coarse['grid']['jtot']
    start_date = datetime.fromisoformat(input_coarse['start'])

    lsm_kind = 'old'
    if 'lsm_kind' in input_coarse['LSM']:
      lsm_kind = input_coarse['LSM']['lsm_kind']

    if lsm_kind == 'TNO':
      create_lsm_input(x_sw, y_sw, input_coarse['grid']['itot'], input_coarse['grid']['jtot'], dx, dy,
                       input_coarse['nprocx'], input_coarse['nprocy'], start_date,
                       input_coarse['outpath'], input_coarse['LSM']['ERA5_path'], input_coarse['LSM']['spatial_data_path'],
                       input_coarse['iexpnr'])
      print('Finished creating LSM input (TNO flavor)')
    else:
      create_lsm_input(x_sw, y_sw, input_coarse['grid']['itot'], input_coarse['grid']['jtot'], dx, dy,
                       input_coarse['nprocx'], input_coarse['nprocy'], start_date,
                       input_coarse['outpath'], input_coarse['LSM']['ERA5_path'], input_coarse['LSM']['spatial_data_path'],
                       input_coarse['iexpnr'])
      print('Finished creating LSM input')

  #%% Advective time interpolation of input data (optional, to be implemented)
  
  #%% Create initial fields > initfields.inp.xxx.nc
  if(input_coarse['start']==input_coarse['time0']): # Not required for warmstarts
    initfields = initial_fields(input_coarse,grid,data,transform)
    print('finished initial fields')
    #%% Create profiles > prof.inp.xxx, lscale.inp.xxx scalar.inp.xxx
    profiles(input_coarse,grid,initfields,data)
    print('finished profiles')
  #%% Create boundary input > openboundaries.inp.xxx.nc
  openboundaries = boundary_fields(input_coarse,grid,data)
  print('finished boundary fields')
  #%% Create synthetic turbulence for boundary input (optional) > openboundaries.inp.xxx.nc
  if('synturb' in input_coarse): 
    synturb = synthetic_turbulence(input_coarse,grid,data,transform)
    print('finished synthetic turbulence')
  #%% Create heterogeneous and time dependend skin temperature > tskin.inp.xxx.nc (if ltskin==true)
  if('tskin' in input_coarse): 
    tskin = surface_temperature(input_coarse,grid,data,transform)
    print('finished surface temperature')

#%% Write data to input files
if('fine' in input):
  input_fine = input['fine']
  input_fine['author'] = input['author']
  #%% Create DALES grid
  grid = GridDales(input_fine['grid'])
  #%% Create initial fields > initfields.inp.xxx.nc
  if(input_fine['start']==input_fine['time0']): # Not required for warmstarts
    initfields_fine = initial_fields_fine(input_fine,grid)
    print('finished initial fields')
  #%% Create boundary input > openboundaries.inp.xxx.nc
  openboundaries_fine = boundary_fields_fine(input_fine,grid)
  print('finished boundary fields')
  #%% Create heterogeneous and time dependend skin temperature > tskin.inp.xxx.nc
  if('tskin' in input_fine):
    tskin_fine = surface_temperature_fine(input_fine,grid)
    print('finished surface temperature')
# %%
