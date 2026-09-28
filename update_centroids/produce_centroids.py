import json
import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import KMeans

with open('./stores.json', 'r') as openfile:
    stores = json.load(openfile)


xpoints = []
ypoints = []

points = []

print(len(stores))
for store in stores:
    coords = store["coordinates"]
    points.append(coords)
    xpoints.append(coords[0])
    ypoints.append(coords[1])

clusters = 17

print("Points: "+str(len(points)))

found = True
for seed in range(0, 100000):
    found = True
    kmeans = KMeans(n_clusters=clusters, random_state=seed, n_init="auto", init="random").fit(points)

    clustered = [[] for _ in range(clusters)]

    #print(kmeans.cluster_centers_)
    labels = kmeans.labels_

    for i in range(len(kmeans.labels_)):
        clustered[labels[i]].append(points[i])

    for c in clustered:
        if len(c)>19:
            found = False
    if found:
        print("seed: "+str(seed))
        break

if found:
    
    for cluster in clustered:
        print(len(cluster))
        xypoints = list(zip(*cluster))
        plt.plot(xypoints[0], xypoints[1], 'o')

    print(kmeans.cluster_centers_)
    centers = list(zip(*kmeans.cluster_centers_))
    plt.plot(centers[0], centers[1],'o', markersize=12)


    plt.show()

    with open('centroids.npy', 'wb') as f:
        np.save(f, kmeans.cluster_centers_)