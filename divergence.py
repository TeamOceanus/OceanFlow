import netCDF4
import numpy as np
import matplotlib.pyplot as plt

def divergence(f):
	num_dims = len(f)
	return np.ufunc.reduce(np.add, [np.gradient(f[i], axis=i) for i in range(num_dims)])

for i in range(1992, 2020):
	data = netCDF4.Dataset('data\\world_oscar_vel_5d%d.nc.gz' %(i), format = 'NETCDF4')

	for j in range(data.variables['time'].size):
		uf = data.variables['uf'][j][0]
		vf = data.variables['vf'][j][0]

		Fx = np.array(uf[:][::-1])
		Fy = np.array(vf[:][::-1])
		F = [Fx, Fy]
		g = divergence(F)

		plt.figure(figsize=(9, 4))
		plt.pcolormesh(g)
#		plt.colorbar()
		plt.savefig("%d_%d.png" %(i, j+1), format = 'png')