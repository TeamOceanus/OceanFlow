# -*- coding: utf-8 -*-
from netCDF4 import Dataset
dataset = Dataset('world_oscar_vel_5d1992.nc.gz')

"""Read the `uf` data to numpy array."""

uf = dataset.variables['uf'][0][0].data
vf = dataset.variables['vf'][0][0].data

lon = dataset.variables['longitude']
lat = dataset.variables['latitude']

import matplotlib.pyplot as plt
import numpy as np
import random as rd

x_axis = np.arange(0, 360, 1)
y_axis = np.arange(139, -1, 1)

R = 5 # 지구 반지름은 6378.1 km

def findNext(latitude, longitude):
    global R, uf, vf, lon, lat
    try:
        lat2 = int(round(latitude - 0.5) + 0.5 - lat[0]) % 140
        lon2 = int(round(longitude - 0.5) + 0.5 - lon[0]) % 360
        u2 = uf[lat2][lon2]
        v2 = vf[lat2][lon2]
        finTheta = latitude + (2*u2)/pow(R, 2)
        finPhi = longitude + (2*v2)/pow(R, 2)
        return (finTheta, finPhi) # 경도, 위도
    except ValueError:
        return False

def validation(latitude, longitude):
    lat2 = int(round(latitude - 0.5) + 0.5 - lat[0]) % 140
    lon2 = int(round(longitude - 0.5) + 0.5 - lon[0]) % 360
    if uf[lat2][lon2] == np.nan or vf[lat2][lon2] == np.nan:
        return False
    else:
        return True
    
def findStart():
    global uf, vf
    Theta = rd.uniform(20.5, 379.5)
    Phi = rd.uniform(-69.5, 69.5)
    while not validation(Theta, Phi):
        Theta = rd.uniform(20.5, 379.5)
        Phi = rd.uniform(-69.5, 69.5)
    return Theta, Phi

def euclidD(A, B):
    return pow((A[0] - B[0])**2 + (A[1] - B[1])**2, 0.5)

plt.figure(figsize=(12.8, 9.6))

for k in range(100):
    routeX = []
    routeY = []
    prevposition = findStart()
    print(prevposition)
    i = 0
    while i <= 50000:
        position = findNext(prevposition[0], prevposition[1])
        routeX.append(position[0])
        routeY.append(position[1])
        i += 1
        if not findNext(position[0], position[1]) or euclidD(position, prevposition) <= 1e-10:
            break
        prevposition = position
        if i % 1000 == 0:
            plt.quiver(lon, lat, uf, vf)
            plt.scatter(routeX, routeY)
plt.show()
print("E")

