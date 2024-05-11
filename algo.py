from sklearn.cluster import KMeans
import numpy as np
import networkx as nx
import itertools
from geopy.distance import geodesic


def generate_schedule(number_of_neighbourhood=3, number_of_van=2, neighbors=[[10, 1, 1], [2, 39, -70], [3, 5, 7]], sts=(0, 0)):
    """
    # input neighbors=[[10,1,1],[...],....]  
        here [[id,latitude,longitude],....]

    # output two object result, path_result.  
        result[i]=[van number, neighbor id, finish time], 
        path_result[i]= optimized path for van i.
    """
    index = []
    locations = []

    def distance(location1, location2):
        # Calculate distance using geodesic distance between two latitude and longitude coordinates
        return geodesic(location1, location2).kilometers

    # Function to solve the Traveling Salesman Problem using the Held-Karp algorithm

    def tsp_held_karp(locations):
        n = len(locations)
        G = nx.complete_graph(n)  # Complete graph with locations as nodes

        # Calculate distances between all pairs of locations
        for i in range(n):
            for j in range(n):
                if i != j:
                    G[i][j]['weight'] = distance(locations[i], locations[j])

        # Generate all permutations of locations with the last location fixed at the end
        permutations = itertools.permutations(range(n - 1))

        # Initialize minimum distance and path
        min_distance = float('inf')
        min_path = None

        # Iterate over all permutations and calculate total distance
        for perm in permutations:
            # Add the last location to the end of the permutation
            perm_with_last = perm + (n - 1,)
            total_distance = 0
            for i in range(n - 1):
                total_distance += G[perm_with_last[i]
                                    ][perm_with_last[i + 1]]['weight']
    #         total_distance += G[perm_with_last[-1]][perm_with_last[0]]['weight']  # Add distance back to the starting location
            if total_distance < min_distance:
                min_distance = total_distance
                min_path = perm_with_last

        return min_path

    def cluster_locations(locations, m):
        X = np.array(locations)
        kmeans = KMeans(n_clusters=m, random_state=0).fit(X)
        return kmeans.labels_

    def generate_clusters(locations, m):
        labels = cluster_locations(locations, m)
        clusters = [[] for _ in range(m)]
        for i, label in enumerate(labels):
            clusters[label].append(i)

        return clusters

    for i in range(number_of_neighbourhood):
        index.append(neighbors[i][0])
        locations.append((neighbors[i][1], neighbors[i][2]))

    clusters = generate_clusters(locations, number_of_van)

    result = []
    path_result = []

    van_number = 1
    for cluster in clusters:
        time = 9
        length = len(cluster)

        loc = []
        for i in range(length):
            loc.append(locations[cluster[i]])
        loc.append(sts)
        path = tsp_held_karp(loc)

        prow = []
        rrow = []
        plen = len(path)

        for x in range(plen-1):
            ind = index[cluster[path[x]]]
            prow.append(ind)
            rrow = []
            rrow.append(van_number)
            rrow.append(ind)
            rrow.append(time)
            time = time+1
            result.append(rrow)

        prow.append("sts")
        path_result.append(prow)
        van_number += 1

    return result, path_result


result, path_result = generate_schedule()
print(result)
print(path_result)
