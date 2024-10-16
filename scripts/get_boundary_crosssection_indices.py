import json
import sys
with open(sys.argv[1]) as f: input = json.load(f)
input = input['fine']
ix_west = int(input['x_offset']/input['dx_coarse'])
ix_east = int(ix_west+input['grid']['xsize']/input['dx_coarse'])
iy_south = int(input['y_offset']/input['dy_coarse'])
iy_north = int(iy_south+input['grid']['ysize']/input['dy_coarse'])
print(f"crossortho: {ix_west+2}, {ix_east+2}")
print(f"crossplane: {iy_south+2}, {iy_north+2}")