# Interpolate fields to DALES domain boundary
# Creates openboundaries.inp.xxx.nc
import numpy as np
import xarray as xr
from datetime import datetime
import pandas as pd 
def boundary_fields(input,grid,data):
  data = data.drop(['lat','lon'])
  # West boundary
  uwest   = data['u'].interp(z=grid.zt, y=grid.yt, x=grid.xm[0], assume_sorted=True).rename({'z': 'zt', 'y': 'yt'}).rename('uwest').drop(['x'])
  vwest   = data['v'].interp(z=grid.zt, y=grid.ym, x=grid.xm[0], assume_sorted=True).rename({'z': 'zt', 'y': 'ym'}).rename('vwest').drop(['x'])
  wwest   = data['w'].interp(z=grid.zm, y=grid.yt, x=grid.xm[0], assume_sorted=True).rename({'z': 'zm', 'y': 'yt'}).rename('wwest').drop(['x'])
  thlwest = data['thl'].interp(z=grid.zt, y=grid.yt, x=grid.xm[0], assume_sorted=True).rename({'z': 'zt', 'y': 'yt'}).rename('thlwest').drop(['x'])
  qtwest  = data['qt'].interp(z=grid.zt, y=grid.yt, x=grid.xm[0], assume_sorted=True).rename({'z': 'zt', 'y': 'yt'}).rename('qtwest').drop(['x'])
  e12west = (xr.ones_like(thlwest)*input['e12']).rename('e12west')
  uwest.attrs.clear(); vwest.attrs.clear(); wwest.attrs.clear(); thlwest.attrs.clear(); qtwest.attrs.clear()
  # East boundary
  ueast   = data['u'].interp(z=grid.zt, y=grid.yt, x=grid.xm[-1], assume_sorted=True).rename({'z': 'zt', 'y': 'yt'}).rename('ueast').drop(['x'])
  veast   = data['v'].interp(z=grid.zt, y=grid.ym, x=grid.xm[-1], assume_sorted=True).rename({'z': 'zt', 'y': 'ym'}).rename('veast').drop(['x'])
  weast   = data['w'].interp(z=grid.zm, y=grid.yt, x=grid.xm[-1], assume_sorted=True).rename({'z': 'zm', 'y': 'yt'}).rename('weast').drop(['x'])
  thleast = data['thl'].interp(z=grid.zt, y=grid.yt, x=grid.xm[-1], assume_sorted=True).rename({'z': 'zt', 'y': 'yt'}).rename('thleast').drop(['x'])
  qteast  = data['qt'].interp(z=grid.zt, y=grid.yt, x=grid.xm[-1], assume_sorted=True).rename({'z': 'zt', 'y': 'yt'}).rename('qteast').drop(['x'])
  e12east = (xr.ones_like(thleast)*input['e12']).rename('e12east')
  ueast.attrs.clear(); veast.attrs.clear(); weast.attrs.clear(); thleast.attrs.clear(); qteast.attrs.clear()
  # South boundary
  usouth   = data['u'].interp(z=grid.zt, y=grid.ym[0], x=grid.xm,assume_sorted=True).rename({'z': 'zt', 'x': 'xm'}).rename('usouth').drop(['y'])
  vsouth   = data['v'].interp(z=grid.zt, y=grid.ym[0], x=grid.xt,assume_sorted=True).rename({'z': 'zt', 'x': 'xt'}).rename('vsouth').drop(['y'])
  wsouth   = data['w'].interp(z=grid.zm, y=grid.ym[0], x=grid.xt,assume_sorted=True).rename({'z': 'zm', 'x': 'xt'}).rename('wsouth').drop(['y'])
  thlsouth = data['thl'].interp(z=grid.zt, y=grid.ym[0], x=grid.xt,assume_sorted=True).rename({'z': 'zt', 'x': 'xt'}).rename('thlsouth').drop(['y'])
  qtsouth  = data['qt'].interp(z=grid.zt, y=grid.ym[0], x=grid.xt,assume_sorted=True).rename({'z': 'zt', 'x': 'xt'}).rename('qtsouth').drop(['y'])
  e12south = (xr.ones_like(thlsouth)*input['e12']).rename('e12south')
  usouth.attrs.clear(); vsouth.attrs.clear(); wsouth.attrs.clear(); thlsouth.attrs.clear(); qtsouth.attrs.clear()
  # North boundary
  unorth   = data['u'].interp(z=grid.zt, y=grid.ym[-1], x=grid.xm, assume_sorted=True).rename({'z': 'zt', 'x': 'xm'}).rename('unorth').drop(['y'])
  vnorth   = data['v'].interp(z=grid.zt, y=grid.ym[-1], x=grid.xt, assume_sorted=True).rename({'z': 'zt', 'x': 'xt'}).rename('vnorth').drop(['y'])
  wnorth   = data['w'].interp(z=grid.zm, y=grid.ym[-1], x=grid.xt, assume_sorted=True).rename({'z': 'zm', 'x': 'xt'}).rename('wnorth').drop(['y'])
  thlnorth = data['thl'].interp(z=grid.zt, y=grid.ym[-1], x=grid.xt, assume_sorted=True).rename({'z': 'zt', 'x': 'xt'}).rename('thlnorth').drop(['y'])
  qtnorth  = data['qt'].interp(z=grid.zt, y=grid.ym[-1], x=grid.xt, assume_sorted=True).rename({'z': 'zt', 'x': 'xt'}).rename('qtnorth').drop(['y'])
  e12north = (xr.ones_like(thlnorth)*input['e12']).rename('e12north')
  unorth.attrs.clear(); vnorth.attrs.clear(); wnorth.attrs.clear(); thlnorth.attrs.clear(); qtnorth.attrs.clear()
  # Top boundary
  utop   = data['u'].interp(z=grid.zm[-1], y=grid.yt, x=grid.xm, assume_sorted=True).rename({'y': 'yt', 'x': 'xm'}).rename('utop').drop(['z'])
  vtop   = data['v'].interp(z=grid.zm[-1], y=grid.ym, x=grid.xt, assume_sorted=True).rename({'y': 'ym', 'x': 'xt'}).rename('vtop').drop(['z'])
  wtop   = data['w'].interp(z=grid.zm[-1], y=grid.yt, x=grid.xt, assume_sorted=True).rename({'y': 'yt', 'x': 'xt'}).rename('wtop').drop(['z'])
  thltop = data['thl'].interp(z=grid.zm[-1], y=grid.yt, x=grid.xt, assume_sorted=True).rename({'y': 'yt', 'x': 'xt'}).rename('thltop').drop(['z'])
  qttop  = data['qt'].interp(z=grid.zm[-1], y=grid.yt, x=grid.xt, assume_sorted=True).rename({'y': 'yt', 'x': 'xt'}).rename('qttop').drop(['z'])
  e12top = (xr.ones_like(thltop)*input['e12']).rename('e12top')
  utop.attrs.clear(); vtop.attrs.clear(); wtop.attrs.clear(); thltop.attrs.clear(); qttop.attrs.clear()
  # Add fields to dataset
  openboundaries = xr.merge([uwest, vwest, wwest, thlwest, qtwest, e12west,
                              ueast, veast, weast, thleast, qteast, e12east,
                              usouth,vsouth,wsouth,thlsouth,qtsouth,e12south,
                              unorth,vnorth,wnorth,thlnorth,qtnorth,e12north,
                              utop,  vtop,  wtop,  thltop,  qttop,  e12top],
                              combine_attrs='drop')
  # Adjust time variable to seconds since initial field
  ts = openboundaries['time'].values.astype('datetime64[s]')
  dts = (ts-np.datetime64(input['time0'],'s'))/np.timedelta64(1, 's')
  openboundaries = openboundaries.assign_coords({'time':('time', dts)})
  openboundaries['time'].attrs.clear()
  # Add variable attributes
  openboundaries['time'] = openboundaries['time'].assign_attrs({'longname': 'Time', 'units': f"seconds since {input['time0']}"})
  openboundaries['xt'] = openboundaries['xt'].assign_attrs({'longname': 'West-East displacement of cell centers','units': 'm'})
  openboundaries['xm'] = openboundaries['xm'].assign_attrs({'longname': 'West-East displacement of cell edges','units': 'm'})
  openboundaries['yt'] = openboundaries['yt'].assign_attrs({'longname': 'South-North displacement of cell centers','units': 'm'})
  openboundaries['ym'] = openboundaries['ym'].assign_attrs({'longname': 'South-North displacement of cell edges','units': 'm'})
  openboundaries['zt'] = openboundaries['zt'].assign_attrs({'longname': 'Vertical displacement of cell centers','units': 'm'})
  openboundaries['zm'] = openboundaries['zm'].assign_attrs({'longname': 'Vertical displacement of cell edges','units': 'm'})
  variables = ['u','v','w','thl','qt','e12']
  units     = ['m/s','m/s','m/s','K','kg/kg','m/s']
  long_names= ['West-East velocity at ',
                'South-North velocity at ',
                'Vertical velocity at ',
                'Liquid water potential temperature at ',
                'Total water specific humidity at ',
                'Square root of turbulent kinetic energy at ']
  for ivar in range(len(variables)):
    var = variables[ivar]
    unit = units[ivar]
    long_name = long_names[ivar]
    for boundary in ['West','East','South','North','top']:
      openboundaries[var+boundary.lower()] = openboundaries[var+boundary.lower()]\
      .assign_attrs({'longname': long_name+boundary+' boundary', 'units': unit})
  # Add global attributes
  openboundaries = openboundaries.assign_attrs({'title': f"openboundaries.inp.{input['iexpnr']:03d}.nc",
                                        'history': f"Created on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
                                        'author': input['author'],
                                        'time0': input['time0']})
  openboundaries.to_netcdf(path=input['outpath']+openboundaries.attrs['title'], mode='w', format="NETCDF4")
  return openboundaries

def boundary_fields_fine(input,grid):
  ix_west = int(input['x_offset']/input['dx_coarse'])
  ix_east = int(ix_west+grid.xsize/input['dx_coarse'])
  iy_south = int(input['y_offset']/input['dy_coarse'])
  iy_north = int(iy_south+grid.ysize/input['dy_coarse'])
  # Get initial boundary fields from initial fields
  if(input['time0']==input['start']):
    with xr.open_mfdataset(f"{input['inpath_coarse']}initfields.inp.*.nc") as ds:
      # West boundary
      uwest0  = ds['u0'].isel(xm=ix_west,drop=True).interp(yt=grid.yt+input['y_offset']).rename('uwest').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(yt=grid.yt,zt=grid.zt)
      vwest0  = ds['v0'].isel(xt=ix_west,drop=True).interp(ym=grid.ym+input['y_offset']).rename('vwest').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(ym=grid.ym,zt=grid.zt)
      wwest0  = ds['w0'].isel(xt=ix_west,drop=True).interp(yt=grid.yt+input['y_offset'],zm=grid.zm,kwargs={"fill_value": "extrapolate"}).rename('wwest').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(yt=grid.yt,zm=grid.zm)
      thlwest0= ds['thl0'].isel(xt=ix_west,drop=True).interp(yt=grid.yt+input['y_offset']).rename('thlwest').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(yt=grid.yt,zt=grid.zt)
      qtwest0 = ds['qt0'].isel(xt=ix_west,drop=True).interp(yt=grid.yt+input['y_offset']).rename('qtwest').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(yt=grid.yt,zt=grid.zt)
      e12west0= ds['e120'].isel(xt=ix_west,drop=True).interp(yt=grid.yt+input['y_offset']).rename('e12west').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(yt=grid.yt,zt=grid.zt)
      if(input['nsv']>0):
        svwest0 =[]
        for isv in range(input['nsv']): 
          svwest0.append(xr.zeros_like(e12west0).rename('svwest'))
        svwest0 = xr.concat(svwest0,'isv')
      # East boundary
      ueast0  = ds['u0'].isel(xm=ix_east,drop=True).interp(yt=grid.yt+input['y_offset']).rename('ueast').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(yt=grid.yt,zt=grid.zt)
      veast0  = ds['v0'].isel(xt=ix_east,drop=True).interp(ym=grid.ym+input['y_offset']).rename('veast').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(ym=grid.ym,zt=grid.zt)
      weast0  = ds['w0'].isel(xt=ix_east,drop=True).interp(yt=grid.yt+input['y_offset'],zm=grid.zm,kwargs={"fill_value": "extrapolate"}).rename('weast').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(yt=grid.yt,zm=grid.zm)
      thleast0= ds['thl0'].isel(xt=ix_east,drop=True).interp(yt=grid.yt+input['y_offset']).rename('thleast').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(yt=grid.yt,zt=grid.zt)
      qteast0 = ds['qt0'].isel(xt=ix_east,drop=True).interp(yt=grid.yt+input['y_offset']).rename('qteast').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(yt=grid.yt,zt=grid.zt)
      e12east0= ds['e120'].isel(xt=ix_east,drop=True).interp(yt=grid.yt+input['y_offset']).rename('e12east').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(yt=grid.yt,zt=grid.zt)
      if(input['nsv']>0):
        sveast0 =[]
        for isv in range(input['nsv']): 
          sveast0.append(xr.zeros_like(e12east0).rename('sveast'))
        sveast0 = xr.concat(sveast0,'isv')
      # South boundary
      usouth0  = ds['u0'].isel(yt=iy_south,drop=True).interp(xm=grid.xm+input['x_offset']).rename('usouth').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xm=grid.xm,zt=grid.zt)
      vsouth0  = ds['v0'].isel(ym=iy_south,drop=True).interp(xt=grid.xt+input['x_offset']).rename('vsouth').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,zt=grid.zt)
      wsouth0  = ds['w0'].isel(yt=iy_south,drop=True).interp(xt=grid.xt+input['x_offset'],zm=grid.zm,kwargs={"fill_value": "extrapolate"}).rename('wsouth').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,zm=grid.zm)
      thlsouth0= ds['thl0'].isel(yt=iy_south,drop=True).interp(xt=grid.xt+input['x_offset']).rename('thlsouth').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,zt=grid.zt)
      qtsouth0 = ds['qt0'].isel(yt=iy_south,drop=True).interp(xt=grid.xt+input['x_offset']).rename('qtsouth').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,zt=grid.zt)
      e12south0= ds['e120'].isel(yt=iy_south,drop=True).interp(xt=grid.xt+input['x_offset']).rename('e12south').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,zt=grid.zt)
      if(input['nsv']>0):
        svsouth0 =[]
        for isv in range(input['nsv']): 
          svsouth0.append(xr.zeros_like(e12south0).rename('svsouth'))
        svsouth0 = xr.concat(svsouth0,'isv')
      # North boundary
      unorth0  = ds['u0'].isel(yt=iy_north,drop=True).interp(xm=grid.xm+input['x_offset']).rename('unorth').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xm=grid.xm,zt=grid.zt)
      vnorth0  = ds['v0'].isel(ym=iy_north,drop=True).interp(xt=grid.xt+input['x_offset']).rename('vnorth').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,zt=grid.zt)
      wnorth0  = ds['w0'].isel(yt=iy_north,drop=True).interp(xt=grid.xt+input['x_offset'],zm=grid.zm,kwargs={"fill_value": "extrapolate"}).rename('wnorth').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,zm=grid.zm)
      thlnorth0= ds['thl0'].isel(yt=iy_north,drop=True).interp(xt=grid.xt+input['x_offset']).rename('thlnorth').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,zt=grid.zt)
      qtnorth0 = ds['qt0'].isel(yt=iy_north,drop=True).interp(xt=grid.xt+input['x_offset']).rename('qtnorth').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,zt=grid.zt)
      e12north0= ds['e120'].isel(yt=iy_north,drop=True).interp(xt=grid.xt+input['x_offset']).rename('e12north').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,zt=grid.zt)
      if(input['nsv']>0):
        svnorth0 =[]
        for isv in range(input['nsv']): 
          svnorth0.append(xr.zeros_like(e12north0).rename('svnorth'))
        svnorth0 = xr.concat(svnorth0,'isv')
      # Top boundary
      utop0  = ds['u0'].isel(zt=grid.kmax-1,drop=True).interp(xm=grid.xm+input['x_offset'],yt=grid.yt+input['y_offset']).rename('utop').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xm=grid.xm,yt=grid.yt)
      vtop0  = ds['v0'].isel(zt=grid.kmax-1,drop=True).interp(xt=grid.xt+input['x_offset'],ym=grid.ym+input['y_offset']).rename('vtop').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,ym=grid.ym)
      wtop0  = ds['w0'].isel(zm=grid.kmax,drop=True).interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('wtop').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,yt=grid.yt)
      thltop0= ds['thl0'].isel(zt=grid.kmax-1,drop=True).interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('thltop').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,yt=grid.yt)
      qttop0 = ds['qt0'].isel(zt=grid.kmax-1,drop=True).interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('qttop').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,yt=grid.yt)
      e12top0= ds['e120'].isel(zt=grid.kmax-1,drop=True).interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('e12top').expand_dims({'time':[pd.Timestamp(input['time0'])]},axis=0).assign_coords(xt=grid.xt,yt=grid.yt)
      if(input['nsv']>0):
        svtop0 =[]
        for isv in range(input['nsv']): 
          svtop0.append(xr.zeros_like(e12top0).rename('svtop'))
        svtop0 = xr.concat(svtop0,'isv')
  # Get initial boundary fields from previous simulation
  else:
    # West boundary
    path = f"{input['outpath_coarse_old']}crossyz/{ix_west+2:04d}/"
    with xr.open_mfdataset(f"{path}uyz*",chunks={"time": input['tchunk']}) as ds:
      uwest0 = ds['uyz'].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset']).rename('uwest').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}vyz*",chunks={"time": input['tchunk']}) as ds:
      vwest0 = ds['vyz'].isel(time=-1,drop=True).interp(ym=grid.ym+input['y_offset']).rename('vwest').assign_coords(ym=grid.ym,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}wyz*",chunks={"time": input['tchunk']}) as ds:
      wwest0 = ds['wyz'].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset'],zm=grid.zm,kwargs={"fill_value": "extrapolate"}).rename('wwest').assign_coords(yt=grid.yt,zm=grid.zm).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}thlyz*",chunks={"time": input['tchunk']}) as ds:
      thlwest0 = ds['thlyz'].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset']).rename('thlwest').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}qtyz*",chunks={"time": input['tchunk']}) as ds:
      qtwest0 = ds['qtyz'].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset']).rename('qtwest').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}e120yz*",chunks={"time": input['tchunk']}) as ds:
      e12west0 = ds['e120yz'].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset']).rename('e12west').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    if(input['nsv']>0):
      svwest0 =[]
      with xr.open_mfdataset(f"{path}nryz*",chunks={"time": input['tchunk']}) as ds:  
        svwest0.append(ds[f"nryz"].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset']).rename('svwest').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims({'isv':[1],'time':[pd.Timestamp(input['start'])]},axis=[0,1]))
      with xr.open_mfdataset(f"{path}qryz*",chunks={"time": input['tchunk']}) as ds:  
        svwest0.append(ds[f"qryz"].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset']).rename('svwest').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims({'isv':[2],'time':[pd.Timestamp(input['start'])]},axis=[0,1]))
      svwest0 = xr.concat(svwest0,'isv')
    # east boundary
    path = f"{input['outpath_coarse_old']}crossyz/{ix_east+2:04d}/"
    with xr.open_mfdataset(f"{path}uyz*",chunks={"time": input['tchunk']}) as ds:
      ueast0 = ds['uyz'].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset']).rename('ueast').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}vyz*",chunks={"time": input['tchunk']}) as ds:
      veast0 = ds['vyz'].isel(time=-1,drop=True).interp(ym=grid.ym+input['y_offset']).rename('veast').assign_coords(ym=grid.ym,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}wyz*",chunks={"time": input['tchunk']}) as ds:
      weast0 = ds['wyz'].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset'],zm=grid.zm,kwargs={"fill_value": "extrapolate"}).rename('weast').assign_coords(yt=grid.yt,zm=grid.zm).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}thlyz*",chunks={"time": input['tchunk']}) as ds:
      thleast0 = ds['thlyz'].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset']).rename('thleast').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}qtyz*",chunks={"time": input['tchunk']}) as ds:
      qteast0 = ds['qtyz'].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset']).rename('qteast').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}e120yz*",chunks={"time": input['tchunk']}) as ds:
      e12east0 = ds['e120yz'].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset']).rename('e12east').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    if(input['nsv']>0):
      sveast0 =[]
      with xr.open_mfdataset(f"{path}nryz*",chunks={"time": input['tchunk']}) as ds:  
        sveast0.append(ds[f"nryz"].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset']).rename('sveast').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims({'isv':[1],'time':[pd.Timestamp(input['start'])]},axis=[0,1]))
      with xr.open_mfdataset(f"{path}qryz*",chunks={"time": input['tchunk']}) as ds:  
        sveast0.append(ds[f"qryz"].isel(time=-1,drop=True).interp(yt=grid.yt+input['y_offset']).rename('sveast').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims({'isv':[2],'time':[pd.Timestamp(input['start'])]},axis=[0,1]))
      sveast0 = xr.concat(sveast0,'isv')
    # south boundary
    path = f"{input['outpath_coarse_old']}crossxz/{iy_south+2:04d}/"
    with xr.open_mfdataset(f"{path}uxz*",chunks={"time": input['tchunk']}) as ds:
      usouth0 = ds['uxz'].isel(time=-1,drop=True).interp(xm=grid.xm+input['x_offset']).rename('usouth').assign_coords(xm=grid.xm,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}vxz*",chunks={"time": input['tchunk']}) as ds:
      vsouth0 = ds['vxz'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset']).rename('vsouth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}wxz*",chunks={"time": input['tchunk']}) as ds:
      wsouth0 = ds['wxz'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset'],zm=grid.zm,kwargs={"fill_value": "extrapolate"}).rename('wsouth').assign_coords(xt=grid.xt,zm=grid.zm).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}thlxz*",chunks={"time": input['tchunk']}) as ds:
      thlsouth0 = ds['thlxz'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset']).rename('thlsouth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}qtxz*",chunks={"time": input['tchunk']}) as ds:
      qtsouth0 = ds['qtxz'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset']).rename('qtsouth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}e120xz*",chunks={"time": input['tchunk']}) as ds:
      e12south0 = ds['e120xz'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset']).rename('e12south').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    if(input['nsv']>0):
      svsouth0 =[]
      with xr.open_mfdataset(f"{path}nrxz*",chunks={"time": input['tchunk']}) as ds:  
        svsouth0.append(ds[f"nrxz"].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset']).rename('svsouth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims({'isv':[1],'time':[pd.Timestamp(input['start'])]},axis=[0,1]))
      with xr.open_mfdataset(f"{path}qrxz*",chunks={"time": input['tchunk']}) as ds:  
        svsouth0.append(ds[f"qrxz"].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset']).rename('svsouth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims({'isv':[2],'time':[pd.Timestamp(input['start'])]},axis=[0,1]))
      svsouth0 = xr.concat(svsouth0,'isv')
    # north boundary
    path = f"{input['outpath_coarse_old']}crossxz/{iy_north+2:04d}/"
    with xr.open_mfdataset(f"{path}uxz*",chunks={"time": input['tchunk']}) as ds:
      unorth0 = ds['uxz'].isel(time=-1,drop=True).interp(xm=grid.xm+input['x_offset']).rename('unorth').assign_coords(xm=grid.xm,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}vxz*",chunks={"time": input['tchunk']}) as ds:
      vnorth0 = ds['vxz'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset']).rename('vnorth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}wxz*",chunks={"time": input['tchunk']}) as ds:
      wnorth0 = ds['wxz'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset'],zm=grid.zm,kwargs={"fill_value": "extrapolate"}).rename('wnorth').assign_coords(xt=grid.xt,zm=grid.zm).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}thlxz*",chunks={"time": input['tchunk']}) as ds:
      thlnorth0 = ds['thlxz'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset']).rename('thlnorth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}qtxz*",chunks={"time": input['tchunk']}) as ds:
      qtnorth0 = ds['qtxz'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset']).rename('qtnorth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}e120xz*",chunks={"time": input['tchunk']}) as ds:
      e12north0 = ds['e120xz'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset']).rename('e12north').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    if(input['nsv']>0):
      svnorth0 =[]
      with xr.open_mfdataset(f"{path}nrxz*",chunks={"time": input['tchunk']}) as ds:  
        svnorth0.append(ds[f"nrxz"].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset']).rename('svnorth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims({'isv':[1],'time':[pd.Timestamp(input['start'])]},axis=[0,1]))
      with xr.open_mfdataset(f"{path}qrxz*",chunks={"time": input['tchunk']}) as ds:  
        svnorth0.append(ds[f"qrxz"].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset']).rename('svnorth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims({'isv':[2],'time':[pd.Timestamp(input['start'])]},axis=[0,1]))
      svnorth0 = xr.concat(svnorth0,'isv')
    # top boundary
    path = f"{input['outpath_coarse_old']}crossxy/{grid.kmax:04d}/"
    with xr.open_mfdataset(f"{path}uxy*",chunks={"time": input['tchunk']}) as ds:
      utop0 = ds['uxy'].isel(time=-1,drop=True).interp(xm=grid.xm+input['x_offset'],yt=grid.yt+input['y_offset']).rename('utop').assign_coords(xm=grid.xm,yt=grid.yt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}vxy*",chunks={"time": input['tchunk']}) as ds:
      vtop0 = ds['vxy'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset'],ym=grid.ym+input['y_offset']).rename('vtop').assign_coords(xt=grid.xt,ym=grid.ym).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}wxy*",chunks={"time": input['tchunk']}) as ds:
      wtop0 = ds['wxy'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('wtop').assign_coords(xt=grid.xt,yt=grid.yt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}thlxy*",chunks={"time": input['tchunk']}) as ds:
      thltop0 = ds['thlxy'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('thltop').assign_coords(xt=grid.xt,yt=grid.yt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}qtxy*",chunks={"time": input['tchunk']}) as ds:
      qttop0 = ds['qtxy'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('qttop').assign_coords(xt=grid.xt,yt=grid.yt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    with xr.open_mfdataset(f"{path}e120xy*",chunks={"time": input['tchunk']}) as ds:
      e12top0 = ds['e120xy'].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('e12top').assign_coords(xt=grid.xt,yt=grid.yt).expand_dims({'time':[pd.Timestamp(input['start'])]},axis=0)
    if(input['nsv']>0):
      svtop0 =[]
      with xr.open_mfdataset(f"{path}nrxy*",chunks={"time": input['tchunk']}) as ds:  
        svtop0.append(ds[f"nrxy"].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('svtop').assign_coords(xt=grid.xt,yt=grid.yt).expand_dims({'isv':[1],'time':[pd.Timestamp(input['start'])]},axis=[0,1]))
      with xr.open_mfdataset(f"{path}qrxy*",chunks={"time": input['tchunk']}) as ds:  
        svtop0.append(ds[f"qrxy"].isel(time=-1,drop=True).interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('svtop').assign_coords(xt=grid.xt,yt=grid.yt).expand_dims({'isv':[2],'time':[pd.Timestamp(input['start'])]},axis=[0,1]))
      svtop0 = xr.concat(svtop0,'isv')
  # Get later time steps from corresponding coarse simulation output
  # West boundary
  path = f"{input['outpath_coarse']}crossyz/{ix_west+2:04d}/"
  with xr.open_mfdataset(f"{path}uyz*",chunks={"time": input['tchunk']}) as ds:
    uwest = ds['uyz'].interp(yt=grid.yt+input['y_offset']).rename('uwest').assign_coords(yt=grid.yt,zt=grid.zt)
    uwest = xr.concat([uwest0,uwest],dim='time')
  with xr.open_mfdataset(f"{path}vyz*",chunks={"time": input['tchunk']}) as ds:
    vwest = ds['vyz'].interp(ym=grid.ym+input['y_offset']).rename('vwest').assign_coords(ym=grid.ym,zt=grid.zt)
    vwest = xr.concat([vwest0,vwest],dim='time')
  with xr.open_mfdataset(f"{path}wyz*",chunks={"time": input['tchunk']}) as ds:
    wwest = ds['wyz'].interp(yt=grid.yt+input['y_offset'],zm=grid.zm,kwargs={"fill_value": "extrapolate"}).rename('wwest').assign_coords(yt=grid.yt,zm=grid.zm)
    wwest = xr.concat([wwest0,wwest],dim='time')
  with xr.open_mfdataset(f"{path}thlyz*",chunks={"time": input['tchunk']}) as ds:
    thlwest = ds['thlyz'].interp(yt=grid.yt+input['y_offset']).rename('thlwest').assign_coords(yt=grid.yt,zt=grid.zt)
    thlwest = xr.concat([thlwest0,thlwest],dim='time')
  with xr.open_mfdataset(f"{path}qtyz*",chunks={"time": input['tchunk']}) as ds:
    qtwest = ds['qtyz'].interp(yt=grid.yt+input['y_offset']).rename('qtwest').assign_coords(yt=grid.yt,zt=grid.zt)
    qtwest = xr.concat([qtwest0,qtwest],dim='time')
  with xr.open_mfdataset(f"{path}e120yz*",chunks={"time": input['tchunk']}) as ds:
    e12west = ds['e120yz'].interp(yt=grid.yt+input['y_offset']).rename('e12west').assign_coords(yt=grid.yt,zt=grid.zt)
    e12west = xr.concat([e12west0,e12west],dim='time')
  if(input['nsv']>0):
    svwest =[]
    with xr.open_mfdataset(f"{path}nryz*",chunks={"time": input['tchunk']}) as ds:
      svwest.append(ds[f"nryz"].interp(yt=grid.yt+input['y_offset']).rename('svwest').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims(dim={'isv':np.array([1])},axis=0))
    with xr.open_mfdataset(f"{path}qryz*",chunks={"time": input['tchunk']}) as ds:
      svwest.append(ds[f"qryz"].interp(yt=grid.yt+input['y_offset']).rename('svwest').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims(dim={'isv':np.array([2])},axis=0))
    # for isv in range(input['nsv']):
    #   with xr.open_mfdataset(f"{path}sv{isv+1:03}*",chunks={"time": input['tchunk']}) as ds:
    #     svwest.append(ds[f"sv{isv+1:03}"].interp(yt=grid.yt+input['y_offset']).rename('svwest').assign_coords(yt=grid.yt,zt=grid.zt))
    svwest = xr.concat(svwest,'isv')
    svwest = xr.concat([svwest0,svwest],dim='time')
  # east boundary
  path = f"{input['outpath_coarse']}crossyz/{ix_east+2:04d}/"
  with xr.open_mfdataset(f"{path}uyz*",chunks={"time": input['tchunk']}) as ds:
    ueast = ds['uyz'].interp(yt=grid.yt+input['y_offset']).rename('ueast').assign_coords(yt=grid.yt,zt=grid.zt)
    ueast = xr.concat([ueast0,ueast],dim='time')
  with xr.open_mfdataset(f"{path}vyz*",chunks={"time": input['tchunk']}) as ds:
    veast = ds['vyz'].interp(ym=grid.ym+input['y_offset']).rename('veast').assign_coords(ym=grid.ym,zt=grid.zt)
    veast = xr.concat([veast0,veast],dim='time')
  with xr.open_mfdataset(f"{path}wyz*",chunks={"time": input['tchunk']}) as ds:
    weast = ds['wyz'].interp(yt=grid.yt+input['y_offset'],zm=grid.zm,kwargs={"fill_value": "extrapolate"}).rename('weast').assign_coords(yt=grid.yt,zm=grid.zm)
    weast = xr.concat([weast0,weast],dim='time')
  with xr.open_mfdataset(f"{path}thlyz*",chunks={"time": input['tchunk']}) as ds:
    thleast = ds['thlyz'].interp(yt=grid.yt+input['y_offset']).rename('thleast').assign_coords(yt=grid.yt,zt=grid.zt)
    thleast = xr.concat([thleast0,thleast],dim='time')
  with xr.open_mfdataset(f"{path}qtyz*",chunks={"time": input['tchunk']}) as ds:
    qteast = ds['qtyz'].interp(yt=grid.yt+input['y_offset']).rename('qteast').assign_coords(yt=grid.yt,zt=grid.zt)
    qteast = xr.concat([qteast0,qteast],dim='time')
  with xr.open_mfdataset(f"{path}e120yz*",chunks={"time": input['tchunk']}) as ds:
    e12east = ds['e120yz'].interp(yt=grid.yt+input['y_offset']).rename('e12east').assign_coords(yt=grid.yt,zt=grid.zt)
    e12east = xr.concat([e12east0,e12east],dim='time')
  if(input['nsv']>0):
    sveast =[]
    with xr.open_mfdataset(f"{path}nryz*",chunks={"time": input['tchunk']}) as ds:
      sveast.append(ds[f"nryz"].interp(yt=grid.yt+input['y_offset']).rename('sveast').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims(dim={'isv':np.array([1])},axis=0))
    with xr.open_mfdataset(f"{path}qryz*",chunks={"time": input['tchunk']}) as ds:
      sveast.append(ds[f"qryz"].interp(yt=grid.yt+input['y_offset']).rename('sveast').assign_coords(yt=grid.yt,zt=grid.zt).expand_dims(dim={'isv':np.array([2])},axis=0))
    # for isv in range(input['nsv']):
    #   with xr.open_mfdataset(f"{path}sv{isv+1:03}*",chunks={"time": input['tchunk']}) as ds:
    #     sveast.append(ds[f"sv{isv+1:03}"].interp(yt=grid.yt+input['y_offset']).rename('sveast').assign_coords(yt=grid.yt,zt=grid.zt))
    sveast = xr.concat(sveast,'isv')
    sveast = xr.concat([sveast0,sveast],dim='time')
  # south boundary
  path = f"{input['outpath_coarse']}crossxz/{iy_south+2:04d}/"
  with xr.open_mfdataset(f"{path}uxz*",chunks={"time": input['tchunk']}) as ds:
    usouth = ds['uxz'].interp(xm=grid.xm+input['x_offset']).rename('usouth').assign_coords(xm=grid.xm,zt=grid.zt)
    usouth = xr.concat([usouth0,usouth],dim='time')
  with xr.open_mfdataset(f"{path}vxz*",chunks={"time": input['tchunk']}) as ds:
    vsouth = ds['vxz'].interp(xt=grid.xt+input['x_offset']).rename('vsouth').assign_coords(xt=grid.xt,zt=grid.zt)
    vsouth = xr.concat([vsouth0,vsouth],dim='time')
  with xr.open_mfdataset(f"{path}wxz*",chunks={"time": input['tchunk']}) as ds:
    wsouth = ds['wxz'].interp(xt=grid.xt+input['x_offset'],zm=grid.zm,kwargs={"fill_value": "extrapolate"}).rename('wsouth').assign_coords(xt=grid.xt,zm=grid.zm)
    wsouth = xr.concat([wsouth0,wsouth],dim='time')
  with xr.open_mfdataset(f"{path}thlxz*",chunks={"time": input['tchunk']}) as ds:
    thlsouth = ds['thlxz'].interp(xt=grid.xt+input['x_offset']).rename('thlsouth').assign_coords(xt=grid.xt,zt=grid.zt)
    thlsouth = xr.concat([thlsouth0,thlsouth],dim='time')
  with xr.open_mfdataset(f"{path}qtxz*",chunks={"time": input['tchunk']}) as ds:
    qtsouth = ds['qtxz'].interp(xt=grid.xt+input['x_offset']).rename('qtsouth').assign_coords(xt=grid.xt,zt=grid.zt)
    qtsouth = xr.concat([qtsouth0,qtsouth],dim='time')
  with xr.open_mfdataset(f"{path}e120xz*",chunks={"time": input['tchunk']}) as ds:
    e12south = ds['e120xz'].interp(xt=grid.xt+input['x_offset']).rename('e12south').assign_coords(xt=grid.xt,zt=grid.zt)
    e12south = xr.concat([e12south0,e12south],dim='time')
  if(input['nsv']>0):
    svsouth =[]
    with xr.open_mfdataset(f"{path}nrxz*",chunks={"time": input['tchunk']}) as ds:
        svsouth.append(ds[f"nrxz"].interp(xt=grid.xt+input['x_offset']).rename('svsouth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims(dim={'isv':np.array([1])},axis=0))
    with xr.open_mfdataset(f"{path}qrxz*",chunks={"time": input['tchunk']}) as ds:
        svsouth.append(ds[f"qrxz"].interp(xt=grid.xt+input['x_offset']).rename('svsouth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims(dim={'isv':np.array([2])},axis=0))
    # for isv in range(input['nsv']):
    #   with xr.open_mfdataset(f"{path}sv{isv+1:03}*",chunks={"time": input['tchunk']}) as ds:
    #     svsouth.append(ds[f"sv{isv+1:03}"].interp(xt=grid.xt+input['x_offset']).rename('svsouth').assign_coords(xt=grid.xt,zt=grid.zt))
    svsouth = xr.concat(svsouth,'isv')
    svsouth = xr.concat([svsouth0,svsouth],dim='time')
  # north boundary
  path = f"{input['outpath_coarse']}crossxz/{iy_north+2:04d}/"
  with xr.open_mfdataset(f"{path}uxz*",chunks={"time": input['tchunk']}) as ds:
    unorth = ds['uxz'].interp(xm=grid.xm+input['x_offset']).rename('unorth').assign_coords(xm=grid.xm,zt=grid.zt)
    unorth = xr.concat([unorth0,unorth],dim='time')
  with xr.open_mfdataset(f"{path}vxz*",chunks={"time": input['tchunk']}) as ds:
    vnorth = ds['vxz'].interp(xt=grid.xt+input['x_offset']).rename('vnorth').assign_coords(xt=grid.xt,zt=grid.zt)
    vnorth = xr.concat([vnorth0,vnorth],dim='time')
  with xr.open_mfdataset(f"{path}wxz*",chunks={"time": input['tchunk']}) as ds:
    wnorth = ds['wxz'].interp(xt=grid.xt+input['x_offset'],zm=grid.zm,kwargs={"fill_value": "extrapolate"}).rename('wnorth').assign_coords(xt=grid.xt,zm=grid.zm)
    wnorth = xr.concat([wnorth0,wnorth],dim='time')
  with xr.open_mfdataset(f"{path}thlxz*",chunks={"time": input['tchunk']}) as ds:
    thlnorth = ds['thlxz'].interp(xt=grid.xt+input['x_offset']).rename('thlnorth').assign_coords(xt=grid.xt,zt=grid.zt)
    thlnorth = xr.concat([thlnorth0,thlnorth],dim='time')
  with xr.open_mfdataset(f"{path}qtxz*",chunks={"time": input['tchunk']}) as ds:
    qtnorth = ds['qtxz'].interp(xt=grid.xt+input['x_offset']).rename('qtnorth').assign_coords(xt=grid.xt,zt=grid.zt)
    qtnorth = xr.concat([qtnorth0,qtnorth],dim='time')
  with xr.open_mfdataset(f"{path}e120xz*",chunks={"time": input['tchunk']}) as ds:
    e12north = ds['e120xz'].interp(xt=grid.xt+input['x_offset']).rename('e12north').assign_coords(xt=grid.xt,zt=grid.zt)
    e12north = xr.concat([e12north0,e12north],dim='time')
  if(input['nsv']>0):
    svnorth =[]
    with xr.open_mfdataset(f"{path}nrxz*",chunks={"time": input['tchunk']}) as ds:
        svnorth.append(ds[f"nrxz"].interp(xt=grid.xt+input['x_offset']).rename('svnorth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims(dim={'isv':np.array([1])},axis=0))
    with xr.open_mfdataset(f"{path}qrxz*",chunks={"time": input['tchunk']}) as ds:
        svnorth.append(ds[f"qrxz"].interp(xt=grid.xt+input['x_offset']).rename('svnorth').assign_coords(xt=grid.xt,zt=grid.zt).expand_dims(dim={'isv':np.array([2])},axis=0))
    # for isv in range(input['nsv']):
    #   with xr.open_mfdataset(f"{path}sv{isv+1:03}*",chunks={"time": input['tchunk']}) as ds:
    #     svnorth.append(ds[f"sv{isv+1:03}"].interp(xt=grid.xt+input['x_offset']).rename('svnorth').assign_coords(xt=grid.xt,zt=grid.zt))
    svnorth = xr.concat(svnorth,'isv')
    svnorth = xr.concat([svnorth0,svnorth],dim='time')
  # top boundary
  path = f"{input['outpath_coarse']}crossxy/{grid.kmax:04d}/"
  with xr.open_mfdataset(f"{path}uxy*",chunks={"time": input['tchunk']}) as ds:
    utop = ds['uxy'].interp(xm=grid.xm+input['x_offset'],yt=grid.yt+input['y_offset']).rename('utop').assign_coords(xm=grid.xm,yt=grid.yt)
    utop = xr.concat([utop0,utop],dim='time')
  with xr.open_mfdataset(f"{path}vxy*",chunks={"time": input['tchunk']}) as ds:
    vtop = ds['vxy'].interp(xt=grid.xt+input['x_offset'],ym=grid.ym+input['y_offset']).rename('vtop').assign_coords(xt=grid.xt,ym=grid.ym)
    vtop = xr.concat([vtop0,vtop],dim='time')
  with xr.open_mfdataset(f"{path}wxy*",chunks={"time": input['tchunk']}) as ds:
    wtop = ds['wxy'].interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('wtop').assign_coords(xt=grid.xt,yt=grid.yt)
    wtop = xr.concat([wtop0,wtop],dim='time')
  with xr.open_mfdataset(f"{path}thlxy*",chunks={"time": input['tchunk']}) as ds:
    thltop = ds['thlxy'].interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('thltop').assign_coords(xt=grid.xt,yt=grid.yt)
    thltop = xr.concat([thltop0,thltop],dim='time')
  with xr.open_mfdataset(f"{path}qtxy*",chunks={"time": input['tchunk']}) as ds:
    qttop = ds['qtxy'].interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('qttop').assign_coords(xt=grid.xt,yt=grid.yt)
    qttop = xr.concat([qttop0,qttop],dim='time')
  with xr.open_mfdataset(f"{path}e120xy*",chunks={"time": input['tchunk']}) as ds:
    e12top = ds['e120xy'].interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('e12top').assign_coords(xt=grid.xt,yt=grid.yt)
    e12top = xr.concat([e12top0,e12top],dim='time')
  if(input['nsv']>0):
    svtop =[]
    with xr.open_mfdataset(f"{path}nrxy*",chunks={"time": input['tchunk']}) as ds:
      svtop.append(ds[f"nrxy"].interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('svtop').assign_coords(xt=grid.xt,yt=grid.yt).expand_dims(dim={'isv':np.array([1])},axis=0))
    with xr.open_mfdataset(f"{path}qrxy*",chunks={"time": input['tchunk']}) as ds:
      svtop.append(ds[f"qrxy"].interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('svtop').assign_coords(xt=grid.xt,yt=grid.yt).expand_dims(dim={'isv':np.array([2])},axis=0))
    # for isv in range(input['nsv']):
    #   with xr.open_mfdataset(f"{path}sv{isv+1:03}*",chunks={"time": input['tchunk']}) as ds:
    #     svtop.append(ds[f"sv{isv+1:03}"].interp(xt=grid.xt+input['x_offset'],yt=grid.yt+input['y_offset']).rename('svtop').assign_coords(xt=grid.xt,yt=grid.yt))
    svtop = xr.concat(svtop,'isv')
    svtop = xr.concat([svtop0,svtop],dim='time')
  # Add fields to dataset
  if(input['nsv']>0):
    openboundaries = xr.merge([uwest, vwest, wwest, thlwest, qtwest, e12west, svwest,
                              ueast, veast, weast, thleast, qteast, e12east, sveast,
                              usouth,vsouth,wsouth,thlsouth,qtsouth,e12south, svsouth,
                              unorth,vnorth,wnorth,thlnorth,qtnorth,e12north, svnorth,
                              utop,  vtop,  wtop,  thltop,  qttop,  e12top, svtop],
                              combine_attrs='drop')
  else:
    openboundaries = xr.merge([uwest, vwest, wwest, thlwest, qtwest, e12west,
                                ueast, veast, weast, thleast, qteast, e12east,
                                usouth,vsouth,wsouth,thlsouth,qtsouth,e12south,
                                unorth,vnorth,wnorth,thlnorth,qtnorth,e12north,
                                utop,  vtop,  wtop,  thltop,  qttop,  e12top],
                                combine_attrs='drop')
  dts  = (openboundaries.time.values.astype('datetime64[s]')-np.datetime64(input['time0'],'s'))/np.timedelta64(1, 's')
  openboundaries = openboundaries.assign_coords({'time':('time', dts)})
  # # Adjust time variable to seconds since initial field
  # ts = openboundaries['time'].values.astype('datetime64[s]')
  # dts = (ts-np.datetime64(input['time0'],'s'))/np.timedelta64(1, 's')
  # openboundaries = openboundaries.assign_coords({'time':('time', dts)})
  # Add variable attributes
  openboundaries['time'] = openboundaries['time'].assign_attrs({'longname': 'Time'})#, 'units': f"seconds since {input['time0']}"})
  openboundaries.time.encoding['units'] = f"seconds since {input['time0']}"
  openboundaries['xt'] = openboundaries['xt'].assign_attrs({'longname': 'West-East displacement of cell centers','units': 'm'})
  openboundaries['xm'] = openboundaries['xm'].assign_attrs({'longname': 'West-East displacement of cell edges','units': 'm'})
  openboundaries['yt'] = openboundaries['yt'].assign_attrs({'longname': 'South-North displacement of cell centers','units': 'm'})
  openboundaries['ym'] = openboundaries['ym'].assign_attrs({'longname': 'South-North displacement of cell edges','units': 'm'})
  openboundaries['zt'] = openboundaries['zt'].assign_attrs({'longname': 'Vertical displacement of cell centers','units': 'm'})
  openboundaries['zm'] = openboundaries['zm'].assign_attrs({'longname': 'Vertical displacement of cell edges','units': 'm'})
  variables = ['u','v','w','thl','qt','e12']
  if(input['nsv']>0):
    variables.append('sv')
  units     = ['m/s','m/s','m/s','K','kg/kg','m/s']
  if(input['nsv']>0):
    units.append('kg/kg')
  long_names= ['West-East velocity at ',
                'South-North velocity at ',
                'Vertical velocity at ',
                'Liquid water potential temperature at ',
                'Total water specific humidity at ',
                'Square root of turbulent kinetic energy at ']
  if(input['nsv']>0):
    long_names.append("scalar fields at ")
  for ivar in range(len(variables)):
    var = variables[ivar]
    unit = units[ivar]
    long_name = long_names[ivar]
    for boundary in ['West','East','South','North','top']:
      openboundaries[var+boundary.lower()] = openboundaries[var+boundary.lower()]\
      .assign_attrs({'longname': long_name+boundary+' boundary', 'units': unit})
  # Add global attributes
  openboundaries = openboundaries.assign_attrs({'title': f"openboundaries.inp.{input['iexpnr']:03d}.nc",
                                        'history': f"Created on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
                                        'author': input['author'],
                                        'time0': input['time0']})
  openboundaries.to_netcdf(path=input['outpath']+openboundaries.attrs['title'], mode='w', format="NETCDF4")
  return openboundaries
