import json
import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import KMeans

with open('stores.json', 'r') as openfile:
    stores = json.load(openfile)


with open('cache/compressed_cache.json', 'r') as openfile:
    found = json.load(openfile)


xpoints = []
ypoints = []

points = []

print(len(stores))
for store in stores:
    coords = store["coordinates"]
    points.append(coords)
    xpoints.append(coords[0])
    ypoints.append(coords[1])



plt.plot(xpoints, ypoints, 'o')



centroids = np.load("centroids.npy")
centers = [[],[]]
for center in centroids:
    centers[0].append(center[0])
    centers[1].append(center[1])

plt.plot(centers[0], centers[1],'o', markersize=12)


centers_f = [[],[]]
for key in found:
    center =  found[key]["store"]["coordinates"]
    centers_f[0].append(center[0])
    centers_f[1].append(center[1])

plt.plot(centers_f[0], centers_f[1],'o')

print(len(centers_f[0]))


plt.show()

