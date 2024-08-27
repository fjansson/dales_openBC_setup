# Crops the HARMONIE data to the required time and spatial extends. 
# Transforms pressure coordinates into height levels.
# Transforms HARMONIE prognostic variables to DALES prognostic variables
import numpy as np
import xarray as xr
from pyproj import Transformer
import dask
from numba import jit
# Constants
# Simulation constants (modglobal)
p0   = 1e5          # Reference pressure
Rd   = 287.04       # Gas constant for dry air
Rv   = 461.5        # Gas constant for water vapor
cp   = 1004.        # Specific heat at constant pressure (dry air)
Lv   = 2.53e6       # Latent heat for vaporisation
grav = 9.81         # Gravitational constant
kappa= 0.4          # Von Karman constant
def prep_harmonie(input,grid):
  variables = ['ua','va','wa','ta','hus','clw','ps','tas','huss']
  if('synturb' in input): variables = variables+['tke','tauu','tauv','cb','hfss']
  data = []
  # Open data and crop data
  for var in variables:
    with xr.open_mfdataset(f"{input['inpath']}{var}_*.nc",chunks={"time": input['tchunk']}) as ds:
      # Get time epochs
      if(var==variables[0]):
        # Read transform information and transform lat/lon of southwest corner to harmonie x/y
        transform = Transform(ds['Lambert_Conformal'].attrs)
        x_sw,y_sw = transform.latlon_to_xy(input['lat_sw'],input['lon_sw'])
        # Round to 5 meters to avoid numerical error in coordinates
        x_sw = np.round(x_sw,0)
        y_sw = np.round(y_sw,0)
        time = ds['time'].values
      # Interpolate fluxes to same time
      if(var in ['tauu','tauv','hfss']):
        ds = ds.interp(time=time,assume_sorted=True,kwargs={'fill_value': 'extrapolate'}).chunk({'time':input['tchunk']})
      # Crop data to time and spatial range, using harmonie spatial resolution or filter as buffer
      dx = ds['x'][1].values-ds['x'][0].values
      dy = ds['y'][1].values-ds['y'][0].values
      if('filter' in input): # add some extra width for gaussian filtering
        buffer = 4*input['filter']['sigma']
      else:
        buffer = dx   
      data.append(ds[var].sel(time=slice(input['start'], input['end']),
                              x=slice(x_sw-buffer,x_sw+grid.xsize+buffer),
                              y=slice(y_sw-buffer,y_sw+grid.ysize+buffer)))
    # Set south west corner of DALES as origin
    data[-1] = data[-1].assign_coords({'x': data[-1]['x'].values-x_sw, 'y': data[-1]['y'].values-y_sw})
  # Merge into xarray dataset
  data = xr.merge(data,compat='override')
  # Change transform parameters to new DALES origin and update transform
  transform.parameters['false_easting'] = transform.parameters['false_easting']-x_sw
  transform.parameters['false_northing']= transform.parameters['false_northing']-y_sw
  proj4 = ''
  for param in transform.parameters['proj4'][1:].split('+'):
    line = '+'+param
    if 'x_0' in param: line = f"+x_0={transform.parameters['false_easting']} "
    if 'y_0' in param: line = f"+y_0={transform.parameters['false_northing']} "
    proj4 = proj4+line
  transform.parameters['proj4']=proj4.rstrip()
  transform = Transform(transform.parameters)
  # Calculate pressure levels
  coeff = np.loadtxt(f"{input['inpath']}H43_65lev.txt")
  a = xr.DataArray(coeff[:,1],dims=['lev'],coords=[coeff[:,0]])
  b = xr.DataArray(coeff[:,2],dims=['lev'],coords=[coeff[:,0]])
  ph = (a+b*data['ps']).transpose('time','lev','y','x')
  p = 0.5*(ph.assign_coords({'lev': ph['lev'].values-1})+ph)
  data = data.assign({'p': p})
  # Add missing surface fields to 3d fields
  variables = ['uas','vas','was','clws']
  if('synturb' in input): variables.append('tkes')
  data = data.assign({var:xr.zeros_like(data['ps']) for var in variables})
  if('synturb' in input):
    tauu = data['tauu']
    tauv = data['tauv']
    hfss = data['hfss']
    cb   = data['cb']
  # Concatenate surface and 3D fields
  variables = ['ua','va','wa','ta','hus','clw','p']
  if('synturb' in input): variables.append('tke')
  data = xr.merge(
    [xr.concat([data[var].assign_coords({'lev': data['lev']}),data[var+'s']
                .expand_dims({'lev':[data.sizes['lev']+1]},axis=1)],dim='lev')
                .chunk({'lev': data.sizes['lev']+1}) 
     for var in variables] )
  # Calculate 3D height levels
  rho = data['p']/(Rd*data['ta']*(1+(Rv/Rd-1)*(data['hus']+data['clw'])-Rv/Rd*data['clw']))
  rhoh= 0.5*(rho.assign_coords({'lev': rho['lev'].values-1})+rho)
  z   = [xr.zeros_like(data['p'].isel(lev=1,drop=True).rename('z3d'))]
  for k in np.arange(data.sizes['lev']-2,-1,-1): 
    z = [z[0]-(data['p'].isel(lev=k,drop=True)-data['p'].isel(lev=k+1,drop=True))/(rhoh.isel(lev=k,drop=True)*grav)] + z
  data = data.assign({'z3d': xr.concat(z,dim='lev').chunk({'lev': data.sizes['lev']+1}).transpose('time','lev','y','x')})
  # Get reference height levels (mean of height field first time step) and crop to grid.zsize
  z_int = data['z3d'].isel({'time':0},drop=True).sel(x=slice(0,grid.xsize),y=slice(0,grid.ysize)).mean(dim=['x','y'])[::-1].values
  z_int = z_int[:np.argwhere(z_int>grid.zsize)[0][0]+1]
  # Interpolate data to reference height levels
  data_intz = []
  its = 0
  new_shape = [data.sizes['time'],len(z_int),data.sizes['y'],data.sizes['x']]
  new_coords = {'time': data.coords['time'],
                'z': z_int,
                'y': data.coords['y'],
                'x': data.coords['x']}
  new_dims = ['time','z','y','x']
  variables = ['ua','va','wa','ta','p','hus','clw']
  if('synturb' in input): variables.append('tke')
  for var in variables:
    its = 0
    var_intz = []
    # Loop over time chunks (allows for parallel calculation in time index)
    for tchunk in data.chunks['time']:
      ite = its+tchunk
      data_slice = dask.delayed(load_data)(data[var],{'time': np.arange(its,ite)},drop=False)
      z_slice = dask.delayed(load_data)(data['z3d'],{'time': np.arange(its,ite)},drop=False)
      var_intz.append(dask.delayed(interp_z)(z_slice,data_slice,z_int))
      its = ite
    # Concatenate data along time chunks and convert back to xarray
    var_intz = dask.delayed(np.concatenate)(var_intz,axis=0)
    var_intz = xr.DataArray(dask.array.from_delayed(var_intz,new_shape,dtype=float),
                            dims=new_dims,
                            coords=new_coords,
                            name = var,
                            attrs = data[var].attrs).chunk({'time': input['tchunk']})
    data_intz.append(var_intz)
  # Store interpolated height data in a DataSet
  data = xr.merge(data_intz).assign({'lat': data['lat'],'lon': data['lon']})
  # Calculate qt
  data = data.assign({'qt': data['clw']+data['hus']})
  # Calculate base profiles and exnr function
  if(input['start']==input['time0']): # Calculate exnr function
    tas_exnr = data['ta'].isel({'time': 0, 'z': 0},drop=True).sel(x=slice(0,grid.xsize),y=slice(0,grid.ysize)).mean(dim=['x','y']).values
    ps_exnr  = data['p'].isel({'time': 0, 'z': 0},drop=True).sel(x=slice(0,grid.xsize),y=slice(0,grid.ysize)).mean(dim=['x','y']).values
    exnrs    = (ps_exnr/p0)**(Rd/cp)
    thls_exnr= tas_exnr/exnrs
    rhobf    = calcBaseprof(z_int,thls_exnr,ps_exnr,pref0=p0)
    p_exnr   = rhobf[1:]*Rd*data['ta'][0,1:].sel(x=slice(0,grid.xsize),y=slice(0,grid.ysize)).mean(dim=['x','y']).values*\
            ( 1+(Rv/Rd-1)*data['qt'][0,1:].sel(x=slice(0,grid.xsize),y=slice(0,grid.ysize)).mean(dim=['x','y']).values-\
              Rv/Rd*data['clw'][0,1:].sel(x=slice(0,grid.xsize),y=slice(0,grid.ysize)).mean(dim=['x','y']).values ) # Ideal gas law
    exnr     = (p_exnr/p0)**(Rd/cp)
  else: # Read exnr.inp.xxx
    f = open(input['exnr_file'],'r')
    line0 = f.readline()
    f.close()
    thls_exnr = float(line0.split(',')[1].split('thls = ')[-1])
    ps_exnr = float(line0.split(',')[2].split('ps = ')[-1])
    exnr = np.loadtxt(input['exnr_file'],skiprows=2)
    exnrs = exnr[0,1]
    exnr = exnr[1:,1]
  exnr     = xr.DataArray(np.concatenate([exnrs[None],exnr]),
                          dims = ['z'],
                          coords={'z': z_int},
                          name = 'exnr',
                          attrs = {'thls': thls_exnr, 'ps': ps_exnr})
  data     = data.assign({'exnr': exnr})
  # Calculate liquid potential temperature and total specific humidity
  thl      = data['ta']/exnr-Lv*data['clw']/(cp*exnr)
  data     = data.assign({'thl': thl})
  # Calculate turbulence parameters
  if('synturb' in input):
    # Calculate inversion height from maximum curvature and with cloud base as a backup
    zi_min= 200
    zi_max= 4000
    thlmean = thl.sel(x=slice(0,grid.xsize),y=slice(0,grid.ysize)).mean(dim=['x','y'])
    cbmean= xr.where(cb>0.,cb,np.NaN).sel(x=slice(0,grid.xsize),y=slice(0,grid.ysize)).mean(dim=['x','y'])
    its = 0 
    d2thl = []
    d1thl = []
    rhobf    = calcBaseprof(z_int,thls_exnr,ps_exnr,pref0=p0)
    for tchunk in thlmean.chunks[0]:
      ite = its+tchunk
      d1thl.append(dask.delayed(differentiate)(thlmean.isel({'time':np.arange(its,ite)}),'z',1,acc=6))
      d2thl.append(dask.delayed(differentiate)(thlmean.isel({'time':np.arange(its,ite)}),'z',2,acc=6))
      its = ite
    d1thl = dask.delayed(xr.concat)(d2thl,dim='time').compute()
    d2thl = dask.delayed(xr.concat)(d1thl,dim='time').compute()
    zi    = d2thl.where(d1thl>0).sel(z=slice(zi_min,zi_max)).idxmax('z').fillna(cbmean)
    rhobs = rhobf[0]-z_int[0]*(rhobf[1]-rhobf[0])/(z_int[1]-z_int[0])
    ustar = np.sqrt(np.maximum(tauu,0)/rhobs).rename('ustar')
    vstar = np.sqrt(np.maximum(tauv,0)/rhobs).rename('vstar')
    wthls = (hfss/(exnrs*rhobs*cp)).rename('wthls')
    data  = data.assign({'ustar': ustar, 'vstar': vstar, 'wthls': wthls, 'zi': zi})
  # Organize data, rename variables and drop non DALES prognostic variables
  data = data.rename({'ua': 'u', 'va': 'v', 'wa': 'w'})\
    .drop(['ta','p','clw','hus','height'])\
    .assign({'transform' : xr.DataArray([],name='Lambert_Conformal',attrs=transform.parameters)})
  #data.to_netcdf(f"{input['outpath']}harmonie.nc", mode='w', format="NETCDF4")
  return data,transform

class Transform:
  def __init__(self,parameters):
    self.parameters = parameters
    self.crs_latlon = 'epsg:4326'
    # Construct transformation objects
    self.latlon_to_xy_transform = Transformer.from_crs(self.crs_latlon,self.parameters['proj4'])
    self.xy_to_latlon_transform = Transformer.from_crs(self.parameters['proj4'],self.crs_latlon)

  def latlon_to_xy(self,lat,lon):
    return self.latlon_to_xy_transform.transform(lat,lon)

  def xy_to_latlon(self,x,y):
    return self.xy_to_latlon_transform.transform(x,y)

@jit(nopython=True, nogil=True)
def interp_z(z,data,z_int):
  data_int = np.zeros((np.shape(data)[0],len(z_int),np.shape(data)[2],np.shape(data)[3]))
  # Reverse data if height is descending
  if(z[0,1,0,0]<z[0,0,0,0]):
     data = data[:,::-1,:,:]
     z = z[:,::-1,:,:]
  for it in range(np.shape(data)[0]):
    for iy in range(np.shape(data)[2]):
      for ix in range(np.shape(data)[3]):
         data_int[it,:,iy,ix] = np.interp(z_int,z[it,:,iy,ix],data[it,:,iy,ix])
  return data_int

def load_data(var,index,drop=False):
      return var.isel(index,drop=drop).values

def calcBaseprof(zt,thls,ps,pref0=1e5):
    # constants
    lapserate=np.array([-6.5/1000.,0.,1./1000,2.8/1000])
    zmat=np.array([11000.,20000.,32000.,47000.])
    grav=9.81
    rd=287.04
    cp=1004.
    zsurf=0
    k1=len(zt)
    # Preallocate
    pmat=np.zeros(4)
    tmat=np.zeros(4)
    rhobf=np.zeros(k1)
    pb=np.zeros(k1)
    tb=np.zeros(k1)
    # DALES code
    tsurf=thls*(ps/pref0)**(rd/cp)
    pmat[0]=np.exp((np.log(ps)*lapserate[0]*rd+np.log(tsurf+zsurf*lapserate[0])*grav-
      np.log(tsurf+zmat[0]*lapserate[0])*grav)/(lapserate[0]*rd))
    tmat[0]=tsurf+lapserate[0]*(zmat[0]-zsurf);
    for j in np.arange(1,4):
        if(abs(lapserate[j])<1e-10):
            pmat[j]=np.exp((np.log(pmat[j-1])*tmat[j-1]*rd+zmat[j-1]*grav-zmat[j]*grav)/(tmat[j-1]*rd))
        else:
            pmat[j]=np.exp((np.log(pmat[j-1])*lapserate[j]*rd+np.log(tmat[j-1]+zmat[j-1]*lapserate[j])*grav-np.log(tmat[j-1]+zmat[j]*lapserate[j])*grav)/(lapserate[j]*rd))
        tmat[j]=tmat[j-1]+lapserate[j]*(zmat[j]-zmat[j-1]);

    for k in range(k1):
        if(zt[k]<zmat[0]):
            pb[k]=np.exp((np.log(ps)*lapserate[0]*rd+np.log(tsurf+zsurf*lapserate[0])*grav-np.log(tsurf+zt[k]*lapserate[0])*grav)/(lapserate[0]*rd))
            tb[k]=tsurf+lapserate[0]*(zt[k]-zsurf)
        else:
            j=0
            while(zt[k]>=zmat[j]):
              j=j+1
            tb[k]=tmat[j-1]+lapserate[j]*(zt[k]-zmat[j-1])
            if(abs(lapserate[j])<1e-99):
                pb[k]=np.exp((np.log(pmat[j-1])*tmat[j-1]*rd+zmat[j-1]*grav-zt[k]*grav)/(tmat[j-1]*rd))
            else:
                pb[k]=np.exp((np.log(pmat[j-1])*lapserate[j]*rd+np.log(tmat[j-1]+zmat[j-1]*lapserate[j])*grav-np.log(tmat[j-1]+zt[k]*lapserate[j])*grav)/(lapserate[j]*rd))
        rhobf[k]=pb[k]/(rd*tb[k]) # dry estimate
    return rhobf

def differentiate(data,coord,order,acc=6):
  ncoef   = int(2*np.floor((order+1)/2)-1+acc)
  out     = xr.zeros_like(data)
  out     = out.where(out!=0).load()
  x       = data.coords[coord].values
  ipoints = np.arange((ncoef-1)/2,len(x)-(ncoef-1)/2,dtype=int)
  b       = np.zeros((ncoef))
  b[order]= 1.
  for ip in ipoints:
    A = np.zeros((ncoef,ncoef))
    for j in range(ncoef):
      ip2= ip-int((ncoef-1)/2)+j
      dx = x[ip2]-x[ip]
      for i in range(ncoef):
        A[i,j] = 1/np.math.factorial(i)*dx**i
    coef = np.linalg.solve(A,b)
    out[{coord: ip}] = 0.
    for i in range(ncoef):
      ip2 = ip-int((ncoef-1)/2)+i
      out[{coord: ip}] = out[{coord: ip}]+coef[i]*data[{coord: ip2}]
  return out