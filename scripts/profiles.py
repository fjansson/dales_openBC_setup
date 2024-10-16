from datetime import datetime
import numpy as np
def profiles(input,grid,initfields,data):
  time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
  # Open prof.inp.xxx
  prof = open(f"{input['outpath']}prof.inp.{input['iexpnr']:03}", 'w')
  prof.write(f"# Input profiles created by {input['author']} at {time}\n")
  prof.write('# z thl qt u v tke \n')
  # Open lscale.inp.xxx (Set to zero)
  lscale = open(f"{input['outpath']}lscale.inp.{input['iexpnr']:03}", 'w')
  lscale.write(f"# Large scale forcing profiles created by {input['author']} at {time}\n")
  lscale.write('# z ug vg wfls dqtdxls dqtdyls dqtdtls dthlrad \n')
  # Open scalar.inp.xxx (Set to zero)
  if(input['nsv']>0):
    scalar =  open(f"{input['outpath']}scalar.inp.{input['iexpnr']:03}", 'w')
    scalar.write(f"# Scalar input profiles created by {input['author']} at {time}\n")
    scalar.write('#z qr nr\n')
  # Calculate profiles
  thlprof = initfields['thl0'].mean(dim=['xt','yt']).values
  qtprof = initfields['qt0'].mean(dim=['xt','yt']).values
  uprof  = initfields['u0'].mean(dim=['xm','yt']).values
  vprof  = initfields['v0'].mean(dim=['xt','ym']).values
  e12prof = np.ones(np.shape(thlprof))*input['e12']
  # Write data
  for i in range(grid.kmax):
      prof.write(f"{grid.zt[i]} {thlprof[i]} {qtprof[i]} {uprof[i]} {vprof[i]} {e12prof[i]} \n")
      lscale.write(f"{grid.zt[i]} {0} {0} {0} {0} {0} {0} {0} \n")
      if(input['nsv']>0): scalar.write(f"{grid.zt[i]} " +" ".join(map(str,np.zeros(input['nsv'])))+" \n" )
  prof.close()
  lscale.close()
  scalar.close()
  # Open exnr.inp.xxx (if used)
  if('exnr' in data):
    exnr = open(f"{input['outpath']}exnr.inp.{input['iexpnr']:03}", 'w')
    exnr.write(f"# Exnr function used, thls = {data['exnr'].attrs['thls']}, ps = {data['exnr'].attrs['ps']}, created by {input['author']} at {time}\n")
    for i in range(data.sizes['z']):
      exnr.write(f"{data['z'][i].values} {data['exnr'][i].values} \n")
    exnr.close()
  # Create Nc0.inp.xxx
  if('Nc_0' in input):
    Nc_cst = input['Nc_0']['Nc_cst']
    z_cst  = input['Nc_0']['z_cst']
    z_e    = input['Nc_0']['z_e']
    Nc0prof = np.ones(grid.kmax)*Nc_cst
    Nc0prof[grid.zt>z_cst] = Nc_cst*np.exp(-(grid.zt[grid.zt>z_cst]-z_cst)/z_e)
    fNc0 = open(f"{input['outpath']}nc0.inp.{input['iexpnr']:03}", 'w')
    fNc0.write(f"# Cloud droplet number input profile created by {input['author']} at {time}\n")
    fNc0.write('# z Nc_0\n')
    for i in range(grid.kmax):
      fNc0.write(f"{grid.zt[i]} {Nc0prof[i]} \n")
    fNc0.close()
  return
